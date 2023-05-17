"""
A script that helps you play Lyres in Genshin Impact with your MIDI keyboard.
"""

import pynput.keyboard
import pygame.midi

import time


def is_note_on_event(e: int) -> bool:
    """
    Check if this MIDI event is "Note On"
    """
    return e >> 4 == 0b1001


midi_key_to_lyre_key = {
    84: 'q', 86: 'w', 88: 'e', 89: 'r', 91: 't', 93: 'y', 95: 'u',
    72: 'a', 74: 's', 76: 'd', 77: 'f', 79: 'g', 81: 'h', 83: 'j',
    60: 'z', 62: 'x', 64: 'c', 65: 'v', 67: 'b', 69: 'n', 71: 'm',
}

pygame.midi.init()
print("=== Electronic MIDI Lyre ===")
print("Middle C is mapped to key A (first note at 2nd row) in the game.")

print('MIDI Input Devices:')
for device_id in range(pygame.midi.get_count()):
    device_info = pygame.midi.get_device_info(device_id)
    is_input = device_info[2]
    if is_input:
        device_name = device_info[1].decode('utf8')
        print(f'  [{device_id + 1}]\t{device_name}')

selected_id: int = pygame.midi.get_default_input_id()
while True:
    try:
        selected_id = int(input('Select a device by its number: '))
    except ValueError:
        print('Please enter an integer.')
        continue

    if not 1 <= selected_id <= pygame.midi.get_count():
        print(f'Please choose a number between 1 and {pygame.midi.get_count()}.')
        continue

    is_input = pygame.midi.get_device_info(selected_id - 1)[2]
    if not is_input:
        print('This is not an input device.')
        continue

    break

available_keys = set(midi_key_to_lyre_key.keys())
midi_input = pygame.midi.Input(selected_id - 1)
keyboard = pynput.keyboard.Controller()

print('Mapping start...')
while True:

    if not midi_input.poll():
        time.sleep(0.001)
        continue

    for event in midi_input.read(midi_input.poll()):
        if not is_note_on_event(event[0][0]):
            continue

        midi_key = event[0][1]
        if midi_key not in available_keys:
            print('\b' * 128 + ' ' * 128 + '\b' * 128, end='')
            print(f'Key {midi_key} is not in lyre\'s range.', end='')
            continue

        lyre_key = midi_key_to_lyre_key[midi_key]
        keyboard.press(lyre_key)
        keyboard.release(lyre_key)
