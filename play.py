import time
import _thread
from typing import Optional

import mido
import pynput


def on_press(key: pynput.keyboard.Key):
    if key == pynput.keyboard.Key.esc:
        print()
        print('Manually terminated!')
        _thread.interrupt_main()


def main(mapping: dict[int, str], transpose: int, file_path: str, enable_hold: bool):
    controller = pynput.keyboard.Controller()
    pynput.keyboard.Listener(on_press=on_press).start()

    midi = mido.MidiFile(file_path)

    print('Song will start in 3 seconds...')
    time.sleep(1)
    print('Song will start in 2 seconds...')
    time.sleep(1)
    print('Song will start in 1 seconds...')
    time.sleep(1)
    print('Song starts...')

    ticks_per_beat = midi.ticks_per_beat
    microsecond_per_4: Optional[int] = None

    for event in midi.merged_track:
        match event.type:
            case 'set_tempo':
                microsecond_per_4 = event.tempo

            case 'note_on' | 'note_off':
                if microsecond_per_4 is None:
                    raise ValueError('Tempo is not specified before the first note.')

                mapped_note = event.note + transpose

                try:
                    key = mapping[mapped_note]
                    duration = mido.tick2second(event.time, ticks_per_beat, microsecond_per_4)

                    if enable_hold:
                        match event.type:
                            case 'note_on':
                                controller.press(key)
                            case 'note_off':
                                controller.release(key)
                    else:
                        match event.type:
                            case 'note_on':
                                controller.press(key)
                                controller.release(key)

                except KeyError:
                    print(f'Cannot map note #{mapped_note}.')
                    continue

                time.sleep(duration)
    print()

    print('Song terminated normally.')

    return 0
