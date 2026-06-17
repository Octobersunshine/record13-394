"""单位换算服务模块，支持长度、重量、温度、体积、时间等单位互转。"""

from typing import Dict, Tuple


_LENGTH_UNITS: Dict[str, float] = {
    "meter": 1.0,
    "m": 1.0,
    "kilometer": 1000.0,
    "km": 1000.0,
    "centimeter": 0.01,
    "cm": 0.01,
    "millimeter": 0.001,
    "mm": 0.001,
    "micrometer": 1e-6,
    "um": 1e-6,
    "nanometer": 1e-9,
    "nm": 1e-9,
    "mile": 1609.344,
    "mi": 1609.344,
    "yard": 0.9144,
    "yd": 0.9144,
    "foot": 0.3048,
    "ft": 0.3048,
    "inch": 0.0254,
    "in": 0.0254,
    "nautical_mile": 1852.0,
    "nmi": 1852.0,
    "furlong": 201.168,
    "fur": 201.168,
    "chain": 20.1168,
    "ch": 20.1168,
    "rod": 5.0292,
    "rd": 5.0292,
    "fathom": 1.8288,
    "ftm": 1.8288,
}

_WEIGHT_UNITS: Dict[str, float] = {
    "kilogram": 1.0,
    "kg": 1.0,
    "gram": 0.001,
    "g": 0.001,
    "milligram": 1e-6,
    "mg": 1e-6,
    "microgram": 1e-9,
    "ug": 1e-9,
    "metric_ton": 1000.0,
    "t": 1000.0,
    "pound": 0.45359237,
    "lb": 0.45359237,
    "ounce": 0.028349523125,
    "oz": 0.028349523125,
    "stone": 6.35029318,
    "st": 6.35029318,
    "ton_us": 907.18474,
    "short_ton": 907.18474,
    "ton_uk": 1016.0469088,
    "long_ton": 1016.0469088,
    "carat": 0.0002,
    "ct": 0.0002,
}

_VOLUME_UNITS: Dict[str, float] = {
    "cubic_meter": 1.0,
    "m3": 1.0,
    "liter": 0.001,
    "L": 0.001,
    "l": 0.001,
    "milliliter": 1e-6,
    "mL": 1e-6,
    "ml": 1e-6,
    "cubic_centimeter": 1e-6,
    "cm3": 1e-6,
    "cc": 1e-6,
    "cubic_millimeter": 1e-9,
    "mm3": 1e-9,
    "cubic_kilometer": 1e9,
    "km3": 1e9,
    "gallon_us": 0.003785411784,
    "gal_us": 0.003785411784,
    "gallon_uk": 0.00454609,
    "gal_uk": 0.00454609,
    "quart_us": 0.000946352946,
    "qt_us": 0.000946352946,
    "pint_us": 0.000473176473,
    "pt_us": 0.000473176473,
    "cup_us": 0.0002365882365,
    "fluid_ounce_us": 2.95735295625e-5,
    "fl_oz_us": 2.95735295625e-5,
    "tablespoon_us": 1.478676478125e-5,
    "tbsp_us": 1.478676478125e-5,
    "teaspoon_us": 4.92892159375e-6,
    "tsp_us": 4.92892159375e-6,
    "cubic_foot": 0.028316846592,
    "ft3": 0.028316846592,
    "cubic_inch": 1.6387064e-5,
    "in3": 1.6387064e-5,
    "cubic_yard": 0.764554857984,
    "yd3": 0.764554857984,
}

_TIME_UNITS: Dict[str, float] = {
    "second": 1.0,
    "s": 1.0,
    "sec": 1.0,
    "millisecond": 0.001,
    "ms": 0.001,
    "microsecond": 1e-6,
    "us": 1e-6,
    "nanosecond": 1e-9,
    "ns": 1e-9,
    "minute": 60.0,
    "min": 60.0,
    "hour": 3600.0,
    "h": 3600.0,
    "hr": 3600.0,
    "day": 86400.0,
    "d": 86400.0,
    "week": 604800.0,
    "wk": 604800.0,
    "month": 2629746.0,
    "mo": 2629746.0,
    "year": 31556952.0,
    "yr": 31556952.0,
    "decade": 315569520.0,
    "century": 3155695200.0,
    "millennium": 31556952000.0,
}

_CATEGORIES: Dict[str, Dict[str, float]] = {
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


def _celsius_to_fahrenheit(c: float) -> float:
    return c * 9 / 5 + 32


def _fahrenheit_to_celsius(f: float) -> float:
    return (f - 32) * 5 / 9


def _celsius_to_kelvin(c: float) -> float:
    return c + 273.15


def _kelvin_to_celsius(k: float) -> float:
    return k - 273.15


def _fahrenheit_to_kelvin(f: float) -> float:
    return _celsius_to_kelvin(_fahrenheit_to_celsius(f))


def _kelvin_to_fahrenheit(k: float) -> float:
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


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """
    将数值从一个单位转换为另一个单位。

    Args:
        value: 要转换的数值
        from_unit: 源单位
        to_unit: 目标单位

    Returns:
        转换后的数值

    Raises:
        ValueError: 如果单位未知或单位类型不匹配
    """
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
        return converter(value)

    units = _CATEGORIES[from_category]
    from_norm = _normalize_unit(from_unit)
    to_norm = _normalize_unit(to_unit)

    base_value = value * units[from_norm]
    result = base_value / units[to_norm]
    return result


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
