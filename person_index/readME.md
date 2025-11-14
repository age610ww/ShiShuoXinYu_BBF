世說新語人物索引工具（PersonIndex + CLI）

本工具用于：
1. 将《世說新語》36 门类的文本整理为 entries.jsonl（每条原文一行）。
2. 将扫描索引页逐页解析为结构化的 canonical_to_aliases.json。
3. 通过命令行（CLI）提供查询人物、搜索人物、反查条目、导出全文等功能。
4. 为研究使用提供 TXT / Markdown / HTML 格式的自动化原文导出。


⸻

# 1. 文件结构

建议项目结构如下：

```
project/
│
├── person_index.py                # 处理人名索引（别名、反向别名、出场信息）
├── cli.py                          # 命令行查询工具
├── cli_utils.py                    # 查询辅助函数
├── make_entries_jsonl.py           # 将36篇 txt 合并成 jsonl
│
├── canonical_to_aliases.json       # 人物索引数据库（运行过程中维护）
├── entries.jsonl                   # 原文数据库（自动生成）
│
└── texts/                          # 存放36个 txt 原文
       01德行.txt
       02言語.txt
       ...
```

⸻

# 2. PersonIndex

person_index.py 提供：
	•	新建人物条目
	•	补充别称（aliases）
	•	补充“見 ××”反向名称（reference_names）
	•	补充人物出场篇名与条目号
	•	冲突检测（重复别称、反向名冲突、非法篇名）
	•	完整性检查（assert_integrity）
	•	保存 JSON 数据文件

使用示例

```
from person_index import PersonIndex

idx = PersonIndex("canonical_to_aliases.json")

idx.add_canonical(
    "王導",
    aliases=["茂弘","丞相","阿龍"],
    appearances={"德行":[27,29], "言語":[31,33]}
)

idx.add_reference("阿龍", "王導")

idx.save()
```


⸻

# 3. 构建 entries.jsonl

将 36 个 txt 格式的原文合并成可查询的 jsonl 文件。

运行：

`python3 make_entries_jsonl.py`

生成文件：

`entries.jsonl`

格式示例：

```
{"section": "德行", "index": 1, "text": "……"}
{"section": "德行", "index": 2, "text": "……"}
{"section": "言語", "index": 1, "text": "……"}
...
```

查询 CLI 将依赖此文件返回原文段落。

⸻

# 4. CLI 使用说明

执行：

`python3 cli.py [command] [参数...]`

CLI 会在启动时自动加载：
	•	`canonical_to_aliases.json`
	•	`entries.jsonl`

⸻

# 5. CLI 命令详解

## 1) 查人物信息（别名、反向别名、出场篇目）

`python3 cli.py lookup 王導`

支持：
	•	直接输入规范名（王導）
	•	通过别称查询（阿龍）
	•	通过“見 ××”反向查询（王大將軍 → 王敦）

## 2) 模糊搜索人物名

`python3 cli.py search 王`

返回所有包含该子串的规范人名。

## 3) 查询人物的出场条目

`python3 cli.py appear 王恭`

## 4) 查询某篇某条出现哪些人物（反向索引）

`python3 cli.py reverse 德行 12`

输出所有在“德行·12”中出现的人物。

## 5) 输出某篇某条的原文

`python3 cli.py text 言語 31`


⸻

# 6. 查询结果导出

在执行：

`python3 cli.py lookup <人物>`

后，CLI 会询问：

```
是否要导出该人物的所有出场原文？
y = txt, m = markdown, 其他 = 取消
> 
```

选择格式后，程序自动生成：

TXT 输出示例

`王導_entries.txt`

内容包含所有原文条目。

Markdown 输出示例

`王導_entries.md`

```
格式：

## 德行 27
> 原文……

## 言語 31
> 原文……
```


⸻

# 7. 数据格式示例

canonical_to_aliases.json 格式：

{
  "王導": {
    "aliases": ["茂弘", "阿龍", "丞相"],
    "reference_names": ["丞相王公"],
    "appearances": {
      "德行": [27, 29],
      "言語": [31, 33]
    }
  }
}