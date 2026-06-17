"""单位换算服务模块，支持长度、重量、温度、体积、时间等单位互转。

使用 Decimal 进行高精度计算，避免浮点数精度丢失问题。
"""

from decimal import Decimal, getcontext, ROUND_HALF_UP
from typing import Dict, List, Optional, Union


getcontext().prec = 50

Number = Union[float, int, str, Decimal]


def _to_decimal(value: Number) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


_LENGTH_UNITS: Dict[str, Decimal] = {
    "meter": Decimal("1"),
    "m": Decimal("1"),
    "kilometer": Decimal("1000"),
    "km": Decimal("1000"),
    "centimeter": Decimal("0.01"),
    "cm": Decimal("0.01"),
    "millimeter": Decimal("0.001"),
    "mm": Decimal("0.001"),
    "micrometer": Decimal("0.000001"),
    "um": Decimal("0.000001"),
    "nanometer": Decimal("0.000000001"),
    "nm": Decimal("0.000000001"),
    "mile": Decimal("1609.344"),
    "mi": Decimal("1609.344"),
    "yard": Decimal("0.9144"),
    "yd": Decimal("0.9144"),
    "foot": Decimal("0.3048"),
    "ft": Decimal("0.3048"),
    "inch": Decimal("0.0254"),
    "in": Decimal("0.0254"),
    "nautical_mile": Decimal("1852"),
    "nmi": Decimal("1852"),
    "furlong": Decimal("201.168"),
    "fur": Decimal("201.168"),
    "chain": Decimal("20.1168"),
    "ch": Decimal("20.1168"),
    "rod": Decimal("5.0292"),
    "rd": Decimal("5.0292"),
    "fathom": Decimal("1.8288"),
    "ftm": Decimal("1.8288"),
}

_WEIGHT_UNITS: Dict[str, Decimal] = {
    "kilogram": Decimal("1"),
    "kg": Decimal("1"),
    "gram": Decimal("0.001"),
    "g": Decimal("0.001"),
    "milligram": Decimal("0.000001"),
    "mg": Decimal("0.000001"),
    "microgram": Decimal("0.000000001"),
    "ug": Decimal("0.000000001"),
    "metric_ton": Decimal("1000"),
    "t": Decimal("1000"),
    "pound": Decimal("0.45359237"),
    "lb": Decimal("0.45359237"),
    "ounce": Decimal("0.028349523125"),
    "oz": Decimal("0.028349523125"),
    "stone": Decimal("6.35029318"),
    "st": Decimal("6.35029318"),
    "ton_us": Decimal("907.18474"),
    "short_ton": Decimal("907.18474"),
    "ton_uk": Decimal("1016.0469088"),
    "long_ton": Decimal("1016.0469088"),
    "carat": Decimal("0.0002"),
    "ct": Decimal("0.0002"),
}

_VOLUME_UNITS: Dict[str, Decimal] = {
    "cubic_meter": Decimal("1"),
    "m3": Decimal("1"),
    "liter": Decimal("0.001"),
    "L": Decimal("0.001"),
    "l": Decimal("0.001"),
    "milliliter": Decimal("0.000001"),
    "mL": Decimal("0.000001"),
    "ml": Decimal("0.000001"),
    "cubic_centimeter": Decimal("0.000001"),
    "cm3": Decimal("0.000001"),
    "cc": Decimal("0.000001"),
    "cubic_millimeter": Decimal("0.000000001"),
    "mm3": Decimal("0.000000001"),
    "cubic_kilometer": Decimal("1000000000"),
    "km3": Decimal("1000000000"),
    "gallon_us": Decimal("0.003785411784"),
    "gal_us": Decimal("0.003785411784"),
    "gallon_uk": Decimal("0.00454609"),
    "gal_uk": Decimal("0.00454609"),
    "quart_us": Decimal("0.000946352946"),
    "qt_us": Decimal("0.000946352946"),
    "pint_us": Decimal("0.000473176473"),
    "pt_us": Decimal("0.000473176473"),
    "cup_us": Decimal("0.0002365882365"),
    "fluid_ounce_us": Decimal("0.0000295735295625"),
    "fl_oz_us": Decimal("0.0000295735295625"),
    "tablespoon_us": Decimal("0.00001478676478125"),
    "tbsp_us": Decimal("0.00001478676478125"),
    "teaspoon_us": Decimal("0.00000492892159375"),
    "tsp_us": Decimal("0.00000492892159375"),
    "cubic_foot": Decimal("0.028316846592"),
    "ft3": Decimal("0.028316846592"),
    "cubic_inch": Decimal("0.000016387064"),
    "in3": Decimal("0.000016387064"),
    "cubic_yard": Decimal("0.764554857984"),
    "yd3": Decimal("0.764554857984"),
}

