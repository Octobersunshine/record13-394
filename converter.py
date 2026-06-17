"""单位换算服务模块，支持长度、重量、温度、体积、时间等单位互转。

使用 Decimal 进行高精度计算，避免浮点数精度丢失问题。
"""

from decimal import Decimal, getcontext, ROUND_HALF_UP
from typing import Dict, Optional, Union


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
