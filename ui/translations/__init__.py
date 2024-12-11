import json
import os

def get_translation(key):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, "ro.json"), "r", encoding="utf-8") as f:
        translations = json.load(f)
    return translations.get(key, key)
