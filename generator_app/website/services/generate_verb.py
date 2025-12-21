import random
from typing import Tuple
# Importujemy funkcję form_of_verb z pliku choose_random_word (zakładamy, że tam się znajduje)
from generator_app.website.services.choose_random_word import form_of_verb


def generate_verb(subject_phrase: str, verb_base: str, complement_phrase: str,
                  tense: str, number: str, mood: bool, question: bool,
                  pronoun_category: str, noun_flag: bool, level: str) -> str:
    """
    Generuje pełne zdanie z poprawnie odmienionym orzeczeniem.

    Argumenty:
    - subject_phrase: gotowy string podmiotu (np. 'My dogs', 'She', 'The boy').
    - verb_base: bezokolicznik czasownika (np. 'eat', 'go').
    - complement_phrase: gotowy string dopełnienia (np. 'an apple').
    - tense: czas gramatyczny.
    - number: 'singular' lub 'plural'.
    - mood: True (twierdzące), False (przeczące).
    - question: True (pytające), False (nie-pytające).
    - pronoun_category: kategoria wybrana w menu (np. 'personal', 'demonstrative') - używana pomocniczo.
    - noun_flag: True jeśli podmiot jest frazą rzeczownikową, False jeśli zaimkiem.
    """

    subject = subject_phrase.strip()
    verb = verb_base.lower()
    complement = complement_phrase.strip()

    # Sprawdzamy czy podmiot to 3. osoba liczby pojedynczej (he/she/it/rzeczownik l.poj)
    third_person = is_third_person(subject, number, noun_flag)

    # Inicjalizacja zmiennych pomocniczych dla konstrukcji złożonych
    before = ""  # To co stoi przed głównym czasownikiem (auxiliary)
    after = ""  # Główny czasownik w odpowiedniej formie (np. v3, ing)

    # --- LOGIKA CZASÓW ---

    if tense == "present_simple":
        if question:
            return make_simple_question(mood, verb, third_person, subject, complement)
        return make_simple_sentence(mood, verb, third_person, subject, complement)

    elif tense == "present_continuous":
        aux_be = get_be_present(subject, number, noun_flag)
        before, after = make_verb_continuous(verb, aux_be)

    elif tense == "present_perfect":
        aux_have = get_have_present(third_person)
        before, after = aux_have, form_of_verb(3, verb)

    elif tense == "present_perfect_continuous":
        aux_have = get_have_present(third_person)
        before, after = make_verb_perfect_continuous(verb, aux_have)

    elif tense == "past_simple":
        if question:
            return make_past_question(mood, verb, subject, complement)
        return make_past_sentence(mood, verb, subject, complement)

    elif tense == "past_continuous":
        aux_be = get_be_past(subject, number, noun_flag)
        before, after = make_verb_continuous(verb, aux_be)

    elif tense == "past_perfect":
        before, after = "had", form_of_verb(3, verb)

    elif tense == "past_perfect_continuous":
        before, after = make_verb_perfect_continuous(verb, "had")

    elif tense == "future_simple":
        before, after = "will", verb

    elif tense == "future_continuous":
        before, after = "will", f"be {get_ing(verb)}"

    elif tense == "future_perfect":
        before, after = "will", f"have {form_of_verb(3, verb)}"

    elif tense == "future_perfect_continuous":
        before, after = "will", f"have been {get_ing(verb)}"

    else:
        # Fallback dla nieznanego czasu
        return f"{subject} {verb} {complement}."

    # --- SKŁADANIE ZDANIA (dla czasów innych niż Simple) ---
    # Tutaj trafiają wszystkie czasy Continuous, Perfect i Future

    # Capitalize subject only
    subj_cap = subject[0].upper() + subject[1:] if subject else ""

    if question:
        if mood:  # Pytanie twierdzące: "Will he go?"
            return f"{before.capitalize()} {subject} {after} {complement}?"
        else:  # Pytanie przeczące: "Will he not go?" (lub Won't he go - tu wersja formalna z 'not')
            # Wersja full: "Will the dog not eat?"
            return f"{before.capitalize()} {subject} not {after} {complement}?"
    else:
        if mood:  # Twierdzenie: "He will go."
            return f"{subj_cap} {before} {after} {complement}."
        else:  # Przeczenie: "He will not go."
            return f"{subj_cap} {before} not {after} {complement}."


# --- FUNKCJE POMOCNICZE (LOGIKA GRAMATYCZNA) ---

