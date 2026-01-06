import random
from typing import Dict, Any, List
from generator_app.website.services.choose_random_word import get_all_subjects, objects_for_subject_verb


def generate_subject(arguments: Dict[str, Any], level: str) -> List[str]:
    """
    Generuje podmiot (Subject).
    Zwraca: [subject_key, phrase_string]
    """

    all_keys = get_all_subjects(level)

    is_noun_phrase = arguments.get("noun")
    number = arguments.get("number")
    selection_type = arguments.get("pronoun_or_article")


    if not is_noun_phrase:
        if number == "singular" and selection_type == "personal":
            valid_keys = [k for k in ["person", "it"] if k in all_keys] or ["it"]
            subject_key = random.choice(valid_keys)
            phrase = random.choice(["I", "you", "he", "she"]) if subject_key == "person" else "it"
        elif number == "singular" and selection_type == "demonstrative":
            subject_key = "it"
            phrase = random.choice(["this", "that"])
        elif selection_type == "indefinite":
            valid_keys = [k for k in ["person", "it"] if k in all_keys] or ["it"]
            subject_key = random.choice(valid_keys)
            if subject_key == "person":
                phrase = random.choice(
                    ["someone", "somebody", "anyone", "anybody", "no one", "nobody", "everyone", "everybody"])
            else:
                phrase = random.choice(["something", "anything", "nothing", "everything"])
        elif number == "singular" and selection_type == "possessive":
            subject_key = random.choice(all_keys)
            phrase = random.choice(["mine", "yours", "his", "hers", "ours", "theirs"])
        elif number == "plural" and selection_type == "personal":
            valid_keys = [k for k in ["person", "it"] if k in all_keys] or ["it"]
            subject_key = random.choice(valid_keys)
            phrase = random.choice(["we", "you", "they"]) if subject_key == "person" else "they"
        elif number == "plural" and selection_type == "demonstrative":
            valid_keys = [k for k in ["person", "it"] if k in all_keys] or ["it"]
            subject_key = random.choice(valid_keys)
            phrase = random.choice(["these", "those"])
        elif number == "plural" and selection_type == "possessive":
            subject_key = random.choice(all_keys)
            phrase = random.choice(["mine", "yours", "his", "hers", "ours", "theirs"])
        else:
            subject_key = "it"
            phrase = "it"

    else:
        if number == "singular" and selection_type == "possessive_det":
            valid_keys = [k for k in all_keys if k != "it"] or ["person"]
            subject_key = random.choice(valid_keys)
            if subject_key == "person":
                noun_str = random.choice(["person", "boy", "girl", "woman", "man"])
                det = random.choice(["my", "your", "her", "his", "our", "their"])
            else:
                noun_str = subject_key
                det = random.choice(["my", "your", "her", "his", "its", "our", "their"])
            phrase = f"{det} {noun_str}"
        elif number == "singular" and selection_type == "demonstrative_det":
            subject_key = random.choice(all_keys)
            if subject_key == "it":
                noun_str = "thing"
            elif subject_key == "person":
                noun_str = random.choice(["person", "boy", "girl", "woman", "man"])
            else:
                noun_str = subject_key
            phrase = f"{random.choice(['this', 'that'])} {noun_str}"
        elif number == "singular" and selection_type == "article":
            valid_keys = [k for k in all_keys if k != "it"] or ["person"]
            subject_key = random.choice(valid_keys)
            if subject_key == "person":
                noun_str = random.choice(["person", "boy", "girl", "woman", "man"])
            else:
                noun_str = subject_key
            if random.choice(["definite", "indefinite"]) == "definite":
                phrase = f"the {noun_str}"
            else:
                phrase = f"{get_indefinite_article(noun_str)} {noun_str}"
        elif number == "plural" and selection_type == "possessive_det":
            valid_keys = [k for k in all_keys if k != "it"] or ["person"]
            subject_key = random.choice(valid_keys)
            if subject_key == "person":
                noun_str = random.choice(["people", "boys", "girls", "women", "men"])
                det = random.choice(["my", "your", "her", "his", "our", "their"])
            else:
                noun_str = make_plural(subject_key)
                det = random.choice(["my", "your", "her", "his", "its", "our", "their"])
            phrase = f"{det} {noun_str}"
        elif number == "plural" and selection_type == "demonstrative_det":
            subject_key = random.choice(all_keys)
            if subject_key == "it":
                noun_str = "things"
            elif subject_key == "person":
                noun_str = random.choice(["people", "boys", "girls", "women", "men"])
            else:
                noun_str = make_plural(subject_key)
            phrase = f"{random.choice(['these', 'those'])} {noun_str}"
        elif number == "plural" and selection_type == "article":
            valid_keys = [k for k in all_keys if k != "it"] or ["person"]
            subject_key = random.choice(valid_keys)
            if subject_key == "person":
                noun_str = random.choice(["people", "boys", "girls", "women", "men"])
            else:
                noun_str = make_plural(subject_key)
            phrase = f"the {noun_str}" if random.choice(["definite", "indefinite"]) == "definite" else noun_str
        else:
            subject_key = "it"
            phrase = "something"

    return [subject_key, phrase]


