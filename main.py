import argparse
from typing import Optional, Literal

import mappings
import freestyle
import play


class Args:
    instrument: Literal['genshin-lyre', 'genshin-horn']
    action: str
    file_path: Optional[str]
    transpose: int
    enable_hold: bool


def main(args: Args):
    mapping: dict[int, str]

    match args.instrument:
        case 'genshin-lyre':
            mapping = mappings.MAPPING_GENSHIN_LYRE
        case 'genshin-horn':
            mapping = mappings.MAPPING_GENSHIN_HORN
        case _:
            raise ValueError('This should never happen')

    match args.action:
        case 'freestyle':
            freestyle.main(mapping, args.transpose, args.enable_hold)
        case 'play':
            play.main(mapping, args.transpose, args.file_path, args.enable_hold)
        case _:
            raise ValueError('This should never happen')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('instrument', choices=['genshin-lyre', 'genshin-horn'])
    parser.add_argument('action', choices=['freestyle', 'play'])
    parser.add_argument('file_path', nargs='?')
    parser.add_argument('-t', '--transpose', type=int, default=0)
    parser.add_argument('-eh', '--enable-hold', action='store_true')

    # noinspection PyTypeChecker
    parsed_args: Args = parser.parse_args()

    match parsed_args.action:
        case 'freestyle':
            if parsed_args.file_path is not None:
                parser.error('Unexpected file name.')
        case 'play':
            if parsed_args.file_path is None:
                parser.error('Expect a MIDI file.')

    main(parsed_args)
