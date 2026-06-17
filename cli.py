"""单位换算命令行接口。"""

import argparse
import sys

from converter import convert, get_supported_units, get_categories, get_common_conversions, quick_convert, search_conversions


def main():
    parser = argparse.ArgumentParser(description="单位换算服务 - 支持长度、重量、温度、体积、时间换算")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    convert_parser = subparsers.add_parser("convert", help="执行单位换算")
    convert_parser.add_argument("value", help="要转换的数值")
    convert_parser.add_argument("from_unit", help="源单位")
    convert_parser.add_argument("to_unit", help="目标单位")
    convert_parser.add_argument(
        "-d", "--decimal-places",
        type=int,
        default=None,
        help="保留的小数位数，默认不四舍五入",
    )

    subparsers.add_parser("units", help="列出所有支持的单位")

    units_parser = subparsers.add_parser("units-by-category", help="按类别列出支持的单位")
    units_parser.add_argument("category", help="类别名称 (length, weight, volume, time, temperature)")

    subparsers.add_parser("categories", help="列出所有支持的类别")

    common_parser = subparsers.add_parser("common", help="列出常用转换组合")
    common_parser.add_argument("-c", "--category", default=None, help="按类别过滤")

    quick_parser = subparsers.add_parser("quick", help="快速执行常用转换")
    quick_parser.add_argument("name", help="转换名称（如 '英里转公里'）")
    quick_parser.add_argument("-v", "--value", default=None, help="自定义数值，不填则使用默认值")
    quick_parser.add_argument(
        "-d", "--decimal-places",
        type=int,
        default=None,
        help="保留的小数位数，默认不四舍五入",
    )

    search_parser = subparsers.add_parser("search", help="搜索常用转换组合")
    search_parser.add_argument("keyword", help="搜索关键词")

    args = parser.parse_args()

    if args.command == "convert":
        try:
            result = convert(args.value, args.from_unit, args.to_unit, decimal_places=args.decimal_places)
            print(f"{args.value} {args.from_unit} = {result} {args.to_unit}")
        except ValueError as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "units":
        units = get_supported_units()
        for category, unit_list in units.items():
            print(f"\n{category}:")
            print(f"  {', '.join(unit_list[:10])}..." if len(unit_list) > 10 else f"  {', '.join(unit_list)}")

    elif args.command == "units-by-category":
        try:
            units = get_supported_units(args.category)
            for category, unit_list in units.items():
                print(f"\n{category}:")
                print(f"  {', '.join(unit_list)}")
        except ValueError as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "categories":
        categories = get_categories()
        print("支持的类别:")
        for cat in categories:
            print(f"  - {cat}")

    elif args.command == "common":
        conversions = get_common_conversions(args.category)
        category_label = f"（{args.category}）" if args.category else ""
        print(f"常用转换组合{category_label}:")
        for i, conv in enumerate(conversions, 1):
            print(f"  {i:2d}. {conv['name']}: {conv['description']}")

    elif args.command == "quick":
        try:
            result = quick_convert(args.name, value=args.value, decimal_places=args.decimal_places)
            print(f"{result['name']}:")
            print(f"  {result['value']} {result['from_unit']} = {result['result']} {result['to_unit']}")
        except ValueError as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "search":
        results = search_conversions(args.keyword)
        if results:
            print(f"找到 {len(results)} 个匹配的转换组合:")
            for i, conv in enumerate(results, 1):
                print(f"  {i:2d}. {conv['name']}: {conv['description']}")
        else:
            print(f"未找到包含 '{args.keyword}' 的转换组合")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
