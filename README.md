# Electronic MIDI Lyre

## Dependencies

- pynput
- rtmidi

## Usage Example

### Freestyle

```shell
python3 main.py genshin-lyre freestyle
```

Play freely with the Lyre in Genshin Impact.

### Play MIDI File

```shell
python3 main.py genshin-horn play song.mid
```

Play `song.mid` with the French horn in Genshin Impact.

## CLI

```shell
python3 main.py <instrument> freestyle
```

```shell
python3 main.py <instrument> play <file>
```

```shell
python3 main.py <instrument> freestyle [--transpose transpose-amount]
python3 main.py <instrument> play <file> [--transpose transpose-amount]
```

### All Instruments

* `genshin-lyre`
* `genshin-horn`
