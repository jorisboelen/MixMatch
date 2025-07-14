from base64 import b64decode
from datetime import date, datetime
from json import loads
from mixmatch.core.utils import is_base64, is_json, MUSIC_KEYS, MUSIC_KEYS_CAMELOT
from re import match
from typing import Any


def parse_bpm(values: Any) -> Any:
    def parse_bpm_value(value: str) -> int:
        return abs(int(float(value)))

    if isinstance(values, list):
        return [parse_bpm_value(str(value)) for value in values]
    return values


def parse_date(values: Any) -> Any:
    def parse_date_value(value: str) -> date:
        if match(r'^[1-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$', value):
            return datetime.strptime(value, '%Y-%m-%d').date()
        elif match(r'^[1-9][0-9][0-9][0-9]-[0-1][0-9]$', value):
            return datetime.strptime(value, '%Y-%m').date()
        elif match(r'^[1-9][0-9][0-9][0-9]$', value):
            return datetime.strptime(value, '%Y').date()
        else:
            return date.today()

    if isinstance(values, list):
        return [parse_date_value(str(value)) for value in values]
    return values


def parse_key(values: Any) -> Any:
    def parse_key_value(value: str) -> str:
        # key is in mixed-in-key format
        if is_base64(value) and is_json(b64decode(value)):
            value = loads(b64decode(value)).get('key')
        # convert keys in different notation
        if value in MUSIC_KEYS_CAMELOT.keys():
            value = MUSIC_KEYS_CAMELOT.get(value)
        # discard keys in incompatible format
        if value not in MUSIC_KEYS:
            value = ''
        return value

    if isinstance(values, list):
        return [parse_key_value(str(value)) for value in values]
    return values
