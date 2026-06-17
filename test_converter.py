"""单位换算模块单元测试。"""

import unittest

from converter import (
    convert,
    get_supported_units,
    get_categories,
)


class TestLengthConversion(unittest.TestCase):
    """长度单位换算测试。"""

    def test_meter_to_kilometer(self):
        result = convert(1000, "meter", "kilometer")
        self.assertAlmostEqual(result, 1.0)

    def test_kilometer_to_meter(self):
        result = convert(1, "km", "m")
        self.assertAlmostEqual(result, 1000.0)

    def test_centimeter_to_meter(self):
        result = convert(100, "cm", "m")
        self.assertAlmostEqual(result, 1.0)

    def test_millimeter_to_centimeter(self):
        result = convert(10, "mm", "cm")
        self.assertAlmostEqual(result, 1.0)

    def test_inch_to_centimeter(self):
        result = convert(1, "inch", "cm")
        self.assertAlmostEqual(result, 2.54)

    def test_foot_to_meter(self):
        result = convert(1, "foot", "meter")
        self.assertAlmostEqual(result, 0.3048)

    def test_mile_to_kilometer(self):
        result = convert(1, "mile", "km")
        self.assertAlmostEqual(result, 1.609344)

    def test_yard_to_meter(self):
        result = convert(1, "yard", "m")
        self.assertAlmostEqual(result, 0.9144)

    def test_same_unit(self):
        result = convert(5, "m", "m")
        self.assertEqual(result, 5.0)


class TestWeightConversion(unittest.TestCase):
    """重量单位换算测试。"""

    def test_kilogram_to_gram(self):
        result = convert(1, "kg", "g")
        self.assertAlmostEqual(result, 1000.0)

    def test_gram_to_milligram(self):
        result = convert(1, "gram", "milligram")
        self.assertAlmostEqual(result, 1000.0)

    def test_pound_to_kilogram(self):
        result = convert(1, "pound", "kg")
        self.assertAlmostEqual(result, 0.45359237)

    def test_ounce_to_gram(self):
        result = convert(1, "oz", "g")
        self.assertAlmostEqual(result, 28.349523125)

    def test_metric_ton_to_kilogram(self):
        result = convert(1, "t", "kg")
        self.assertAlmostEqual(result, 1000.0)

    def test_stone_to_pound(self):
        result = convert(1, "stone", "lb")
        self.assertAlmostEqual(result, 14.0)


class TestTemperatureConversion(unittest.TestCase):
    """温度单位换算测试。"""

    def test_celsius_to_fahrenheit_freezing(self):
        result = convert(0, "celsius", "fahrenheit")
        self.assertAlmostEqual(result, 32.0)

    def test_celsius_to_fahrenheit_boiling(self):
        result = convert(100, "c", "f")
        self.assertAlmostEqual(result, 212.0)

    def test_fahrenheit_to_celsius_freezing(self):
        result = convert(32, "fahrenheit", "celsius")
        self.assertAlmostEqual(result, 0.0)

    def test_fahrenheit_to_celsius_boiling(self):
        result = convert(212, "f", "c")
        self.assertAlmostEqual(result, 100.0)

    def test_celsius_to_kelvin_zero(self):
        result = convert(0, "celsius", "kelvin")
        self.assertAlmostEqual(result, 273.15)

    def test_kelvin_to_celsius_absolute_zero(self):
        result = convert(0, "kelvin", "celsius")
        self.assertAlmostEqual(result, -273.15)

    def test_fahrenheit_to_kelvin(self):
        result = convert(32, "fahrenheit", "kelvin")
        self.assertAlmostEqual(result, 273.15)

    def test_kelvin_to_fahrenheit(self):
        result = convert(273.15, "k", "f")
        self.assertAlmostEqual(result, 32.0)

    def test_same_temperature_unit(self):
        result = convert(25, "celsius", "celsius")
        self.assertEqual(result, 25.0)


