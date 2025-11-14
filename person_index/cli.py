#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
世說新語 人名索引 CLI 查詢工具
使用方法
查人（自动处理别称、反向名）
python cli.py lookup 阿龍

模糊搜索
python cli.py search 王

查某人在哪些篇目出现
python cli.py appear 王衍

查某篇目某条目里有谁
python cli.py reverse 德行 5
'''

import argparse
from person_index import PersonIndex
from pprint import pprint
import json
from cli_utils import (
    lookup_name, search_people, get_appearances, find_people_in_entry,
    load_entries_jsonl
)

ENTRIES = load_entries_jsonl("entries.jsonl")

def cmd_lookup(idx, args):
    name = args.name
    canonical = name

    # 先尝试 canonical
    if name not in idx.data:
        canonical = lookup_name(idx, name)
        if not canonical:
            print(f"未找到：{name}")
            return
        print(f"[resolved] {name} → {canonical}")
    else:
        print(f"[canonical] {canonical}")

    person = idx.data[canonical]
    pprint(person, width=100)

    # 是否导出？
    print("\n是否要导出该人物的所有出场原文？")
    print("y = txt, m = markdown, h = html, 其他 = 取消")
    choice = input("> ").strip().lower()

    if not choice:
        return

    apps = person.get("appearances", {})
    entries = []

    for section, ids in apps.items():
        for eid in ids:
            key = (section, eid)
            if key in ENTRIES:
                entries.append((section, eid, ENTRIES[key]))

    if not entries:
        print("此人无可导出的条目。")
        return

    if choice == "y":
        export_person_txt(canonical, entries)
    elif choice == "m":
        export_person_markdown(canonical, entries)
    elif choice == "h":
        export_person_html(canonical, entries)
    else:
        print("取消导出。")


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
            

def cmd_text(idx, args):
    key = (args.section, args.index)
    if key not in ENTRIES:
        print("找不到對應條目")
        return
    print(ENTRIES[key])
    
    
def export_person_txt(canonical, entries):
    filename = f"{canonical}_entries.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for section, eid, text in entries:
            f.write(f"{section} {eid}\n{text}\n\n")
    print(f"已导出：{filename}")


def export_person_markdown(canonical, entries):
    filename = f"{canonical}_entries.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {canonical} 出場條目\n\n")
        for section, eid, text in entries:
            f.write(f"## {section} {eid}\n")
            f.write(f"> {text}\n\n")
    print(f"已导出：{filename}")


def export_person_html(canonical, entries):
    filename = f"{canonical}_entries.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"<h1>{canonical} 出場條目</h1>\n")
        for section, eid, text in entries:
            f.write(f"<h3>{section} {eid}</h3>\n")
            f.write(f"<blockquote>{text}</blockquote>\n")
    print(f"已导出：{filename}")


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
    
    # text
    p_text = subparsers.add_parser("text", help="輸出某篇某條的原文")
    p_text.add_argument("section")
    p_text.add_argument("index", type=int)
    p_text.set_defaults(func=cmd_text)

    args = parser.parse_args()

    idx = PersonIndex(args.json, conflict_mode="warn")

    if not args.command:
        parser.print_help()
        return
    args.func(idx, args)


if __name__ == "__main__":
    main()