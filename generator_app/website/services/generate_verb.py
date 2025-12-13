from generator_app.website.services.choose_random_word import random_verb, random_verb_2, random_verb_3

def generate_verb(subject, tense, number, mood, question, pronoun, noun, complement):
    verb = random_verb()

    if tense == "present_simple":
        third_person = is_third_person(number, pronoun, noun)
        if question:
            return make_simple_question(mood, verb, third_person, subject, complement)
        return f"{subject.capitalize()} {make_verb_simple(random_verb(), third_person, mood)} {complement}."

    elif tense == "present_continuous":
        before, after = make_verb_continuous(random_verb(), get_be(pronoun, noun))

    elif tense == "present_perfect":
        third_person = is_third_person(number, pronoun, noun)
        before, after = get_have(third_person), random_verb_3()

    elif tense == "present_perfect_continuous":
        third_person = is_third_person(number, pronoun, noun)
        before, after = make_verb_perfect_continuous(random_verb(), get_have(third_person))

    elif tense == "past_simple":
        if question:
            return make_past_question(subject, complement, mood)
        return f"{subject.capitalize()} {make_verb_past(mood)} {complement}."

    elif tense == "past_continuous":
        before, after = make_verb_continuous(random_verb(), get_be_2(pronoun, noun))

    elif tense == "past_perfect":
        before, after = "had", random_verb_3()

    elif tense == "past_perfect_continuous":
        before, after = make_verb_perfect_continuous(random_verb(), "had")

    elif tense == "future_simple":
        before, after = "will", random_verb()

    elif tense == "future_continuous":
        before, after = "will", " ".join(make_verb_continuous(random_verb(), "be"))

    elif tense == "future_perfect":
        before, after = "will", f"have {random_verb_3()}"

    else:
        before, after = "will", " ".join(make_verb_perfect_continuous(random_verb(), "have"))

    if question:
        if mood:
            return f"{before.capitalize()} {subject} {after} {complement}?"
        else:
            return f"{before.capitalize()} {subject} not {after} {complement}?"
    else:
        if mood:
            return f"{subject.capitalize()} {before} {after} {complement}."
        else:
            return f"{subject.capitalize()} {before} not {after} {complement}."


def make_verb_simple(verb, third_person, mood):
    if not mood:
        if third_person:
            return f'does not {verb}'
        else:
            return f'do not {verb}'

    if " " in verb:
        verb, addition = verb.split(" ")
    else:
        addition = None

    if third_person:
        if verb[-1] == "y":
            verb = verb[0:-1] + "ies"
        elif verb[-1] in ("s", "z", "x", "o") or verb[len(verb) - 2:] in ("sh", "ch"):
            verb += "es"
        else:
            verb += "s"

    if addition:
        return f'{verb} {addition}'
    return verb


def make_simple_question(mood, verb, third_person, subject, complement):
    if not mood:
        verb = f"not {verb}"
    if third_person:
        return f"Does {subject} {verb} {complement}?"
    else:
        return f"Do {subject} {verb} {complement}?"


def make_verb_continuous(verb, be):
    verb, addition = get_ing(verb)
    if addition:
        return be, f'{verb} {addition}'
    return be, verb


def make_verb_perfect_continuous(verb, have):
    verb, addition = get_ing(verb)
    if addition:
        return have, f'been {verb} {addition}'
    return have, f'been {verb}'


def make_verb_past(mood):
    if not mood:
        verb = f"did not {random_verb()}"
    else:
        verb = random_verb_2()
    return verb


def make_past_question(subject, complement, mood):
    if not mood:
        verb = f"not {random_verb()}"
    else:
        verb = random_verb()
    return f"Did {subject} {verb} {complement}?"


def is_third_person(number, pronoun, noun):
    if number == "singular":
        if pronoun in ("he", "she", "it", "this", "that") or noun:
            return True
    return False


def get_be(pronoun, noun):
    if pronoun == "I":
        return "am"
    if pronoun in ("he", "she", "it", "this", "that") or noun:
        return "is"
    else:
        return "are"


def get_be_2(pronoun, noun):
    if pronoun in ("I", "he", "she", "it", "this", "that") or noun:
        return "was"
    else:
        return "were"


def get_have(third_person):
    if third_person:
        return "has"
    else:
        return "have"


def get_ing(verb):
    if " " in verb:
        verb, addition = verb.split(" ")
    else:
        addition = None
    if verb[-1] == "e":
        verb = verb[0:-1] + "ing"
    else:
        verb += "ing"
    return verb, addition
