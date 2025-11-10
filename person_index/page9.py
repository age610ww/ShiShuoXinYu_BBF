from person_index import PersonIndex
idx = PersonIndex("canonical_to_aliases.json", conflict_mode="warn")

# ===== 先列出本頁出現的反向索引（見 ××），按頁面自上而下順序 =====
idx.add_reference("王凝之妻", "謝道韞")
idx.add_reference("王孝伯", "王恭")
idx.add_reference("王右軍", "王羲之")
idx.add_reference("王大", "王恬")
idx.add_reference("王大將軍", "王敦")
idx.add_reference("王太尉", "王衍")
idx.add_reference("王右軍夫人", "郗夫人")
# 下列幾條字跡略糊，等你確認後再加：
# idx.add_reference("王荊產", "王徽")
# idx.add_reference("王荊州", "王忬")
# idx.add_reference("王盛田", "王迺")
# idx.add_reference("王孝伯", "王恭")  #（若本頁另處再出一次，重複調用也沒關係）

# ===== 接著是本頁的新建/補充主條目（同樣依頁面順序）=====
idx.add_canonical("王朗", aliases=[], appearances={"德行":[12,13]})

idx.add_canonical("王渾", aliases=["參軍"], appearances={"排調":[8]})

idx.add_canonical("王祥", aliases=["太保"], appearances={"德行":[14,19], "品藻":[6]})

idx.add_canonical(
    "王導",
    aliases=["茂弘","阿龍","丞相","王公","丞相王公","司空"],
    appearances={
        "德行":[27,29],
        "言語":[31,33,36,37,40,102],
        "政事":[12,13,14,15],
        "文學":[21,22],
        "方正":[23,24,36,37,39,40,42,45],
        "雅量":[8,13,14,16,19,22],
        "識鑒":[11,37,40,46,47,54],
        "賞罰":[57,58,59,60,61,62],
        "品藻":[6,13,16,18,20,23,26,28,43],
        "規範": [11, 14, 15],
        "捷悟": [5],
        "容止": [15, 16, 24, 25],
        "企羨": [1, 2],
        "傷逡": [6],
        "樓逸": [4],
        "術解": [8],
        "龍禮": [1],
        "倜誕": [24, 32],
        "簡傲": [7],
        "排調": [10, 12, 13, 14, 16, 18, 21],
        "輕誚": [4, 5, 6, 8],
        "倨睨": [7],
        "決修": [1],
        "尤悔": [5, 6, 7],
        "紆漏": [4],
        "惑溺": [7]
    }
)

idx.add_canonical("王爽", aliases=["王眞"], appearances={"文學":[101], "方正":[64,65], "雅量":[42]})

idx.add_canonical(
    "王恭",
    aliases=[],  # 若你確認括號中“孝伯/王甯/王丞”等是主條目括號，就加進 aliases
    appearances={
        "德行":[44],
        "言語":[86,100],
        "文學":[101,102],
        "方正":[63,64],
        "雅量":[41,42],
        "識鑒":[26],
        "賞罰":[143,153,154,155],
        "品藻":[73,76,78,84,85],
        "容止":[39],
        "企羨":[6],
        "傷逝":[17],
        "任誕":[51,53],
        "排調":[54],
        "輕詆":[22]
    }
)

idx.add_canonical("王蒼", aliases=["小奴","衛軍"], appearances={"雅量":[26,38]})

idx.add_canonical("王著之", aliases=["倩歙"], appearances={"賞罰":[122], "仇隙":[4]})

idx.add_canonical("王彪之", aliases=["虎犢"], appearances={})  # 本頁未見條目號，先建檔

idx.save()

# 可選：頁末做一次體檢
for w in idx.assert_integrity():
    print("[CHECK]", w)