class TestVolumeConversion(unittest.TestCase):
    """体积单位换算测试。"""

    def test_cubic_meter_to_liter(self):
        result = convert(1, "cubic_meter", "liter")
        self.assertAlmostEqual(result, 1000.0)

    def test_liter_to_milliliter(self):
        result = convert(1, "L", "mL")
        self.assertAlmostEqual(result, 1000.0)

    def test_milliliter_to_cubic_centimeter(self):
        result = convert(1, "ml", "cm3")
        self.assertAlmostEqual(result, 1.0)

    def test_gallon_us_to_liter(self):
        result = convert(1, "gallon_us", "liter")
        self.assertAlmostEqual(result, 3.785411784)

    def test_gallon_uk_to_liter(self):
        result = convert(1, "gal_uk", "L")
        self.assertAlmostEqual(result, 4.54609)

    def test_cubic_foot_to_cubic_meter(self):
        result = convert(1, "ft3", "m3")
        self.assertAlmostEqual(result, 0.028316846592)

    def test_cubic_inch_to_cubic_centimeter(self):
        result = convert(1, "in3", "cm3")
        self.assertAlmostEqual(result, 16.387064)


class TestTimeConversion(unittest.TestCase):
    """时间单位换算测试。"""

    def test_minute_to_second(self):
        result = convert(1, "minute", "second")
        self.assertEqual(result, 60.0)

    def test_hour_to_minute(self):
        result = convert(1, "hour", "minute")
        self.assertEqual(result, 60.0)

    def test_day_to_hour(self):
        result = convert(1, "day", "hour")
        self.assertEqual(result, 24.0)

    def test_week_to_day(self):
        result = convert(1, "week", "day")
        self.assertEqual(result, 7.0)

    def test_hour_to_second(self):
        result = convert(1, "h", "s")
        self.assertEqual(result, 3600.0)

    def test_millisecond_to_second(self):
        result = convert(1000, "ms", "sec")
        self.assertEqual(result, 1.0)

    def test_year_to_day(self):
        result = convert(1, "year", "day")
        self.assertAlmostEqual(result, 365.2425)


class TestErrorHandling(unittest.TestCase):
    """错误处理测试。"""

    def test_unknown_unit(self):
        with self.assertRaises(ValueError):
            convert(1, "unknown_unit", "meter")

    def test_unknown_target_unit(self):
        with self.assertRaises(ValueError):
            convert(1, "meter", "unknown_unit")

    def test_category_mismatch_length_weight(self):
        with self.assertRaises(ValueError):
            convert(1, "meter", "kilogram")

    def test_category_mismatch_temperature_length(self):
        with self.assertRaises(ValueError):
            convert(1, "celsius", "meter")


class TestSupportedUnits(unittest.TestCase):
    """支持单位查询测试。"""

    def test_get_all_units(self):
        units = get_supported_units()
        self.assertIn("length", units)
        self.assertIn("weight", units)
        self.assertIn("volume", units)
        self.assertIn("time", units)
        self.assertIn("temperature", units)

    def test_get_length_units(self):
        units = get_supported_units("length")
        self.assertIn("length", units)
        self.assertIn("meter", units["length"])
        self.assertIn("km", units["length"])

    def test_get_temperature_units(self):
        units = get_supported_units("temperature")
        self.assertIn("temperature", units)
        self.assertIn("celsius", units["temperature"])
        self.assertIn("fahrenheit", units["temperature"])

    def test_get_unknown_category(self):
        with self.assertRaises(ValueError):
            get_supported_units("unknown_category")

    def test_get_categories(self):
        categories = get_categories()
        self.assertIn("length", categories)
        self.assertIn("weight", categories)
        self.assertIn("volume", categories)
        self.assertIn("time", categories)
        self.assertIn("temperature", categories)


class TestUnitAliases(unittest.TestCase):
    """单位别名测试。"""

    def test_length_aliases(self):
        r1 = convert(1, "meter", "cm")
        r2 = convert(1, "m", "centimeter")
        self.assertAlmostEqual(r1, r2)

    def test_weight_aliases(self):
        r1 = convert(1, "kilogram", "pound")
        r2 = convert(1, "kg", "lb")
        self.assertAlmostEqual(r1, r2)

    def test_temperature_aliases(self):
        r1 = convert(25, "celsius", "fahrenheit")
        r2 = convert(25, "c", "f")
        self.assertAlmostEqual(r1, r2)

    def test_time_aliases(self):
        r1 = convert(1, "hour", "minute")
        r2 = convert(1, "h", "min")
        self.assertAlmostEqual(r1, r2)


if __name__ == "__main__":
    unittest.main()
