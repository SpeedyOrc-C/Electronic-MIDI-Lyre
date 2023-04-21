import time
from typing import Tuple
from pynput.keyboard import Key, Controller
import pygame.midi as midi

midi.init()

print('MIDI Input Devices:')
for device_id in range(midi.get_count()):
    device_info: Tuple[bytes, bytes, int, int, int]
    device_info = midi.get_device_info(device_id)
    is_input = device_info[2]
    if is_input:
        device_name = device_info[1].decode('utf8')
        print(f'[{device_id + 1}]\t{device_name}')

selected_id: int = midi.get_default_input_id()
while True:
    try:
        selected_id = int(input('Select a device by its number: ')) - 1
    except ValueError:
        print('Please enter an integer.')
        continue

    if not 0 <= selected_id < midi.get_count():
        print(f'Please choose a number between 0 and {midi.get_count()-1}.')
        continue

    is_input = midi.get_device_info(selected_id)[2]
    if not is_input:
        print('This is not an input device.')
        continue

    break

midi_key_to_genshin_key = {
    60: 'z',
    62: 'x',
    64: 'c',
    65: 'v',
    67: 'b',
    69: 'n',
    71: 'm',

    72: 'a',
    74: 's',
    76: 'd',
    77: 'f',
    79: 'g',
    81: 'h',
    83: 'j',

    84: 'q',
    86: 'w',
    88: 'e',
    89: 'r',
    91: 't',
    93: 'y',
    95: 'u',
}

available_keys = set(midi_key_to_genshin_key.keys())

midi_input = midi.Input(selected_id)
keyboard = Controller()
while True:
    if not midi_input.poll():
        time.sleep(0.001)
        continue
    events = midi_input.read(midi_input.poll())
    for event in events:
        is_press = event[0][0] == 155
        if is_press:
            midi_key = event[0][1]
            if midi_key in available_keys:
                genshin_key = midi_key_to_genshin_key[midi_key]
                keyboard.press(genshin_key)
                keyboard.release(genshin_key)
