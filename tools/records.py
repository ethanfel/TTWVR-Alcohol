# SPDX-License-Identifier: GPL-3.0-only
from struct import pack, pack_into


def string(value):
    return value.encode("ascii") + b"\0"


def record(tag, number, fields, flags=0):
    data = b"".join(pack("<4sH", name, len(value)) + value for name, value in fields)
    return pack("<4sIIIIHH", tag, len(data), flags, number, 0, 15, 0) + data


def group(tag, data):
    return pack("<4sI4sIII", b"GRUP", 24 + len(data), tag, 0, 0, 0) + data


def image_modifier(form_id, editor_id, *, blur=0, refocus=False):
    # Non-animated FNV IMAD. Static channels use two equal keys.
    # Multiplicative channels are identity and additive channels are zero.
    counts = [2] * 61
    for idx in (0, 1, 50, 51, 52, 56):
        counts[idx] = 0
    if refocus:
        # JIP updates the live value and first key for trait 46. One key
        # keeps the running modifier at that value until the next update.
        counts[46] = 1
    data = bytearray(pack("<61I", *counts))
    pack_into("<2f", data, 51 * 4, 0.5, 0.5)
    fields = [(b"EDID", string(editor_id)), (b"DNAM", data)]
    def curve(tag, value):
        fields.append((tag, pack("<4f", 0, value, 1, value)))
    curve(b"BNAM", blur)
    if refocus:
        fields.append((b"VNAM", pack("<2f", 0, 0)))
    else:
        curve(b"VNAM", 0)
    for tag in (b"TNAM", b"NAM3"):
        fields.append((tag, pack("<10f", 0, 0, 0, 0, 0, 1, 0, 0, 0, 0)))
    for tag in (b"RNAM", b"SNAM", b"UNAM", b"NAM1", b"NAM2", b"WNAM", b"XNAM", b"YNAM", b"NAM4"):
        curve(tag, 0)
    for channel in range(21):
        curve(bytes([channel]) + b"IAD", 1)
        curve(bytes([channel + 64]) + b"IAD", 0)
    return record(b"IMAD", form_id, fields)
