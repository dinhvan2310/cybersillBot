import json
import os

LANG_DIR = "i18n"
_language_cache = {}

def load_language(lang_code):
    """Load language file and cache it."""
    if lang_code in _language_cache:
        return _language_cache[lang_code]
    path = os.path.join(LANG_DIR, f"{lang_code}.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        _language_cache[lang_code] = data
        return data

def get_text(key, lang_code="en", **kwargs):
    """Get translated text by key and language code, with optional format."""
    lang_data = load_language(lang_code)
    text = lang_data.get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text 