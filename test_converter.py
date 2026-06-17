"""单位换算模块单元测试。"""

import unittest
from decimal import Decimal

from converter import (
    convert,
    get_supported_units,
    get_categories,
    set_precision,
    get_common_conversions,
    quick_convert,
    search_conversions,
)


class TestLengthConversion(unittest.TestCase):
    """长度单位换算测试。"""

    def test_meter_to_kilometer(self):
        result = convert(1000, "meter", "kilometer")
        self.assertEqual(result, Decimal("1"))

    def test_kilometer_to_meter(self):
        result = convert(1, "km", "m")
        self.assertEqual(result, Decimal("1000"))

    def test_centimeter_to_meter(self):
        result = convert(100, "cm", "m")
        self.assertEqual(result, Decimal("1"))

    def test_millimeter_to_centimeter(self):
        result = convert(10, "mm", "cm")
        self.assertEqual(result, Decimal("1"))

    def test_inch_to_centimeter(self):
        result = convert(1, "inch", "cm")
        self.assertEqual(result, Decimal("2.54"))

    def test_foot_to_meter(self):
        result = convert(1, "foot", "meter")
        self.assertEqual(result, Decimal("0.3048"))

    def test_mile_to_kilometer(self):
        result = convert(1, "mile", "km")
        self.assertEqual(result, Decimal("1.609344"))

    def test_yard_to_meter(self):
        result = convert(1, "yard", "m")
        self.assertEqual(result, Decimal("0.9144"))

    def test_same_unit(self):
        result = convert(5, "m", "m")
        self.assertEqual(result, Decimal("5"))


class TestWeightConversion(unittest.TestCase):
    """重量单位换算测试。"""

    def test_kilogram_to_gram(self):
        result = convert(1, "kg", "g")
        self.assertEqual(result, Decimal("1000"))

    def test_gram_to_milligram(self):
        result = convert(1, "gram", "milligram")
        self.assertEqual(result, Decimal("1000"))

    def test_pound_to_kilogram(self):
        result = convert(1, "pound", "kg")
        self.assertEqual(result, Decimal("0.45359237"))

    def test_ounce_to_gram(self):
        result = convert(1, "oz", "g")
        self.assertEqual(result, Decimal("28.349523125"))

    def test_metric_ton_to_kilogram(self):
        result = convert(1, "t", "kg")
        self.assertEqual(result, Decimal("1000"))

    def test_stone_to_pound(self):
        result = convert(1, "stone", "lb")
        self.assertEqual(result, Decimal("14"))


class TestTemperatureConversion(unittest.TestCase):
    """温度单位换算测试。"""

    def test_celsius_to_fahrenheit_freezing(self):
        result = convert(0, "celsius", "fahrenheit")
        self.assertEqual(result, Decimal("32"))

    def test_celsius_to_fahrenheit_boiling(self):
        result = convert(100, "c", "f")
        self.assertEqual(result, Decimal("212"))

    def test_fahrenheit_to_celsius_freezing(self):
        result = convert(32, "fahrenheit", "celsius")
        self.assertEqual(result, Decimal("0"))

    def test_fahrenheit_to_celsius_boiling(self):
        result = convert(212, "f", "c")
        self.assertEqual(result, Decimal("100"))

    def test_celsius_to_kelvin_zero(self):
        result = convert(0, "celsius", "kelvin")
        self.assertEqual(result, Decimal("273.15"))

    def test_kelvin_to_celsius_absolute_zero(self):
        result = convert(0, "kelvin", "celsius")
        self.assertEqual(result, Decimal("-273.15"))

    def test_fahrenheit_to_kelvin(self):
        result = convert(32, "fahrenheit", "kelvin")
        self.assertEqual(result, Decimal("273.15"))

    def test_kelvin_to_fahrenheit(self):
        result = convert(Decimal("273.15"), "k", "f")
        self.assertEqual(result, Decimal("32"))

    def test_same_temperature_unit(self):
        result = convert(25, "celsius", "celsius")
        self.assertEqual(result, Decimal("25"))


class TestVolumeConversion(unittest.TestCase):
    """体积单位换算测试。"""

    def test_cubic_meter_to_liter(self):
        result = convert(1, "cubic_meter", "liter")
        self.assertEqual(result, Decimal("1000"))

    def test_liter_to_milliliter(self):
        result = convert(1, "L", "mL")
        self.assertEqual(result, Decimal("1000"))

    def test_milliliter_to_cubic_centimeter(self):
        result = convert(1, "ml", "cm3")
        self.assertEqual(result, Decimal("1"))

    def test_gallon_us_to_liter(self):
        result = convert(1, "gallon_us", "liter")
        self.assertEqual(result, Decimal("3.785411784"))

    def test_gallon_uk_to_liter(self):
        result = convert(1, "gal_uk", "L")
        self.assertEqual(result, Decimal("4.54609"))

    def test_cubic_foot_to_cubic_meter(self):
        result = convert(1, "ft3", "m3")
        self.assertEqual(result, Decimal("0.028316846592"))

    def test_cubic_inch_to_cubic_centimeter(self):
        result = convert(1, "in3", "cm3")
        self.assertEqual(result, Decimal("16.387064"))