_TIME_UNITS: Dict[str, Decimal] = {
    "second": Decimal("1"),
    "s": Decimal("1"),
    "sec": Decimal("1"),
    "millisecond": Decimal("0.001"),
    "ms": Decimal("0.001"),
    "microsecond": Decimal("0.000001"),
    "us": Decimal("0.000001"),
    "nanosecond": Decimal("0.000000001"),
    "ns": Decimal("0.000000001"),
    "minute": Decimal("60"),
    "min": Decimal("60"),
    "hour": Decimal("3600"),
    "h": Decimal("3600"),
    "hr": Decimal("3600"),
    "day": Decimal("86400"),
    "d": Decimal("86400"),
    "week": Decimal("604800"),
    "wk": Decimal("604800"),
    "month": Decimal("2629746"),
    "mo": Decimal("2629746"),
    "year": Decimal("31556952"),
    "yr": Decimal("31556952"),
    "decade": Decimal("315569520"),
    "century": Decimal("3155695200"),
    "millennium": Decimal("31556952000"),
}

_CATEGORIES: Dict[str, Dict[str, Decimal]] = {
    "length": _LENGTH_UNITS,
    "weight": _WEIGHT_UNITS,
    "mass": _WEIGHT_UNITS,
    "volume": _VOLUME_UNITS,
    "time": _TIME_UNITS,
}

_CATEGORY_NAMES = {
    "length": "长度",
    "weight": "重量",
    "mass": "重量",
    "volume": "体积",
    "time": "时间",
    "temperature": "温度",
}


def _celsius_to_fahrenheit(c: Decimal) -> Decimal:
    return c * Decimal("9") / Decimal("5") + Decimal("32")


def _fahrenheit_to_celsius(f: Decimal) -> Decimal:
    return (f - Decimal("32")) * Decimal("5") / Decimal("9")


def _celsius_to_kelvin(c: Decimal) -> Decimal:
    return c + Decimal("273.15")


def _kelvin_to_celsius(k: Decimal) -> Decimal:
    return k - Decimal("273.15")


def _fahrenheit_to_kelvin(f: Decimal) -> Decimal:
    return _celsius_to_kelvin(_fahrenheit_to_celsius(f))


def _kelvin_to_fahrenheit(k: Decimal) -> Decimal:
    return _celsius_to_fahrenheit(_kelvin_to_celsius(k))


_TEMPERATURE_CONVERTERS = {
    ("celsius", "fahrenheit"): _celsius_to_fahrenheit,
    ("fahrenheit", "celsius"): _fahrenheit_to_celsius,
    ("celsius", "kelvin"): _celsius_to_kelvin,
    ("kelvin", "celsius"): _kelvin_to_celsius,
    ("fahrenheit", "kelvin"): _fahrenheit_to_kelvin,
    ("kelvin", "fahrenheit"): _kelvin_to_fahrenheit,
    ("celsius", "celsius"): lambda x: x,
    ("fahrenheit", "fahrenheit"): lambda x: x,
    ("kelvin", "kelvin"): lambda x: x,
}

_TEMPERATURE_ALIASES = {
    "celsius": "celsius",
    "centigrade": "celsius",
    "c": "celsius",
    "°c": "celsius",
    "fahrenheit": "fahrenheit",
    "f": "fahrenheit",
    "°f": "fahrenheit",
    "kelvin": "kelvin",
    "k": "kelvin",
    "°k": "kelvin",
}


