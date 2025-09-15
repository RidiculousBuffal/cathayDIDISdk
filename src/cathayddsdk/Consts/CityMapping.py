import json
import threading
from collections import defaultdict
from importlib.resources import files
from pathlib import Path
from typing import List, Dict, Tuple, Set, Optional

# 数据文件路径（相对于本模块文件）
_here = Path(__file__).resolve().parent
_data_file = _here / "city20250915.json"


class CityLookup:
    def __init__(self, items: List[Dict], case_sensitive: bool = False):
        self.case_sensitive = case_sensitive
        # mapping: normalized name -> set of (city_id, city_name)
        self._city_map: Dict[str, Set[Tuple[int, str]]] = defaultdict(set)
        self._county_map: Dict[str, Set[Tuple[int, str]]] = defaultdict(set)
        self._build(items)

    def _norm(self, name: str) -> str:
        return name if self.case_sensitive else name.strip().lower()

    def _build(self, items: List[Dict]):
        for it in items:
            cid = it.get("city_id")
            cname = it.get("city_name")
            if cid is None or cname is None:
                continue
            kn = self._norm(cname)
            self._city_map[kn].add((cid, cname))
            for c in it.get("county_list", []):
                county_name = c.get("county_name")
                if county_name:
                    kn2 = self._norm(county_name)
                    # 把 county_name 映射到对应的 city 信息
                    self._county_map[kn2].add((cid, cname))

    def find(self, name: str, exact: bool = True) -> List[Dict]:
        if not name:
            return []
        q = self._norm(name)
        results: Set[Tuple[int, str]] = set()

        if exact:
            if q in self._city_map:
                results.update(self._city_map[q])
            if q in self._county_map:
                results.update(self._county_map[q])
        else:
            # 模糊子串匹配（在 key 上）
            for k, v in self._city_map.items():
                if q in k or k in q:
                    results.update(v)
            for k, v in self._county_map.items():
                if q in k or k in q:
                    results.update(v)

        return [{"city_id": cid, "city_name": cname} for cid, cname in sorted(results)]


_lock = threading.Lock()
_singleton: Optional[CityLookup] = None


def _load_items() -> Dict:
    text = files(__package__).joinpath("city20250915.json").read_text(encoding="utf-8")
    return json.loads(text)


def get_city_lookup(case_sensitive: bool = False, force_reload: bool = False) -> CityLookup:
    global _singleton
    if _singleton is None or force_reload:
        with _lock:
            if _singleton is None or force_reload:
                items = _load_items()
                _singleton = CityLookup(items.get('data'), case_sensitive=case_sensitive)
    return _singleton

