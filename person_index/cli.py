#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from person_index import PersonIndex
from pprint import pprint

def cmd_lookup(idx, args):
    name = args.name
    # 尝试 canonical
    if name in idx.data:
        print(f"[canonical] {name}")
        pprint(idx.data[name], width=100)
        return

    # 尝试 aliases / reference_names
    from cli_utils import lookup_name
    canonical = lookup_name(idx, name)
    if canonical:
        print(f"[resolved] {name}  →  {canonical}")
        pprint(idx.data[canonical], width=100)
    else:
        print(f"未找到：{name}")


def cmd_search(idx, args):
    text = args.text
    from cli_utils import search_people
    result = search_people(idx, text)
    if not result:
        print("沒有搜尋結果")
    else:
        for r in result:
            print(r)


def cmd_appear(idx, args):
    name = args.name
    if name not in idx.data:
        print("找不到此人")
        return
    from cli_utils import get_appearances
    app = get_appearances(idx, name)
    pprint(app, width=100)


def cmd_reverse(idx, args):
    section = args.section
    entry = args.entry
    from cli_utils import find_people_in_entry
    result = find_people_in_entry(idx, section, entry)
    if not result:
        print("無人出現於此條目")
    else:
        for r in result:
            print(r)


def main():
    parser = argparse.ArgumentParser(description="世說新語 人名索引 CLI 查詢工具")
    parser.add_argument("--json", default="canonical_to_aliases.json",
                        help="索引 JSON 檔案位置（預設：canonical_to_aliases.json）")

    subparsers = parser.add_subparsers(dest="command")

    # lookup
    p_lookup = subparsers.add_parser("lookup", help="查某人（可用別稱或見××的名字）")
    p_lookup.add_argument("name")
    p_lookup.set_defaults(func=cmd_lookup)

    # search
    p_search = subparsers.add_parser("search", help="模糊搜尋（子串匹配）")
    p_search.add_argument("text")
    p_search.set_defaults(func=cmd_search)

    # appearances
    p_app = subparsers.add_parser("appear", help="查某人在哪些篇目出現")
    p_app.add_argument("name")
    p_app.set_defaults(func=cmd_appear)

    # reverse index
    p_rev = subparsers.add_parser("reverse", help="查某篇目某條目裡有誰")
    p_rev.add_argument("section")
    p_rev.add_argument("entry", type=int)
    p_rev.set_defaults(func=cmd_reverse)

    args = parser.parse_args()

    idx = PersonIndex(args.json, conflict_mode="warn")

    if not args.command:
        parser.print_help()
        return
    args.func(idx, args)


if __name__ == "__main__":
    main()