class TestTimeConversion(unittest.TestCase):
    """时间单位换算测试。"""

    def test_minute_to_second(self):
        result = convert(1, "minute", "second")
        self.assertEqual(result, Decimal("60"))

    def test_hour_to_minute(self):
        result = convert(1, "hour", "minute")
        self.assertEqual(result, Decimal("60"))

    def test_day_to_hour(self):
        result = convert(1, "day", "hour")
        self.assertEqual(result, Decimal("24"))

    def test_week_to_day(self):
        result = convert(1, "week", "day")
        self.assertEqual(result, Decimal("7"))

    def test_hour_to_second(self):
        result = convert(1, "h", "s")
        self.assertEqual(result, Decimal("3600"))

    def test_millisecond_to_second(self):
        result = convert(1000, "ms", "sec")
        self.assertEqual(result, Decimal("1"))

    def test_year_to_day(self):
        result = convert(1, "year", "day")
        self.assertEqual(result, Decimal("365.2425"))


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
        self.assertEqual(r1, r2)

    def test_weight_aliases(self):
        r1 = convert(1, "kilogram", "pound")
        r2 = convert(1, "kg", "lb")
        self.assertEqual(r1, r2)

    def test_temperature_aliases(self):
        r1 = convert(25, "celsius", "fahrenheit")
        r2 = convert(25, "c", "f")
        self.assertEqual(r1, r2)

    def test_time_aliases(self):
        r1 = convert(1, "hour", "minute")
        r2 = convert(1, "h", "min")
        self.assertEqual(r1, r2)


class TestDecimalPrecision(unittest.TestCase):
    """Decimal 精度测试 - 验证浮点数精度丢失问题已修复。"""

    def test_no_floating_point_error(self):
        """验证经典浮点数精度问题：0.1 + 0.2 != 0.3 在 float 中存在。"""
        float_result = 0.1 + 0.2
        self.assertNotEqual(float_result, 0.3)

        decimal_result = Decimal("0.1") + Decimal("0.2")
        self.assertEqual(decimal_result, Decimal("0.3"))

    def test_conversion_precision_exact(self):
        """验证换算结果是精确的 Decimal，而非近似 float。"""
        result = convert(1, "inch", "cm")
        self.assertEqual(result, Decimal("2.54"))
        self.assertIsInstance(result, Decimal)

    def test_high_precision_calculation(self):
        """验证高精度换算不丢失精度。"""
        result = convert(Decimal("0.000000001"), "km", "mm")
        self.assertEqual(result, Decimal("0.001"))

    def test_precise_division(self):
        """验证除法运算精度。"""
        result = convert(1, "yard", "mile")
        expected = Decimal("0.0005681818181818181818181818182")
        self.assertAlmostEqual(float(result), float(expected), places=20)

    def test_set_precision(self):
        """测试设置全局精度。"""
        set_precision(10)
        result = convert(1, "yard", "mile")
        self.assertEqual(len(str(result).replace(".", "").replace("-", "").lstrip("0")), 10)
        set_precision(50)


class TestDecimalPlaces(unittest.TestCase):
    """小数位控制测试。"""

    def test_decimal_places_2(self):
        result = convert(10, "meter", "foot", decimal_places=2)
        self.assertEqual(result, Decimal("32.81"))

    def test_decimal_places_4(self):
        result = convert(10, "m", "ft", decimal_places=4)
        self.assertEqual(result, Decimal("32.8084"))

    def test_decimal_places_0(self):
        result = convert(10, "meter", "foot", decimal_places=0)
        self.assertEqual(result, Decimal("33"))

    def test_no_decimal_places(self):
        """不指定 decimal_places 时返回完整精度。"""
        result = convert(1, "inch", "cm")
        self.assertEqual(result, Decimal("2.54"))

    def test_decimal_places_temperature(self):
        result = convert(25, "celsius", "fahrenheit", decimal_places=1)
        self.assertEqual(result, Decimal("77.0"))

    def test_decimal_places_rounding_half_up(self):
        """验证四舍五入（ROUND_HALF_UP）。"""
        result = convert(1, "m", "ft", decimal_places=2)
        self.assertEqual(result, Decimal("3.28"))

        result = convert(1, "m", "ft", decimal_places=3)
        self.assertEqual(result, Decimal("3.281"))

        result = convert(1, "yard", "mile", decimal_places=6)
        self.assertEqual(result, Decimal("0.000568"))

    def test_decimal_places_with_trailing_zeros(self):
        """验证保留小数位时末尾零被保留。"""
        result = convert(100, "cm", "m", decimal_places=4)
        self.assertEqual(result, Decimal("1.0000"))