def generate_complement(arguments: Dict[str, Any], level: str, subject_key: str, verb: str) -> List[str]:
    """
    Generuje dopełnienie (Complement/Object).
    Wymaga subject_key i verb, aby pobrać poprawne semantycznie obiekty z bazy.
    Zwraca: [object_key, phrase_string]
    """

    valid_objects = objects_for_subject_verb(subject_key, verb, level)

    is_noun_phrase = arguments.get("noun")
    number = arguments.get("number")
    selection_type = arguments.get("pronoun_or_article")

    if not is_noun_phrase:

        if number == "singular" and selection_type == "personal":
            candidates = [k for k in ["person", "it"] if k in valid_objects]
            if not candidates: candidates = ["it"]  # fallback

            object_key = random.choice(candidates)

            if object_key == "person":
                phrase = random.choice(["me", "you", "him", "her"])
            else:
                phrase = "it"

        elif number == "singular" and selection_type == "demonstrative":
            object_key = "it"
            phrase = random.choice(["this", "that"])

        elif selection_type == "indefinite":
            candidates = [k for k in ["person", "it"] if k in valid_objects]
            if not candidates: candidates = ["it"]

            object_key = random.choice(candidates)

            if object_key == "person":
                phrase = random.choice(
                    ["someone", "somebody", "anyone", "anybody", "no one", "nobody", "everyone", "everybody"])
            else:
                phrase = random.choice(["something", "anything", "nothing", "everything"])

        elif number == "singular" and selection_type == "possessive":
            object_key = random.choice(valid_objects)
            phrase = random.choice(["mine", "yours", "his", "hers", "ours", "theirs"])

        elif number == "plural" and selection_type == "personal":
            candidates = [k for k in ["person", "it"] if k in valid_objects]
            if not candidates: candidates = ["it"]

            object_key = random.choice(candidates)

            if object_key == "person":
                phrase = random.choice(["us", "you", "them"])
            else:
                phrase = "them"

        elif number == "plural" and selection_type == "demonstrative":
            candidates = [k for k in ["person", "it"] if k in valid_objects]
            if not candidates: candidates = ["it"]
            object_key = random.choice(candidates)

            phrase = random.choice(["these", "those"])

        elif number == "plural" and selection_type == "possessive":
            object_key = random.choice(valid_objects)
            phrase = random.choice(["mine", "yours", "his", "hers", "ours", "theirs"])

        else:
            object_key = "it"
            phrase = "it"

    else:
        if number == "singular" and selection_type == "possessive_det":
            candidates = [k for k in valid_objects if k != "it"]
            if not candidates: candidates = ["person"]  # fallback

            object_key = random.choice(candidates)

            if object_key == "person":
                noun_str = random.choice(["person", "boy", "girl", "woman", "man"])
                det = random.choice(["my", "your", "her", "his", "our", "their"])
            else:
                noun_str = object_key
                det = random.choice(["my", "your", "her", "his", "its", "our", "their"])

            phrase = f"{det} {noun_str}"

        elif number == "singular" and selection_type == "demonstrative_det":
            object_key = random.choice(valid_objects)

            if object_key == "it":
                noun_str = "thing"
            elif object_key == "person":
                noun_str = random.choice(["person", "boy", "girl", "woman", "man"])
            else:
                noun_str = object_key

            det = random.choice(["this", "that"])
            phrase = f"{det} {noun_str}"

        elif number == "singular" and selection_type == "article":
            candidates = [k for k in valid_objects if k != "it"]
            if not candidates: candidates = ["person"]

            object_key = random.choice(candidates)

            if object_key == "person":
                noun_str = random.choice(["person", "boy", "girl", "woman", "man"])
            else:
                noun_str = object_key

            article_type = random.choice(["definite", "indefinite"])
            if article_type == "definite":
                phrase = f"the {noun_str}"
            else:
                phrase = f"{get_indefinite_article(noun_str)} {noun_str}"

        elif number == "plural" and selection_type == "possessive_det":
            candidates = [k for k in valid_objects if k != "it"]
            if not candidates: candidates = ["person"]

            object_key = random.choice(candidates)

            if object_key == "person":
                noun_str = random.choice(["people", "boys", "girls", "women", "men"])
                det = random.choice(["my", "your", "her", "his", "our", "their"])  # bez its
            else:
                noun_str = make_plural(object_key)
                det = random.choice(["my", "your", "her", "his", "its", "our", "their"])

            phrase = f"{det} {noun_str}"

        elif number == "plural" and selection_type == "demonstrative_det":
            object_key = random.choice(valid_objects)

            if object_key == "it":
                noun_str = "things"
            elif object_key == "person":
                noun_str = random.choice(["people", "boys", "girls", "women", "men"])
            else:
                noun_str = make_plural(object_key)

            det = random.choice(["these", "those"])
            phrase = f"{det} {noun_str}"

        elif number == "plural" and selection_type == "article":
            candidates = [k for k in valid_objects if k != "it"]
            if not candidates: candidates = ["person"]

            object_key = random.choice(candidates)

            if object_key == "person":
                noun_str = random.choice(["people", "boys", "girls", "women", "men"])
            else:
                noun_str = make_plural(object_key)

            article_type = random.choice(["definite", "indefinite"])
            if article_type == "definite":
                phrase = f"the {noun_str}"
            else:
                phrase = noun_str

        else:
            object_key = "it"
            phrase = "something"

    return [object_key, phrase]


def get_indefinite_article(word: str) -> str:
    """Zwraca 'a' lub 'an' w zależności od pierwszej litery rzeczownika."""
    if not word: return "a"
    if word[0].lower() in ('a', 'e', 'i', 'o', 'u'):
        return "an"
    return "a"


def make_plural(word: str) -> str:
    """Tworzenie liczby mnogiej."""
    if not word: return ""
    w = word.lower()

    irregular = {
        "man": "men", "woman": "women", "child": "children",
        "person": "people", "mouse": "mice", "tooth": "teeth",
        "foot": "feet", "goose": "geese", "thing": "things"
    }
    if w in irregular:
        return irregular[w]

    if w.endswith(('s', 'x', 'z', 'ch', 'sh')):
        return w + "es"
    if w.endswith('y') and len(w) > 1 and w[-2] not in "aeiou":
        return w[:-1] + "ies"

    return w + "s"