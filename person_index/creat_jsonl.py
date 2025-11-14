#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
import re

TEXT_DIR = Path("text")
OUT_FILE = Path("entries.jsonl")

section_pattern = re.compile(r"^\d+\s*(.*)\.txt$")

def main():
    with OUT_FILE.open("w", encoding="utf-8") as out:
        for file in sorted(TEXT_DIR.iterdir()):
            if not file.suffix.lower() == ".txt":
                continue

            # 解析篇名
            m = section_pattern.match(file.name)
            if not m:
                print("无法解析篇名：", file.name)
                continue
            section = m.group(1)

            # 读文件
            with file.open("r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines()]

            # 去掉空行
            lines = [l for l in lines if l.strip()]

            # 写入 jsonl
            for idx, text in enumerate(lines, 1):
                obj = {
                    "section": section,
                    "index": idx,
                    "text": text
                }
                out.write(json.dumps(obj, ensure_ascii=False) + "\n")

    print("已生成 entries.jsonl")

if __name__ == "__main__":
    main()