class TestInputTypes(unittest.TestCase):
    """不同输入类型测试。"""

    def test_int_input(self):
        result = convert(10, "m", "cm")
        self.assertEqual(result, Decimal("1000"))

    def test_float_input(self):
        result = convert(0.5, "kg", "g")
        self.assertEqual(result, Decimal("500"))

    def test_string_input(self):
        result = convert("0.1", "km", "m")
        self.assertEqual(result, Decimal("100"))

    def test_decimal_input(self):
        result = convert(Decimal("3.14159"), "m", "cm")
        self.assertEqual(result, Decimal("314.159"))

    def test_string_input_precise(self):
        """字符串输入避免 float 精度丢失。"""
        result = convert("0.1", "m", "mm")
        self.assertEqual(result, Decimal("100"))


class TestCommonConversions(unittest.TestCase):
    """常用转换组合测试。"""

    def test_get_all_common_conversions(self):
        conversions = get_common_conversions()
        self.assertIsInstance(conversions, list)
        self.assertGreater(len(conversions), 0)
        for conv in conversions:
            self.assertIn("name", conv)
            self.assertIn("from_unit", conv)
            self.assertIn("to_unit", conv)
            self.assertIn("category", conv)
            self.assertIn("description", conv)
            self.assertIn("default_value", conv)

    def test_get_common_conversions_by_category_length(self):
        conversions = get_common_conversions("length")
        self.assertGreater(len(conversions), 0)
        for conv in conversions:
            self.assertEqual(conv["category"], "length")

    def test_get_common_conversions_by_category_weight(self):
        conversions = get_common_conversions("weight")
        self.assertGreater(len(conversions), 0)
        for conv in conversions:
            self.assertEqual(conv["category"], "weight")

    def test_get_common_conversions_by_category_temperature(self):
        conversions = get_common_conversions("temperature")
        self.assertGreater(len(conversions), 0)
        for conv in conversions:
            self.assertEqual(conv["category"], "temperature")

    def test_get_common_conversions_by_category_volume(self):
        conversions = get_common_conversions("volume")
        self.assertGreater(len(conversions), 0)
        for conv in conversions:
            self.assertEqual(conv["category"], "volume")

    def test_get_common_conversions_by_category_time(self):
        conversions = get_common_conversions("time")
        self.assertGreater(len(conversions), 0)
        for conv in conversions:
            self.assertEqual(conv["category"], "time")

    def test_get_common_conversions_unknown_category(self):
        conversions = get_common_conversions("unknown")
        self.assertEqual(conversions, [])


class TestQuickConvert(unittest.TestCase):
    """快速转换测试。"""

    def test_quick_convert_mile_to_km(self):
        result = quick_convert("英里转公里")
        self.assertEqual(result["name"], "英里转公里")
        self.assertEqual(result["from_unit"], "mile")
        self.assertEqual(result["to_unit"], "km")
        self.assertEqual(result["value"], Decimal("1"))
        self.assertEqual(result["result"], Decimal("1.609344"))
        self.assertEqual(result["category"], "length")

    def test_quick_convert_with_custom_value(self):
        result = quick_convert("英里转公里", value=5)
        self.assertEqual(result["value"], Decimal("5"))
        self.assertEqual(result["result"], Decimal("8.04672"))

    def test_quick_convert_temperature(self):
        result = quick_convert("摄氏度转华氏度")
        self.assertEqual(result["name"], "摄氏度转华氏度")
        self.assertEqual(result["value"], Decimal("25"))
        self.assertEqual(result["result"], Decimal("77"))

    def test_quick_convert_with_decimal_places(self):
        result = quick_convert("米转英尺", decimal_places=2)
        self.assertEqual(result["result"], Decimal("3.28"))

    def test_quick_convert_unknown_name(self):
        with self.assertRaises(ValueError):
            quick_convert("不存在的转换")

    def test_quick_convert_with_string_value(self):
        result = quick_convert("磅转千克", value="2.5")
        self.assertEqual(result["value"], Decimal("2.5"))
        self.assertEqual(result["result"], Decimal("1.133980925"))


class TestSearchConversions(unittest.TestCase):
    """搜索转换组合测试。"""

    def test_search_by_name(self):
        results = search_conversions("英里")
        self.assertGreater(len(results), 0)
        for conv in results:
            self.assertTrue("英里" in conv["name"])

    def test_search_by_unit(self):
        results = search_conversions("mile")
        self.assertGreater(len(results), 0)

    def test_search_by_description(self):
        results = search_conversions("1 英里")
        self.assertGreater(len(results), 0)

    def test_search_no_results(self):
        results = search_conversions("不存在的关键词xyz")
        self.assertEqual(results, [])

    def test_search_case_insensitive(self):
        results1 = search_conversions("MILE")
        results2 = search_conversions("mile")
        self.assertEqual(len(results1), len(results2))


if __name__ == "__main__":
    unittest.main()
