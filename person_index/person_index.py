import json
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Iterable, Optional, Tuple

def _uniq_keep_order(seq: Iterable):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

class PersonIndex:
    """
    维护 'canonical_to_aliases.json' 的增量更新工具（繁体）。
    結構：
    {
      "高柔": {
        "aliases": ["世遠","安固"],
        "reference_names": ["高世遠"],
        "appearances": {"言語":[84], "輕詆":[13]}
      }
    }
    """
    def __init__(self, json_path: str = "canonical_to_aliases.json", conflict_mode: str = "warn"):
        assert conflict_mode in ("raise","warn","ignore")
        self.conflict_mode = conflict_mode
        self.path = Path(json_path)
        if self.path.exists():
            with self.path.open("r", encoding="utf-8") as f:
                self.data: Dict[str, Dict] = json.load(f, object_pairs_hook=OrderedDict)
        else:
            self.data = OrderedDict()
        self._reindex()

    # ---------- 基础 ----------

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def _ensure_person(self, canonical: str):
        if canonical not in self.data:
            self.data[canonical] = OrderedDict([
                ("aliases", []),
                ("reference_names", []),
                ("appearances", OrderedDict())
            ])

    def _reindex(self):
        """重建全局反查索引，供冲突检测使用。"""
        self.ref_owner: Dict[str, str] = {}     # reference_name -> canonical
        self.alias_owner: Dict[str, str] = {}   # alias -> canonical
        for c, obj in self.data.items():
            for r in obj.get("reference_names", []):
                if r not in self.ref_owner:
                    self.ref_owner[r] = c
            for a in obj.get("aliases", []):
                if a not in self.alias_owner:
                    self.alias_owner[a] = c

    # ---------- 公共 API ----------

    def add_canonical(
        self,
        canonical: str,
        aliases: Optional[List[str]] = None,
        appearances: Optional[Dict[str, Iterable[int]]] = None
    ):
        """
        建立/補充主條目：
        - aliases：括號中的並列稱謂（字、號、尊稱等）
        - appearances：{"篇名":[條目號,...]}（合併去重並升序）
        同時檢查別稱在其他人物下是否已存在，若有則告警/報錯。
        """
        self._ensure_person(canonical)

        # 合併 aliases
        if aliases:
            current = self.data[canonical]["aliases"]
            merged = _uniq_keep_order(list(current) + list(aliases))
            self.data[canonical]["aliases"] = merged
            # 衝突檢查：別稱是否被其他人物佔用
            for a in aliases:
                owner = self.alias_owner.get(a)
                if owner and owner != canonical:
                    self._handle_conflict(
                        f"別稱衝突：'{a}' 已屬於 '{owner}'，當前嘗試加入 '{canonical}'"
                    )
                self.alias_owner[a] = canonical  # 更新索引

        # 合併 appearances
        if appearances:
            app = self.data[canonical]["appearances"]
            for section, ids in appearances.items():
                ids = list(ids)
                exist = app.get(section, [])
                merged = sorted(set(int(x) for x in list(exist) + ids))
                app[section] = merged

    def add_reference(self, reference_name: str, canonical: str):
        """
        添加 '見××' 的反向索引到 canonical.reference_names。
        - 若 canonical 尚未建檔，會先佔位。
        - 會檢查 reference_name 是否已指向其他 canonical。
        """
        self._ensure_person(canonical)
        # 衝突檢查：同一 reference_name 指向多個 canonical
        owner = self.ref_owner.get(reference_name)
        if owner and owner != canonical:
            self._handle_conflict(
                f"反向名衝突：'{reference_name}' 已指向 '{owner}'，當前嘗試指向 '{canonical}'"
            )
        refs = self.data[canonical]["reference_names"]
        self.data[canonical]["reference_names"] = _uniq_keep_order(refs + [reference_name])
        self.ref_owner[reference_name] = canonical  # 更新索引

    def add_appearance(self, canonical: str, section: str, ids: Iterable[int]):
        self._ensure_person(canonical)
        app = self.data[canonical]["appearances"]
        exist = app.get(section, [])
        merged = sorted(set(int(x) for x in list(exist) + list(ids)))
        app[section] = merged

    # ---------- 診斷 ----------

    def _handle_conflict(self, msg: str):
        if self.conflict_mode == "raise":
            raise ValueError(msg)
        elif self.conflict_mode == "warn":
            print("[WARN]", msg)
        # ignore：不提示

    def assert_integrity(self) -> List[str]:
        """
        全表體檢，返回告警列表（不拋異常）：
        - 同一 reference_name 指向多個 canonical
        - 同一 alias 存在多個 canonical
        可在批量更新後調用。
        """
        warnings = []
        ref_seen: Dict[str, str] = {}
        alias_seen: Dict[str, str] = {}

        for c, obj in self.data.items():
            for r in obj.get("reference_names", []):
                if r in ref_seen and ref_seen[r] != c:
                    warnings.append(f"反向名重複：'{r}' -> '{ref_seen[r]}' / '{c}'")
                else:
                    ref_seen[r] = c
            for a in obj.get("aliases", []):
                if a in alias_seen and alias_seen[a] != c:
                    warnings.append(f"別稱重複：'{a}' -> '{alias_seen[a]}' / '{c}'")
                else:
                    alias_seen[a] = c
        return warnings