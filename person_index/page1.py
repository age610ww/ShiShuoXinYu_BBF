from person_index import PersonIndex
idx = PersonIndex("/Users/user/Desktop/搞搞别的/世说新语/canonical_to_aliases.json")

# —— 龐統 / 龐士元
idx.add_canonical(
    "龐統",
    aliases=["士元"],                # 括号内的“字”，按你的新规则归入 aliases
    appearances={"言語":[9], "品藻":[2, 3]}
)
idx.add_reference("龐士元", "龐統")   # “見龐統”

# —— 高松（高靈、阿郁、高侍中）
idx.add_canonical(
    "高松",
    aliases=["高靈", "阿酃", "高侍中"],
    appearances={"言語":[82], "排調":[26]}
)
idx.add_reference("高侍中", "高松")   # 24 高侍中 見高松（若已在 aliases 也没关系，这里只是补 reference_names）

# —— 高柔（世遠、安固）
idx.add_canonical(
    "高柔",
    aliases=["世遠", "安固"],
    appearances={"言語":[84], "輕詆":[13]}
)
idx.add_reference("高世遠", "高柔")   # 44 高世遠 見高柔

# —— 高貴鄉公
idx.add_canonical(
    "高貴鄉公",
    aliases=[],
    appearances={"方正":[8], "尤悔":[7]}
)

# —— 高坐道人
idx.add_canonical(
    "高坐道人",
    aliases=[],
    appearances={"言語":[39], "賞罰":[48], "簡傲":[7]}
)

idx.save()