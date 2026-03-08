import pathlib

import pytest

import sketchplot as sp

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def _read_fixture(name: str) -> str:
    return (FIXTURES / name).read_text()


class TestBarSnapshot:
    def test_basic_unicode(self) -> None:
        result = sp.bar([3, 5, 2, 8, 6], title="Sales", render="string")
        assert result == _read_fixture("bar_basic_unicode.txt")

    def test_basic_ascii(self) -> None:
        result = sp.bar(
            [3, 5, 2, 8, 6], title="Sales", render="string", charset="ascii"
        )
        assert result == _read_fixture("bar_basic_ascii.txt")

    def test_multi_unicode(self) -> None:
        result = sp.bar(
            [[4, 7, 2, 9], [2, 5, 8, 3]], title="Comparison", render="string"
        )
        assert result == _read_fixture("bar_multi_unicode.txt")

    def test_multi_ascii(self) -> None:
        result = sp.bar(
            [[4, 7, 2, 9], [2, 5, 8, 3]],
            title="Comparison",
            render="string",
            charset="ascii",
        )
        assert result == _read_fixture("bar_multi_ascii.txt")

    def test_single_unicode(self) -> None:
        result = sp.bar([42], render="string")
        assert result == _read_fixture("bar_single_unicode.txt")

    def test_single_ascii(self) -> None:
        result = sp.bar([42], render="string", charset="ascii")
        assert result == _read_fixture("bar_single_ascii.txt")


class TestBarEdgeCases:
    def test_all_same_value(self) -> None:
        result = sp.bar([5, 5, 5, 5], render="string")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_single_value_in_series(self) -> None:
        result = sp.bar([7], render="string")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_two_series(self) -> None:
        result = sp.bar([[1, 2, 3], [4, 5, 6]], render="string")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_print_mode(self, capsys: pytest.CaptureFixture[str]) -> None:
        result = sp.bar([1, 2, 3], render="print")
        assert result is None
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_generator_input(self) -> None:
        result = sp.bar(iter([1, 2, 3]), render="string")
        assert isinstance(result, str)
        assert len(result) > 0


class TestBarValidation:
    def test_empty_data(self) -> None:
        with pytest.raises(ValueError, match="empty data"):
            sp.bar([], render="string")

    def test_nan_data(self) -> None:
        with pytest.raises(ValueError, match="NaN"):
            sp.bar([1.0, float("nan")], render="string")

    def test_mismatched_series_lengths(self) -> None:
        with pytest.raises(ValueError, match="same length"):
            sp.bar([[1, 2, 3], [4, 5]], render="string")

    def test_invalid_charset(self) -> None:
        with pytest.raises(ValueError, match="charset"):
            sp.bar([1, 2, 3], charset="utf8", render="string")

    def test_width_too_small(self) -> None:
        with pytest.raises(ValueError, match="width"):
            sp.bar([1, 2, 3], width=5, render="string")
