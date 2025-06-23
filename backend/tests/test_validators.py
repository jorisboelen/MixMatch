from datetime import date
from mixmatch.file.validators import parse_bpm, parse_date, parse_key


def test_parse_bpm():
    assert parse_bpm(['128', '128.3', '128.6']) == [128, 128, 128]
    assert parse_bpm([128, 128.3, 128.6]) == [128, 128, 128]
    assert parse_bpm([]) == []


def test_parse_date():
    assert parse_date(['2001-10-22', '1999-12-01', '2025-01-31']) == [date(year=2001, month=10, day=22),
                                                                      date(year=1999, month=12, day=1),
                                                                      date(year=2025, month=1, day=31)]
    assert parse_date(['2001-10', '1999-12', '2025-01']) == [date(year=2001, month=10, day=1),
                                                             date(year=1999, month=12, day=1),
                                                             date(year=2025, month=1, day=1)]
    assert parse_date(['2001', '1999', '2025']) == [date(year=2001, month=1, day=1),
                                                    date(year=1999, month=1, day=1),
                                                    date(year=2025, month=1, day=1)]


def test_parse_key():
    assert (parse_key(['1A', '6A', '12B'])) == ['1A', '6A', '12B']
    assert (parse_key(['A major', 'C# major', 'G# minor'])) == ['11B', '3B', '1A']
    assert (parse_key(['eyJrZXkiOiAiMUEifQ==', 'eyJrZXkiOiAiNkEifQ==', 'eyJrZXkiOiAiMTJCIn0='])) == ['1A', '6A', '12B']
    assert (parse_key(['eyJrZXkiOiAiQSBtYWpvciJ9', 'eyJrZXkiOiAiQyMgbWFqb3IifQ==', 'eyJrZXkiOiAiRyMgbWlub3IifQ=='])) == ['11B', '3B', '1A']
    assert (parse_key(['1a', '12C', 'Z# minor'])) == ['', '', '']
