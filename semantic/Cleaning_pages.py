from pathlib import Path
import textacy
from textacy import preprocessing
import contractions


def clean_text(file_path):
    """
    Otwiera plik, czyści tekst i przygotowuje go do analizy NLP.
    """
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(p)

    text = p.read_text(encoding="utf8")

    # 1. Rozwijanie skrótów (np. don't -> do not, I'm -> I am)
    expanded_words = []
    for word in text.split():
        # using contractions.fix to expand the shortened words
        expanded_words.append(contractions.fix(word))

    text = ' '.join(expanded_words)

    # 2. Normalizacja białych znaków (usuwa wielokrotne spacje, tabulatory, dziwne znaki nowej linii)
    text = textacy.preprocessing.normalize.whitespace(text)

    # 3. Normalizacja cudzysłowów i myślników (ujednolica różne style zapisu)
    text = textacy.preprocessing.normalize.quotation_marks(text)
    text = textacy.preprocessing.normalize.hyphenated_words(text)

    # 4. Normalizacja Unicode (naprawia błędy kodowania znaków)
    text = textacy.preprocessing.normalize.unicode(text)

    temp = p.with_suffix(p.suffix + ".tmp")
    temp.write_text(text, encoding="utf8")
    temp.replace(p)
    return


def remove_lines_containing(file_path: str, substring: str):
    """
    Usuń wszystkie linie z pliku `file_path` które zawierają `substring`.
    Zwraca liczbę usuniętych linii.
    """

    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(p)

    # Wczytaj linie
    text = p.read_text(encoding="utf8").splitlines(keepends=True)

    match = lambda line: substring in line

    # Filtruj linie
    filtered = [line for line in text if not match(line)]
    removed = len(text) - len(filtered)
    print(f"Removed {removed} lines.")
    # Zapisz przefiltrowaną zawartość z powrotem
    temp = p.with_suffix(p.suffix + ".tmp")
    temp.write_text("".join(filtered), encoding="utf8")
    temp.replace(p)

    return


def remove_lines_of_page(file_path: str):
    """
    Usuń linie z pliku tekstowego, które nie zawierają żadnej litery (tylko cyfry/znaki specjalne).
    Zwraca liczbę usuniętych linii.
    """
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(p)

    # Wczytaj linie z zachowaniem końcówek linii
    text = p.read_text(encoding="utf8").splitlines(keepends=True)

    # Funkcja zwraca True dla linii, które nie zawierają żadnej litery (do usunięcia)
    no_letter = lambda line: not any(ch.isalpha() for ch in line)

    # Przefiltruj linie (zachowaj tylko te, które zawierają przynajmniej jedną literę)
    filtered = [line for line in text if not no_letter(line)]
    removed = len(text) - len(filtered)
    print(f"Removed {removed} lines.")

    # Zapisz przefiltrowaną zawartość atomowo
    temp = p.with_suffix(p.suffix + ".tmp")
    temp.write_text("".join(filtered), encoding="utf8")
    temp.replace(p)

    return


def replace_strings_in_file(file_path: str, old: str, new: str):
    """
    Zamień wszystkie wystąpienia `old` na `new` w pliku `file_path`.
    Zwraca liczbę dokonanych zamian.
    """

    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(p)

    text = p.read_text(encoding="utf8")
    count = text.count(old)

    print(f"Replaced {count} strings.")

    new_text = text.replace(old, new)

    temp = p.with_suffix(p.suffix + ".tmp")
    temp.write_text(new_text, encoding="utf8")
    temp.replace(p)

    return

#remove_lines_containing("B1_B2/TheHungerGames.txt", "Page The Hunger Games — Suzanne Collins")
#remove_lines_of_page("B1_B2/HarryPotter2.txt")
#remove_lines_containing("B1_B2/HarryPotter3.txt", " ")
#replace_strings_in_file("B1_B2/HarryPotter4.txt", "­", "—")
#remove_lines_of_page("B2_C1/OfMiceAndMen.txt")
#remove_lines_of_page("A2_B1/Matilda.txt")
#remove_lines_containing("A2_B1/Matilda.txt", "ROALD DAHL - Matilda")
#remove_lines_containing("A2_B1/Matilda.txt", "The Reader of Books")
#replace_strings_in_file("A2_B1_knowledge_base.json", "ﬁ", "fi")
#replace_strings_in_file("A2_B1_knowledge_base.json", "ﬀ", "ff")
#replace_strings_in_file("A2_B1_knowledge_base.json", "ﬂ", "fl")
#replace_strings_in_file("B1_B2_knowledge_base.json", "ﬁ", "fi")
#replace_strings_in_file("B1_B2_knowledge_base.json", "ﬀ", "ff")
#replace_strings_in_file("B1_B2_knowledge_base.json", "ﬂ", "fl")
#replace_strings_in_file("B2_C1_knowledge_base.json", "ﬁ", "fi")
#replace_strings_in_file("B2_C1_knowledge_base.json", "ﬀ", "ff")
#replace_strings_in_file("B2_C1_knowledge_base.json", "ﬂ", "fl")


files_A2_B1 = [
    'A2_B1/Level1.txt',
    'A2_B1/TheLittlePrince.txt',
    'A2_B1/Matilda.txt',
    'A2_B1/CharlottesWeb.txt',
]

files_B1_B2 = [
    'B1_B2/Level2.txt',
    'B1_B2/TheHungerGames.txt',
    'B1_B2/CatchingFire.txt',
    'B1_B2/Mockingjay.txt',
    'B1_B2/HarryPotter1.txt',
    'B1_B2/HarryPotter2.txt',
    'B1_B2/HarryPotter3.txt',
    'B1_B2/HarryPotter4.txt',
    'B1_B2/HarryPotter4_2.txt',
    'B1_B2/HarryPotter5.txt',
    'B1_B2/HarryPotter6.txt',
    'B1_B2/HarryPotter7.txt',
]

files_B2_C1 = [
    'B2_C1/ManCalledOve.txt',
    'B2_C1/Level3.txt',
    'B2_C1/TheHobbit.txt',
    'B2_C1/OfMiceAndMen.txt',
]

for file in files_A2_B1 + files_B1_B2 + files_B2_C1:
    clean_text(file)