def _normalize_unit(unit: str) -> str:
    return unit.strip().lower()


def _find_category(unit: str) -> str:
    unit_norm = _normalize_unit(unit)
    for category, units in _CATEGORIES.items():
        if unit_norm in units:
            return category
    if unit_norm in _TEMPERATURE_ALIASES:
        return "temperature"
    raise ValueError(f"未知单位: {unit}")


def _get_temperature_unit(unit: str) -> str:
    unit_norm = _normalize_unit(unit)
    if unit_norm not in _TEMPERATURE_ALIASES:
        raise ValueError(f"未知温度单位: {unit}")
    return _TEMPERATURE_ALIASES[unit_norm]


def _round_decimal(value: Decimal, decimal_places: Optional[int]) -> Decimal:
    if decimal_places is None:
        return value
    quantize_str = "0." + "0" * decimal_places if decimal_places > 0 else "0"
    return value.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)


def convert(
    value: Number,
    from_unit: str,
    to_unit: str,
    decimal_places: Optional[int] = None,
) -> Decimal:
    """
    将数值从一个单位转换为另一个单位。

    使用 Decimal 进行高精度计算，避免浮点数精度丢失。

    Args:
        value: 要转换的数值（支持 float、int、str、Decimal）
        from_unit: 源单位
        to_unit: 目标单位
        decimal_places: 可选，保留的小数位数，None 表示不四舍五入

    Returns:
        转换后的 Decimal 数值

    Raises:
        ValueError: 如果单位未知或单位类型不匹配
    """
    value_dec = _to_decimal(value)

    from_category = _find_category(from_unit)
    to_category = _find_category(to_unit)

    if from_category != to_category:
        raise ValueError(
            f"单位类型不匹配: {from_unit} 属于 {_CATEGORY_NAMES.get(from_category, from_category)}, "
            f"{to_unit} 属于 {_CATEGORY_NAMES.get(to_category, to_category)}"
        )

    if from_category == "temperature":
        from_temp = _get_temperature_unit(from_unit)
        to_temp = _get_temperature_unit(to_unit)
        converter = _TEMPERATURE_CONVERTERS[(from_temp, to_temp)]
        result = converter(value_dec)
    else:
        units = _CATEGORIES[from_category]
        from_norm = _normalize_unit(from_unit)
        to_norm = _normalize_unit(to_unit)
        base_value = value_dec * units[from_norm]
        result = base_value / units[to_norm]

    return _round_decimal(result, decimal_places)


def get_supported_units(category: str = None) -> Dict[str, list]:
    """
    获取支持的单位列表。

    Args:
        category: 可选，指定类别（length, weight, volume, time, temperature）

    Returns:
        按类别组织的单位列表字典
    """
    if category:
        cat_norm = _normalize_unit(category)
        if cat_norm == "temperature":
            return {"temperature": list(_TEMPERATURE_ALIASES.keys())}
        if cat_norm in _CATEGORIES:
            return {cat_norm: list(_CATEGORIES[cat_norm].keys())}
        raise ValueError(f"未知类别: {category}")

    result = {}
    for cat, units in _CATEGORIES.items():
        if cat not in result:
            result[cat] = list(units.keys())
    result["temperature"] = list(_TEMPERATURE_ALIASES.keys())
    return result


def get_categories() -> list:
    """获取所有支持的类别列表。"""
    return list(_CATEGORY_NAMES.keys())


def set_precision(prec: int) -> None:
    """
    设置 Decimal 全局计算精度。

    Args:
        prec: 有效数字位数
    """
    getcontext().prec = prec


