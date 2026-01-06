from pathlib import Path
import json

# --- KONFIGURACJA MAPOWANIA ---
MAPOWANIE_ZAIMKOW = {
    # Te słowa zamieniamy na "person"
    **{slowo: "person" for slowo in [
        "I", "i", "you", "she", "he", "me", "him", "her", "us", "them", "they", "we",
        "someone", "somebody", "people", "anyone", "anybody", "everyone", "everybody",
        "noone", "nobody", "myself", "himself", "herself", "yourself", "ourself",
        "themself", "ourselves", "yourselves", "themselves"
    ]},
    # Te słowa zamieniamy na "it"
    **{slowo: "it" for slowo in [
        "itself", "something", "anything", "nothing", "everything", "this", "that", "these", "those"
    ]}
}


def merge_values(v1, v2):
    """
    Łączy dwie wartości w przypadku kolizji kluczy.
    Wspiera łączenie list (bez duplikatów) oraz słowników.
    """
    if isinstance(v1, list) and isinstance(v2, list):
        # Łączymy listy i usuwamy duplikaty zachowując kolejność
        seen = set()
        result = []
        for item in v1 + v2:
            # Jeśli elementem listy jest słownik, nie możemy go dodać do set() bezpośrednio
            # Uproszczone usuwanie duplikatów dla typów prostych
            val_hash = json.dumps(item, sort_keys=True) if isinstance(item, (dict, list)) else item
            if val_hash not in seen:
                seen.add(val_hash)
                result.append(item)
        return result

    if isinstance(v1, dict) and isinstance(v2, dict):
        # Jeśli oba są słownikami, łączymy je (płytkie łączenie)
        new_dict = v1.copy()
        for k, v in v2.items():
            if k in new_dict:
                new_dict[k] = merge_values(new_dict[k], v)
            else:
                new_dict[k] = v
        return new_dict

    # W innych przypadkach (np. str, int) zwracamy nowszą wartość
    return v2


def rekurencyjne_przetwarzanie(dane):
    """
    Przechodzi przez JSON, zamienia zaimki w kluczach i wartościach
    oraz dba o to, by nie gubić danych przy kolizji kluczy.
    """
    # 1. Jeśli to napis (str) -> sprawdzamy mapowanie
    if isinstance(dane, str):
        czyste = dane.strip().lower()
        return MAPOWANIE_ZAIMKOW.get(czyste, dane)

    # 2. Jeśli to słownik (dict) -> przetwarzamy klucze i wartości
    elif isinstance(dane, dict):
        nowy_slownik = {}
        for k, v in dane.items():
            # Przetwarzamy klucz i wartość
            nowy_klucz = rekurencyjne_przetwarzanie(k)
            nowa_wartosc = rekurencyjne_przetwarzanie(v)

            if nowy_klucz in nowy_slownik:
                # KOLIZJA! Łączymy starą zawartość z nową
                nowy_slownik[nowy_klucz] = merge_values(nowy_slownik[nowy_klucz], nowa_wartosc)
            else:
                nowy_slownik[nowy_klucz] = nowa_wartosc
        return nowy_slownik

    # 3. Jeśli to lista (list) -> przetwarzamy każdy element
    elif isinstance(dane, list):
        # Tutaj też warto zadbać o unikalność po zmianie
        przetworzona_lista = [rekurencyjne_przetwarzanie(item) for item in dane]
        # Usuwamy ewentualne duplikaty wynikłe z zamiany (np. ["he", "she"] -> ["person", "person"])
        seen = set()
        result = []
        for item in przetworzona_lista:
            val_hash = json.dumps(item, sort_keys=True) if isinstance(item, (dict, list)) else item
            if val_hash not in seen:
                seen.add(val_hash)
                result.append(item)
        return result

    return dane


def napraw_i_zamien_w_pliku(filepath):
    p = Path(filepath)
    if not p.exists():
        print(f"Błąd: Nie znaleziono pliku {filepath}")
        return

    try:
        # 1. Wczytujemy dane
        with open(p, 'r', encoding='utf-8') as f:
            dane = json.load(f)

        # 2. Przetwarzamy (zamiana + scalanie kolizji)
        wynik = rekurencyjne_przetwarzanie(dane)

        # 3. Zapisujemy do pliku tymczasowego i podmieniamy (bezpieczny zapis)
        temp_file = p.with_suffix(".tmp")
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(wynik, f, indent=2, ensure_ascii=False)

        temp_file.replace(p)
        print(f"Sukces: Przetworzono {filepath}")

    except Exception as e:
        print(f"Błąd podczas pracy z plikiem {filepath}: {e}")


# --- URUCHOMIENIE ---
pliki = [
    "A2_B1_knowledge_base.json",
    "B1_B2_knowledge_base.json",
    "B2_C1_knowledge_base.json"
]

for plik in pliki:
    napraw_i_zamien_w_pliku(plik)
