# -*- coding: utf-8 -*-

import json

def get_person(idx, canonical):
    return idx.data.get(canonical, None)

def lookup_name(idx, name):
    if name in idx.data:
        return name
    for canonical, obj in idx.data.items():
        if name in obj.get("aliases", []):
            return canonical
    for canonical, obj in idx.data.items():
        if name in obj.get("reference_names", []):
            return canonical
    return None

def get_appearances(idx, canonical):
    person = idx.data.get(canonical)
    if not person:
        return {}
    return person.get("appearances", {})

def find_people_in_entry(idx, section, entry_id):
    result = []
    for canonical, obj in idx.data.items():
        app = obj.get("appearances", {})
        if section in app and entry_id in app[section]:
            result.append(canonical)
    return result

def search_people(idx, text):
    text = text.strip()
    results = []
    for canonical, obj in idx.data.items():
        if text in canonical:
            results.append(canonical)
            continue
        for a in obj.get("aliases", []):
            if text in a:
                results.append(canonical)
                break
        for r in obj.get("reference_names", []):
            if text in r:
                results.append(canonical)
                break
    return results


def load_entries_jsonl(path="entries.jsonl"):
    entries = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            key = (obj["section"], int(obj["index"]))
            entries[key] = obj["text"]
    return entries