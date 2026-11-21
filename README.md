# TTWVR Alcohol

Alcohol in Fallout: New Vegas gradually blurs your vision, makes your aim drift, and sways your view in VR. At higher levels, you get double vision that briefly comes back into focus. Drinks keep their original stat bonuses and addiction chances.

## Install

1. Start with TTWVR 1.1.7, xNVSE and JIP LN NVSE installed.
2. Download the **TTWVR-Alcohol** ZIP from the [latest release](https://github.com/ethanfel/TTWVR-Alcohol/releases/latest) and install it with your mod manager.
3. Enable **TTWVRAlcohol.esp** and restart Fallout.

Physical Canteen is optional. If you use version 0.1.16 or earlier of Physical Canteen, give Alcohol priority for their shared DLL.

## Drink strength

| Units | Examples |
| --- | --- |
| 1 | Beer, irradiated beer |
| 2 | Wine, Rum & Nuka, Sierra Madre Martini |
| 3 | Vodka, whiskey, scotch, Wasteland Tequila |
| 4 | Moonshine, absinthe, large Wasteland Tequila |

Six units give full intensity. Two vodkas, six beers, or one vodka and three beers get you there when consumed together. You recover one unit per in-game hour, including waiting and sleeping. Drinking above six extends recovery. Other mods’ drinks tagged for alcohol addiction contribute two units by default.

## Settings

To turn off headset sway or double vision, set the corresponding value to `0` under `[Drinking]` in `Data/NVSE/Plugins/TTWVRPhysicalCanteen.ini`. Both default to `1`. Create the file if needed, then restart Fallout.

```ini
[Drinking]
ViewSway=1
DoubleVision=1
```

## Build

On Linux, install GNU Make, Python 3, a C++17 compiler, 32-bit MinGW-w64 C++ and the OpenXR headers. Run `make test` and `make package`. The installable ZIP appears in `build/`. The shared runtime source is included under `src/`.

Licensed under [GPL-3.0-only](LICENSE).
