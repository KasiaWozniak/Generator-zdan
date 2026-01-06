import json
import os
import random
from typing import Dict, List, Any

# Cache do przechowywania załadowanych baz wiedzy, aby nie czytać pliku przy każdym żądaniu
_KB_CACHE: Dict[str, Dict[str, Dict[str, List[str]]]] = {}

def load_knowledge(level: str) -> Dict[str, Any]:
    """
    Ładuje plik JSON dla danego poziomu.
    Struktura: { subject: { verb: [objects...] } }
    """
    if level in _KB_CACHE:
        return _KB_CACHE[level]

    path = os.path.join("..\semantic", f"{level}_knowledge_base.json")
    if not os.path.exists(path):
        # Fallback - próba szukania lokalnie lub rzucenie błędu
        if os.path.exists(f"{level}_knowledge_base.json"):
            path = f"{level}_knowledge_base.json"
        else:
            raise FileNotFoundError(f"Brak pliku wiedzy dla poziomu: {level} ({path})")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            _KB_CACHE[level] = data
            return data
    except Exception as e:
        raise ValueError(f"Błąd ładowania JSON: {e}")


def get_all_subjects(level: str) -> List[str]:
    """Zwraca listę wszystkich kluczy (podmiotów) dostępnych na danym poziomie zaawansowania."""
    data = load_knowledge(level)
    return list(data.keys())


def verb_for_subject(subject_key: str, level: str) -> str:
    """Zwraca listę czasowników dla danego klucza podmiotu."""
    data = load_knowledge(level)
    verbs = list(data.get(subject_key, {}).keys())
    if not verbs:
        raise ValueError(f"Brak orzeczeń dla podmiotu '{subject_key}' na poziomie {level}")
    return random.choice(verbs)


def objects_for_subject_verb(subject_key: str, verb: str, level: str) -> List[str]:
    """Zwraca listę dopełnień dla pary podmiot-orzeczenie."""
    data = load_knowledge(level)
    return data.get(subject_key, {}).get(verb, [])