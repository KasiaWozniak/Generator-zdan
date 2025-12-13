import random


def random_word(type):
    try:
        with open(f'website/services/words/{type}.txt', 'r', encoding='utf-8') as plik:
            noun = plik.readlines()
        if noun:
            losowa_linia = random.choice(noun).strip()
            return f"{losowa_linia}"
    except Exception as e:
        return f"Wystąpił błąd: {e}"


def random_noun():
    return random_word("nouns")


def random_verb():
    return random_word("verbs")


def random_adjective():
    return random_word("adjectives")


def random_verb_2():
    return random_word("verbs_2")


def random_verb_3():
    return random_word("verbs_3")