_COMMON_CONVERSIONS: List[Dict] = [
    {
        "category": "length",
        "name": "英里转公里",
        "from_unit": "mile",
        "to_unit": "km",
        "default_value": 1,
        "description": "1 英里 = 1.609344 公里",
    },
    {
        "category": "length",
        "name": "公里转英里",
        "from_unit": "km",
        "to_unit": "mile",
        "default_value": 1,
        "description": "1 公里 ≈ 0.621371 英里",
    },
    {
        "category": "length",
        "name": "英尺转米",
        "from_unit": "foot",
        "to_unit": "meter",
        "default_value": 1,
        "description": "1 英尺 = 0.3048 米",
    },
    {
        "category": "length",
        "name": "米转英尺",
        "from_unit": "meter",
        "to_unit": "foot",
        "default_value": 1,
        "description": "1 米 ≈ 3.28084 英尺",
    },
    {
        "category": "length",
        "name": "英寸转厘米",
        "from_unit": "inch",
        "to_unit": "cm",
        "default_value": 1,
        "description": "1 英寸 = 2.54 厘米",
    },
    {
        "category": "length",
        "name": "厘米转英寸",
        "from_unit": "cm",
        "to_unit": "inch",
        "default_value": 1,
        "description": "1 厘米 ≈ 0.393701 英寸",
    },
    {
        "category": "length",
        "name": "码转米",
        "from_unit": "yard",
        "to_unit": "m",
        "default_value": 1,
        "description": "1 码 = 0.9144 米",
    },
    {
        "category": "weight",
        "name": "磅转千克",
        "from_unit": "pound",
        "to_unit": "kg",
        "default_value": 1,
        "description": "1 磅 ≈ 0.453592 千克",
    },
    {
        "category": "weight",
        "name": "千克转磅",
        "from_unit": "kg",
        "to_unit": "pound",
        "default_value": 1,
        "description": "1 千克 ≈ 2.20462 磅",
    },
    {
        "category": "weight",
        "name": "盎司转克",
        "from_unit": "ounce",
        "to_unit": "g",
        "default_value": 1,
        "description": "1 盎司 ≈ 28.3495 克",
    },
    {
        "category": "weight",
        "name": "克转盎司",
        "from_unit": "g",
        "to_unit": "ounce",
        "default_value": 1,
        "description": "1 克 ≈ 0.035274 盎司",
    },
    {
        "category": "weight",
        "name": "英石转磅",
        "from_unit": "stone",
        "to_unit": "lb",
        "default_value": 1,
        "description": "1 英石 = 14 磅",
    },
    {
        "category": "temperature",
        "name": "摄氏度转华氏度",
        "from_unit": "celsius",
        "to_unit": "fahrenheit",
        "default_value": 25,
        "description": "25°C = 77°F",
    },
    {
        "category": "temperature",
        "name": "华氏度转摄氏度",
        "from_unit": "fahrenheit",
        "to_unit": "celsius",
        "default_value": 77,
        "description": "77°F = 25°C",
    },
    {
        "category": "temperature",
        "name": "摄氏度转开尔文",
        "from_unit": "celsius",
        "to_unit": "kelvin",
        "default_value": 0,
        "description": "0°C = 273.15 K",
    },
    {
        "category": "temperature",
        "name": "开尔文转摄氏度",
        "from_unit": "kelvin",
        "to_unit": "celsius",
        "default_value": 273.15,
        "description": "273.15 K = 0°C",
    },
    {
        "category": "volume",
        "name": "美制加仑转升",
        "from_unit": "gallon_us",
        "to_unit": "liter",
        "default_value": 1,
        "description": "1 美制加仑 ≈ 3.78541 升",
    },
    {
        "category": "volume",
        "name": "升转美制加仑",
        "from_unit": "liter",
        "to_unit": "gallon_us",
        "default_value": 1,
        "description": "1 升 ≈ 0.264172 美制加仑",
    },
    {
        "category": "volume",
        "name": "英制加仑转升",
        "from_unit": "gallon_uk",
        "to_unit": "L",
        "default_value": 1,
        "description": "1 英制加仑 ≈ 4.54609 升",
    },
    {
        "category": "volume",
        "name": "升转毫升",
        "from_unit": "L",
        "to_unit": "mL",
        "default_value": 1,
        "description": "1 升 = 1000 毫升",
    },
    {
        "category": "volume",
        "name": "立方英尺转立方米",
        "from_unit": "ft3",
        "to_unit": "m3",
        "default_value": 1,
        "description": "1 立方英尺 ≈ 0.0283168 立方米",
    },
    {
        "category": "time",
        "name": "小时转秒",
        "from_unit": "hour",
        "to_unit": "second",
        "default_value": 1,
        "description": "1 小时 = 3600 秒",
    },
    {
        "category": "time",
        "name": "天转小时",
        "from_unit": "day",
        "to_unit": "hour",
        "default_value": 1,
        "description": "1 天 = 24 小时",
    },
    {
        "category": "time",
        "name": "周转天",
        "from_unit": "week",
        "to_unit": "day",
        "default_value": 1,
        "description": "1 周 = 7 天",
    },
    {
        "category": "time",
        "name": "年转天",
        "from_unit": "year",
        "to_unit": "day",
        "default_value": 1,
        "description": "1 年 ≈ 365.2425 天",
    },
    {
        "category": "length",
        "name": "海里转公里",
        "from_unit": "nautical_mile",
        "to_unit": "km",
        "default_value": 1,
        "description": "1 海里 = 1.852 公里",
    },
    {
        "category": "weight",
        "name": "吨转千克",
        "from_unit": "t",
        "to_unit": "kg",
        "default_value": 1,
        "description": "1 吨 = 1000 千克",
    },
    {
        "category": "length",
        "name": "公里转米",
        "from_unit": "km",
        "to_unit": "m",
        "default_value": 1,
        "description": "1 公里 = 1000 米",
    },
    {
        "category": "length",
        "name": "米转厘米",
        "from_unit": "m",
        "to_unit": "cm",
        "default_value": 1,
        "description": "1 米 = 100 厘米",
    },
    {
        "category": "weight",
        "name": "千克转克",
        "from_unit": "kg",
        "to_unit": "g",
        "default_value": 1,
        "description": "1 千克 = 1000 克",
    },
]