def is_third_person(subject_phrase: str, number: str, noun_flag: bool) -> bool:
    """
    Określa, czy podmiot wymaga formy 3. osoby l.poj (np. 'does', 'has', 'is').
    """
    # 1. Jeśli liczba mnoga -> False (they, we, you, dogs)
    if number == "plural":
        return False

    # 2. Jeśli to fraza rzeczownikowa (noun=True) i liczba pojedyncza -> True (The dog, A boy)
    if noun_flag:
        return True

    # 3. Jeśli to zaimek (noun=False), musimy sprawdzić jaki konkretnie
    s = subject_phrase.lower()
    if s in ("i", "you"):
        return False

    # Pozostałe zaimki singularne: he, she, it, this, that, someone, everyone... -> True
    return True


def get_be_present(subject_phrase: str, number: str, noun_flag: bool) -> str:
    """Zwraca 'am', 'is' lub 'are'."""
    s = subject_phrase.lower()

    if s == "i" and not noun_flag:
        return "am"

    if number == "plural" or s == "you":
        return "are"

    # 3 os. l.poj
    return "is"


def get_be_past(subject_phrase: str, number: str, noun_flag: bool) -> str:
    """Zwraca 'was' lub 'were'."""
    s = subject_phrase.lower()

    if number == "plural" or s == "you":
        return "were"

    # I, he, she, it, rzeczowniki l.poj -> was
    return "was"


def get_have_present(third_person: bool) -> str:
    return "has" if third_person else "have"


def get_ing(verb: str) -> str:
    """Tworzy formę Gerund (ing)."""
    # Obsługa phrasal verbs np. "wake up" -> "waking up"
    addition = ""
    if " " in verb:
        verb, addition = verb.split(" ", 1)
        addition = " " + addition

    v = verb.lower()
    if v.endswith("ie"):
        base = v[:-2] + "ying"
    elif v.endswith("e") and not v.endswith("ee"):
        base = v[:-1] + "ing"
    elif len(v) > 2 and v[-1] not in "aeiouwyx" and v[-2] in "aeiou" and v[-3] not in "aeiou":
        # Podwajanie spółgłoski (uproszczone, np. sit -> sitting)
        base = v + v[-1] + "ing"
    else:
        base = v + "ing"

    return base + addition


# --- FUNKCJE BUDUJĄCE CZĘŚCI ZDANIA ---

def make_simple_sentence(mood: bool, verb: str, third_person: bool, subject: str, complement: str) -> str:
    """Obsługa Present Simple (Twierdzące/Przeczące)."""
    subj_cap = subject[0].upper() + subject[1:]

    if mood:  # Twierdzące
        final_verb = verb
        # Dodawanie -s/-es w 3 os. l.poj
        if third_person:
            # Obsługa phrasal verbs
            addition = ""
            if " " in verb:
                verb_part, addition = verb.split(" ", 1)
                addition = " " + addition
            else:
                verb_part = verb

            if verb_part.endswith("y") and len(verb_part) > 1 and verb_part[-2] not in "aeiou":
                verb_part = verb_part[:-1] + "ies"
            elif verb_part.endswith(("s", "z", "x", "ch", "sh", "o")):
                verb_part += "es"
            else:
                verb_part += "s"
            final_verb = verb_part + addition

        return f"{subj_cap} {final_verb} {complement}."

    else:  # Przeczące
        aux = "does" if third_person else "do"
        return f"{subj_cap} {aux} not {verb} {complement}."


def make_simple_question(mood: bool, verb: str, third_person: bool, subject: str, complement: str) -> str:
    """Obsługa Present Simple (Pytania)."""
    aux = "Does" if third_person else "Do"

    if mood:  # Pytanie zwykłe: Do you eat?
        return f"{aux} {subject} {verb} {complement}?"
    else:  # Pytanie przeczące: Do you not eat?
        return f"{aux} {subject} not {verb} {complement}?"


def make_past_sentence(mood: bool, verb: str, subject: str, complement: str) -> str:
    """Obsługa Past Simple."""
    subj_cap = subject[0].upper() + subject[1:]

    if mood:  # Twierdzące: I ate.
        v2 = form_of_verb(2, verb)
        return f"{subj_cap} {v2} {complement}."
    else:  # Przeczące: I did not eat.
        return f"{subj_cap} did not {verb} {complement}."


def make_past_question(mood: bool, verb: str, subject: str, complement: str) -> str:
    """Obsługa Past Simple (Pytania)."""
    if mood:
        return f"Did {subject} {verb} {complement}?"
    else:
        return f"Did {subject} not {verb} {complement}?"


def make_verb_continuous(verb: str, aux_be: str) -> Tuple[str, str]:
    """Zwraca (aux, main_verb) dla czasów Continuous."""
    return aux_be, get_ing(verb)


def make_verb_perfect_continuous(verb: str, aux_have: str) -> Tuple[str, str]:
    """Zwraca (aux, main_verb) dla czasów Perfect Continuous."""
    return aux_have, f"been {get_ing(verb)}"