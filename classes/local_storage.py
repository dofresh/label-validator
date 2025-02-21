import json
import os

MAPPING_FILE = "mapping.json"

def save_mapping_to_file(mapping):
    try:
        with open(MAPPING_FILE, "w", encoding="utf-8") as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"매핑 저장 오류: {e}")

def load_mapping_from_file():
    if os.path.exists(MAPPING_FILE):
        try:
            with open(MAPPING_FILE, "r", encoding="utf-8") as f:
                mapping = json.load(f)
                return mapping
        except Exception as e:
            print(f"매핑 불러오기 오류: {e}")
    return {}
