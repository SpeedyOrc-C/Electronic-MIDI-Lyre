# Electronic MIDI Lyre

## Usage Example

### Freestyle

```shell
python main.py genshin-lyre freestyle
```

Play freely with the Lyre in Genshin Impact.

### Play MIDI File

```shell
python main.py genshin-horn play song.mid
```

Play `song.mid` with the French horn in Genshin Impact.

## CLI

```shell
python main.py <instrument> freestyle
```

```shell
python main.py <instrument> play <file>
```

### All Instruments

* `genshin-lyre`
* `genshin-horn`

### Enable Hold Notes

`-eh` / `-enable-hold`

### Transpose

`-t amount` / `--transpose amount`

e.g. `-t 7` will map C4 to G4.
