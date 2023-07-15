# DayR Unpacker
Unpacks the resource.car file within the `assets/` folder of DayR's APK.

## Using
```
git clone https://github.com/yntha/dayr-unpacker
cd dayr-unpacker
python dayr-unpacker <resource.car path>
```
Three new directories will be created:
- `dis`: Disassembled Lua 5.1 bytecode
- `res`: Raw unpacked and compiled lua files
- `src`: Decompiled Lua 5.1 files

Lua module names are represented as paths in `dis` and `src`. Ex:<br/>
`lib.config.enemy_config.lu -> lib/config/enemy_config.lua`

## Credit
This project requires [corona-archiver.py](https://github.com/0BuRner/corona-archiver). [LICENSE](https://github.com/0BuRner/corona-archiver/blob/master/LICENSE)<br/>
This project requires [unluac](https://sourceforge.net/p/unluac/). [LICENSE](https://sourceforge.net/p/unluac/hgcode/ci/default/tree/license.txt)
