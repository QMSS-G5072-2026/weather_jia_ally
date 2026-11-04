
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
import weather_xj2376

from weather_xj2376 import (
    celsius_to_fahrenheit,
    summarize_temperatures,
    clean_readings,
)


def test_version_is_defined():
    assert isinstance(weather_xj2376.__version__, str)



# =============================================================================
# PART 1: UNIT TESTS
# =============================================================================


@pytest.mark.parametrize(
    "celsius, expected", [
        (0, 32),
        (100, 212),
        (-40, -40),
        (37, 98.6),
        (-273.15, -459.67)
    ]

)
def test_celsius_to_fahrenheit(celsius, expected):
    result = celsius_to_fahrenheit(celsius)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize('bad_input, expected_error', [
    ('string', TypeError),
    (None, TypeError),
    (True, TypeError),
    (-300, ValueError),
])

def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)


def test_summarize_temperatures():
    test_arrange = [20.0, 25.0, float('nan'), 30.0]
    result = summarize_temperatures(test_arrange)
    assert result['mean'] == pytest.approx(25.0)
    assert result['min'] == 20.0
    assert result['max'] == 30.0
    assert result['n_missing'] == 1

# =============================================================================
# PART 2: FIXTURES
# =============================================================================


@pytest.fixture
def raw_readings():
   
    return pd.DataFrame({
    "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
    "date": ["2026-07-02", "2026-07-01", "2026-07-01", "2026-07-02", "2026-07-01"],
    "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
    })


def test_raw_readings_fixture(raw_readings):
    columns = list(raw_readings.columns)
    rows = len(raw_readings)
    missing_data = raw_readings.isna().sum().sum()

    assert columns == ['station', 'date', 'temp_c']
    assert rows == 5
    assert missing_data == 1


# =============================================================================
# PART 3: TESTING DATAFRAMES
# =============================================================================


def test_clean_readings(raw_readings):
    expected_results = pd.DataFrame({
        "station": ["CPK", "JFK", "LGA"],
        "date": ["2026-07-01", "2026-07-02","2026-07-01"],
        "temp_c": [25.0, 30.0, 28.0],
        "temp_f": [77.0, 86.0, 82.4],
    })
    actual_results = clean_readings(raw_readings)
    assert_frame_equal(expected_results, actual_results)

