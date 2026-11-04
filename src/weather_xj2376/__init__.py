# read version from installed package
from importlib.metadata import version
__version__ = version("weather_xj2376")

from weather_xj2376.weather_xj2376 import (
    celsius_to_fahrenheit,
    summarize_temperatures,
    clean_readings,
)