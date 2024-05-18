import time

import rtmidi
import pynput


def is_note_on(e: int) -> bool: return e >> 4 == 0b1001


def is_note_off(e: int) -> bool: return e >> 4 == 0b1000


def main(mapping: dict[int, str], transpose: int, enable_hold: bool):
    midi_in = rtmidi.MidiIn()
    available_ports: list[str] = midi_in.get_ports()

    for i, available_port in enumerate(available_ports):
        print(f'{i} - {available_port}')

    while True:
        port_no_raw = input('Choose a MIDI device, or press ENTER for 0: ')
        if not port_no_raw:
            port_no = 0
            break
        else:
            try:
                port_no = int(port_no_raw)
                break
            except:
                print('Please enter a number.')

    try:
        midi_in.open_port(port_no)
    except rtmidi.InvalidPortError:
        print(f'Cannot find port #{port_no}.')

    controller = pynput.keyboard.Controller()

    print('Mapping starts...')

    while True:
        raw_message = midi_in.get_message()

        if raw_message is None:
            continue

        [event, note, velocity], dt = raw_message
        mapped_note = note + transpose

        try:
            key = mapping[mapped_note]
        except KeyError:
            print(f'Cannot map note #{mapped_note}.')
            continue

        if enable_hold:
            if is_note_on(event):
                controller.press(key)
            elif is_note_off(event):
                controller.release(key)
        else:
            if is_note_on(event) or is_note_off(event):
                controller.press(key)
                controller.release(key)

        time.sleep(0.01)
