from base64 import b64decode, b64encode
from json import loads
from math import modf
from prettytable import PrettyTable
from re import findall


MUSIC_KEYS = ['1A', '1B', '2A', '2B', '3A', '3B', '4A', '4B', '5A', '5B', '6A', '6B',
              '7A', '7B', '8A', '8B', '9A', '9B', '10A', '10B', '11A', '11B', '12A', '12B']

MUSIC_KEYS_CAMELOT = {'A major': '11B', 'Ab major': '4B', 'A minor': '8A', 'Ab minor': '1A',
                      'B major': '1B', 'Bb major': '6B', 'Bb minor': '3A', 'B minor': '10A',
                      'C major': '8B', 'C# major': '3B', 'Db minor': '12A', 'C# minor': '12A', 'C minor': '5A',
                      'D major': '10B', 'Db major': '3B', 'D minor': '7A',
                      'E major': '12B', 'Eb major': '5B', 'Eb minor': '2A', 'E minor': '9A',
                      'F major': '7B', 'F# minor': '11A', 'F minor': '4A', 'F# major': '2B',
                      'G major': '9B', 'G# minor': '1A', 'Gb major': '2B', 'G minor': '6A'}


def dict_to_table(ld: list[dict]) -> str:
    if ld:
        table = PrettyTable(field_names=list(ld[0].keys()))
        table.add_rows([list(d.values()) for d in ld])
        return table.get_string()
    else:
        return ''


def get_compatible_keys(key: str, include_key: bool=False) -> list[str]:
    compatible_keys = []
    if key not in MUSIC_KEYS:
        raise ValueError(f'Invalid key {key}. Value not in {MUSIC_KEYS}')
    split_key = findall(r'[A-Za-z]+|\d+', key)
    compatible_keys.append(f'{str(split_key[0])}A')
    compatible_keys.append(f'{str(split_key[0])}B')
    if int(split_key[0]) == 1:
        compatible_keys.append('12A')
        compatible_keys.append('2A')
    elif int(split_key[0]) == 12:
        compatible_keys.append('11A')
        compatible_keys.append('1A')
    else:
        compatible_keys.append(f'{str(int(split_key[0]) - 1)}A')
        compatible_keys.append(f'{str(int(split_key[0]) + 1)}A')
    if not include_key:
        compatible_keys.remove(key)
    return compatible_keys


def is_base64(sb: str | bytes) -> bool:
    try:
        if isinstance(sb, str):
            sb_bytes = bytes(sb, 'ascii')
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            raise ValueError("Argument must be string or bytes")
        return b64encode(b64decode(sb_bytes)) == sb_bytes
    except Exception:
        return False


def is_json(s: bytes) -> bool:
    try:
        loads(s)
    except ValueError:
        return False
    return True


def round_bpm(input_bpm: int | float) -> int:
    fractional, integer = modf(input_bpm)
    bpm = int(integer)
    if fractional > 0.05:
        bpm += 1
    return bpm