def get_common_conversions(category: str = None) -> List[Dict]:
    """
    获取常用转换组合列表。

    Args:
        category: 可选，按类别过滤（length, weight, volume, time, temperature）

    Returns:
        常用转换组合列表，每个元素包含 name、from_unit、to_unit、default_value、description 等信息
    """
    if category:
        cat_norm = _normalize_unit(category)
        return [conv for conv in _COMMON_CONVERSIONS if conv["category"] == cat_norm]
    return list(_COMMON_CONVERSIONS)


def quick_convert(
    conversion_name: str,
    value: Number = None,
    decimal_places: Optional[int] = None,
) -> Dict:
    """
    通过转换名称快速执行常用转换。

    Args:
        conversion_name: 转换名称（如 "英里转公里"、"摄氏度转华氏度"）
        value: 可选，自定义数值。不填则使用默认值
        decimal_places: 可选，保留的小数位数

    Returns:
        包含转换信息的字典：name、from_unit、to_unit、value、result、description

    Raises:
        ValueError: 如果找不到对应的转换名称
    """
    for conv in _COMMON_CONVERSIONS:
        if conv["name"] == conversion_name:
            val = value if value is not None else conv["default_value"]
            result = convert(val, conv["from_unit"], conv["to_unit"], decimal_places=decimal_places)
            return {
                "name": conv["name"],
                "from_unit": conv["from_unit"],
                "to_unit": conv["to_unit"],
                "value": _to_decimal(val),
                "result": result,
                "description": conv["description"],
                "category": conv["category"],
            }
    raise ValueError(f"未找到常用转换: {conversion_name}")


def search_conversions(keyword: str) -> List[Dict]:
    """
    按关键词搜索常用转换组合。

    Args:
        keyword: 搜索关键词

    Returns:
        匹配的转换组合列表
    """
    keyword_norm = keyword.strip().lower()
    results = []
    for conv in _COMMON_CONVERSIONS:
        if (
            keyword_norm in conv["name"].lower()
            or keyword_norm in conv["from_unit"].lower()
            or keyword_norm in conv["to_unit"].lower()
            or keyword_norm in conv["description"].lower()
        ):
            results.append(conv)
    return results
