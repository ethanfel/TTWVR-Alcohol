# SPDX-License-Identifier: GPL-3.0-only
from pathlib import Path
import re
import struct
import sys
from unittest import TestCase, main

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "alcohol"))
from package import SERVINGS, esp, registration


def records(data):
    pos = 0
    while pos < len(data):
        tag, size, _, form = struct.unpack_from("<4sIII", data, pos)
        if tag == b"GRUP":
            yield from records(data[pos + 24:pos + size])
            pos += size
            continue
        end = pos + 24 + size
        pos += 24
        fields = []
        while pos < end:
            key, length = struct.unpack_from("<4sH", data, pos)
            pos += 6
            fields.append((key, data[pos:pos + length]))
            pos += length
        assert pos == end
        yield tag, form, fields


class Alcohol(TestCase):
    def test_no_game_records_overridden_or_canteen_master(self):
        header, blur, split = records(esp())
        self.assertEqual([v for k, v in header[2] if k == b"MAST"], [b"FalloutNV.esm\0"])
        self.assertEqual([(tag, form) for tag, form, _ in (blur, split)],
                         [(b"IMAD", 0x01000805), (b"IMAD", 0x01000806)])

    def test_generated_servings_and_mixed_drinks(self):
        script = registration()
        rows = re.findall(r'GetFormFromMod "([^"]+)" "([A-F0-9]+)" ; ([^\n]+)\n'
                          r'  if eval beverage\n   AuxVarSetFlt "\*_TTWVRAlcoholUnits" (\d+) 0 beverage\n'
                          r'   SetOnUseAidItemEventHandler callback 1 beverage', script)
        self.assertEqual(len(rows), sum(map(len, SERVINGS.values())))
        self.assertEqual(len({(master, form) for master, form, _, _ in rows}), len(rows))
        drinks = {name: int(units) for _, _, name, units in rows}
        self.assertEqual(6 * drinks["Beer"], 6)
        self.assertEqual(2 * drinks["Vodka"], 6)
        self.assertEqual(drinks["Beer"] + drinks["Wine"] + drinks["Vodka"], 6)
        self.assertEqual(drinks["Moonshine"], 4)
        self.assertIn('GetAddictionEffect beverage', script)


if __name__ == "__main__":
    main()
