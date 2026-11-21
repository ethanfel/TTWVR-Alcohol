# SPDX-License-Identifier: GPL-3.0-only
"""Build the ordinary alcohol addon with the shared VR effects runtime."""
from pathlib import Path
from struct import pack
import sys
from zipfile import ZIP_DEFLATED, ZipFile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
from records import group, image_modifier, record, string

# Stable local form IDs in the owning master. Display names may be localized.
SERVINGS = {
    "FalloutNV.esm": [
        (0x15197, "Beer", 1), (0x143FDE, "Irradiated Beer", 1),
        (0x3404A, "Wine", 2), (0x118356, "Drugged Wine", 2),
        (0x11702C, "Rum & Nuka", 2), (0xE2F6A, "Atomic Cocktail", 2),
        (0x32C74, "Vodka", 3), (0x32C75, "Whiskey", 3),
        (0x151A1, "Scotch", 3), (0x143FE1, "Irradiated Whiskey", 3),
        (0x143FEF, "Irradiated Scotch", 3), (0x122B4A, "Dixon's Whiskey", 3),
        (0x1673D6, "Jake Juice", 3), (0x115EB1, "Absinthe", 4),
        (0x16163D, "Moonshine", 4),
    ],
    "DeadMoney.esm": [(0x10395, "Sierra Madre Martini", 2)],
    "HonestHearts.esm": [(0x11111, "Wasteland Tequila", 3),
                         (0x112F9, "Large Wasteland Tequila", 4)],
    "OldWorldBlues.esm": [(0x1495E, "Battle Brew", 2)],
    "PointLookout.esm": [(0x422D, "Moonshine", 4)],
    "TaleOfTwoWastelands.esm": [(0x7D2A, "Ant Nog", 2), (0x7D2C, "Fire Ant Nog", 2),
                                (0x18098, "Centaur Sangria", 2)],
}


def registration():
    lines = []
    for master, drinks in SERVINGS.items():
        lines.append(f' if IsModLoaded "{master}"')
        for form, name, units in drinks:
            lines.extend([
                f'  let beverage := GetFormFromMod "{master}" "{form:06X}" ; {name}',
                '  if eval beverage',
                f'   AuxVarSetFlt "*_TTWVRAlcoholUnits" {units} 0 beverage',
                '   SetOnUseAidItemEventHandler callback 1 beverage',
                '  endif',
            ])
        lines.append(' endif')
    return (HERE / "Register.txt").read_text().replace(" ; @servings", "\n".join(lines))


def esp():
    header = record(b"TES4", 0, [
        (b"HEDR", pack("<fII", 1.34, 3, 0x807)), (b"CNAM", string("TTWVR Alcohol")),
        (b"MAST", string("FalloutNV.esm")), (b"DATA", bytes(8)),
    ])
    blur = image_modifier(0x01000805, "TTWVRAlcoholBlur", blur=2.4)
    ghost = image_modifier(0x01000806, "TTWVRAlcoholDoubleVision", refocus=True)
    return header + group(b"IMAD", blur + ghost)


def build():
    build_dir = ROOT / "build"
    out = build_dir / "TTWVR-Alcohol-0.1.0.zip"
    udf = "NVSE/user_defined_functions/TTWVRAlcohol"
    with ZipFile(out, "w", ZIP_DEFLATED) as archive:
        archive.write(build_dir / "TTWVRPhysicalCanteen.dll", "NVSE/Plugins/TTWVRPhysicalCanteen.dll")
        archive.writestr("TTWVRAlcohol.esp", esp())
        archive.writestr("NVSE/Plugins/scripts/ln_TTWVRAlcohol.txt",
                         'Call (CompileScript "TTWVRAlcohol/Register.txt")\n')
        archive.writestr(f"{udf}/Register.txt", registration())
        archive.write(HERE / "Drink.txt", f"{udf}/Drink.txt")
        archive.write(ROOT / "README.md", "docs/TTWVRAlcohol/README.md")
        archive.write(ROOT / "LICENSE", "docs/TTWVRAlcohol/LICENSE")
    print(out)


if __name__ == "__main__":
    build()
