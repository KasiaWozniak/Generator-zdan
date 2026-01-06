from typing import Tuple

def generate_verb(subject_phrase: str, verb_base: str, complement_phrase: str,
                  tense: str, number: str, mood: bool, question: bool, noun_flag: bool) -> str:
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
    - noun_flag: True jeśli podmiot jest frazą rzeczownikową, False jeśli zaimkiem.
    """

    subject = subject_phrase.strip()
    verb = verb_base.lower()
    complement = complement_phrase.strip()

    third_person = is_third_person(subject, number, noun_flag)


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

    subj_cap = subject[0].upper() + subject[1:] if subject else ""

    if question:
        if mood:
            return f"{before.capitalize()} {subject} {after} {complement}?"
        else:
            return f"{before.capitalize()} {subject} not {after} {complement}?"
    else:
        if mood:
            return f"{subj_cap} {before} {after} {complement}."
        else:
            return f"{subj_cap} {before} not {after} {complement}."



def is_third_person(subject_phrase: str, number: str, noun_flag: bool) -> bool:
    """
    Określenie, czy podmiot wymaga formy dla 3. osoby l.poj.
    """
    if number == "plural":
        return False

    if noun_flag:
        return True

    s = subject_phrase.lower()
    if s in ("i", "you"):
        return False

    return True


def get_be_present(subject_phrase: str, number: str, noun_flag: bool) -> str:
    """Zwraca 'am', 'is' lub 'are'."""
    s = subject_phrase.lower()

    if s == "i" and not noun_flag:
        return "am"

    if number == "plural" or s == "you":
        return "are"

    return "is"


def get_be_past(subject_phrase: str, number: str, noun_flag: bool) -> str:
    """Zwraca 'was' lub 'were'."""
    s = subject_phrase.lower()

    if number == "plural" or s == "you":
        return "were"

    return "was"


def get_have_present(third_person: bool) -> str:
    return "has" if third_person else "have"


def get_ing(verb: str) -> str:
    """Tworzy formę Gerund (ing)."""
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
        base = v + v[-1] + "ing"
    else:
        base = v + "ing"

    return base + addition


def form_of_verb(form: int, verb: str) -> str:
    if form not in (2, 3):
        raise ValueError("form must be 2 or 3")

    if not verb or not isinstance(verb, str):
        raise ValueError("verb must be a non-empty string")

    v = verb.lower()

    irregular = {
        "be": ("was", "been"),
        "become": ("became", "become"),
        "begin": ("began", "begun"),
        "break": ("broke", "broken"),
        "bring": ("brought", "brought"),
        "build": ("built", "built"),
        "buy": ("bought", "bought"),
        "catch": ("caught", "caught"),
        "choose": ("chose", "chosen"),
        "come": ("came", "come"),
        "cost": ("cost", "cost"),
        "cut": ("cut", "cut"),
        "do": ("did", "done"),
        "draw": ("drew", "drawn"),
        "dream": ("dreamt", "dreamt"),
        "drink": ("drank", "drunk"),
        "drive": ("drove", "driven"),
        "eat": ("ate", "eaten"),
        "fall": ("fell", "fallen"),
        "feel": ("felt", "felt"),
        "find": ("found", "found"),
        "fly": ("flew", "flown"),
        "get": ("got", "got"),
        "give": ("gave", "given"),
        "go": ("went", "gone"),
        "grow": ("grew", "grown"),
        "have": ("had", "had"),
        "hear": ("heard", "heard"),
        "hit": ("hit", "hit"),
        "hold": ("held", "held"),
        "hurt": ("hurt", "hurt"),
        "keep": ("kept", "kept"),
        "know": ("knew", "known"),
        "learn": ("learnt", "learnt"),
        "leave": ("left", "left"),
        "lend": ("lent", "lent"),
        "lose": ("lost", "lost"),
        "make": ("made", "made"),
        "mean": ("meant", "meant"),
        "meet": ("met", "met"),
        "pay": ("paid", "paid"),
        "put": ("put", "put"),
        "read": ("read", "read"),
        "ride": ("rode", "ridden"),
        "ring": ("rang", "rung"),
        "run": ("ran", "run"),
        "say": ("said", "said"),
        "see": ("saw", "seen"),
        "sell": ("sold", "sold"),
        "send": ("sent", "sent"),
        "show": ("showed", "shown"),
        "shut": ("shut", "shut"),
        "sing": ("sang", "sung"),
        "sit": ("sat", "sat"),
        "sleep": ("slept", "slept"),
        "speak": ("spoke", "spoken"),
        "spend": ("spent", "spent"),
        "stand": ("stood", "stood"),
        "steal": ("stole", "stolen"),
        "swim": ("swam", "swum"),
        "take": ("took", "taken"),
        "teach": ("taught", "taught"),
        "tell": ("told", "told"),
        "think": ("thought", "thought"),
        "throw": ("threw", "thrown"),
        "wake": ("woke", "woken"),
        "wear": ("wore", "worn"),
        "understand": ("understood", "understood"),
        "win": ("won", "won"),
        "write": ("wrote", "written"),
        "awake": ("awoke", "awoken"),
        "beat": ("beat", "beaten"),
        "bite": ("bit", "bitten"),
        "bleed": ("bled", "bled"),
        "blow": ("blew", "blown"),
        "burn": ("burnt", "burnt"),
        "dig": ("dug", "dug"),
        "feed": ("fed", "fed"),
        "fight": ("fought", "fought"),
        "forget": ("forgot", "forgotten"),
        "forgive": ("forgave", "forgiven"),
        "freeze": ("froze", "frozen"),
        "hang": ("hung", "hung"),
        "hide": ("hid", "hidden"),
        "let": ("let", "let"),
        "lie": ("lay", "lain"),
        "quit": ("quit", "quit"),
        "rise": ("rose", "risen"),
        "shake": ("shook", "shaken"),
        "shine": ("shone", "shone"),
        "shoot": ("shot", "shot"),
        "sink": ("sank", "sunk"),
        "stick": ("stuck", "stuck"),
        "strike": ("struck", "struck"),
        "tear": ("tore", "torn"),
        "bear": ("bore", "borne"),
        "bend": ("bent", "bent"),
        "breed": ("bred", "bred"),
        "cast": ("cast", "cast"),
        "deal": ("dealt", "dealt"),
        "forbid": ("forbade", "forbidden"),
        "lead": ("led", "led"),
        "seek": ("sought", "sought"),
        "set": ("set", "set"),
        "shrink": ("shrank", "shrunk"),
        "slide": ("slid", "slid"),
        "split": ("split", "split"),
        "spread": ("spread", "spread"),
        "swear": ("swore", "sworn"),
        "sweep": ("swept", "swept"),
        "swing": ("swung", "swung"),
        "arise": ("arose", "arisen"),
        "bet": ("bet", "bet"),
        "flee": ("fled", "fled"),
        "lay": ("laid", "laid"),
        "spin": ("spun", "spun"),
        "stink": ("stank", "stunk"),
        "bind": ("bound", "bound"),
        "cling": ("clung", "clung"),
        "creep": ("crept", "crept"),
        "fling": ("flung", "flung"),
        "forsake": ("forsook", "forsaken"),
        "foretell": ("foretold", "foretold"),
        "grind": ("ground", "ground"),
        "saw": ("sawed", "sawn"),
        "shed": ("shed", "shed"),
        "slay": ("slew", "slain"),
        "sling": ("slung", "slung"),
        "spring": ("sprang", "sprung"),
        "sting": ("stung", "stung"),
        "strive": ("strove", "striven"),
        "tread": ("trod", "trodden"),
        "weep": ("wept", "wept"),
        "wind": ("wound", "wound"),
        "wring": ("wrung", "wrung"),
        "chide": ("chid", "chidden"),
        "cleave": ("clove", "cloven"),
        "gird": ("girt", "girt"),
        "mistake": ("mistook", "mistaken"),
        "overhear": ("overheard", "overheard"),
        "sow": ("sowed", "sown"),
        "upset": ("upset", "upset"),
        "backslide": ("backslid", "backslidden"),
        "behold": ("beheld", "beheld"),
        "bestride": ("bestrode", "bestridden"),
        "bid": ("bade", "bidden"),
        "broadcast": ("broadcast", "broadcast"),
        "foresee": ("foresaw", "foreseen"),
        "gainsay": ("gainsaid", "gainsaid"),
        "interweave": ("interwove", "interwoven"),
        "miscast": ("miscast", "miscast"),
        "mislead": ("misled", "misled"),
        "overcome": ("overcame", "overcome"),
        "overdraw": ("overdrew", "overdrawn"),
        "overtake": ("overtook", "overtaken"),
        "partake": ("partook", "partaken"),
        "prepay": ("prepaid", "prepaid"),
        "proofread": ("proofread", "proofread"),
        "rebuild": ("rebuilt", "rebuilt"),
        "repay": ("repaid", "repaid"),
        "rewind": ("rewound", "rewound"),
        "smite": ("smote", "smitten"),
        "spit": ("spit", "spit"),
        "stride": ("strode", "stridden"),
        "sublet": ("sublet", "sublet"),
        "telecast": ("telecast", "telecast"),
        "unbend": ("unbent", "unbent"),
        "undergo": ("underwent", "undergone"),
        "undersell": ("undersold", "undersold"),
        "undertake": ("undertook", "undertaken"),
        "unwind": ("unwound", "unwound"),
        "withdraw": ("withdrew", "withdrawn"),
        "withhold": ("withheld", "withheld"),
        "withstand": ("withstood", "withstood"),
    }

    if v in irregular:
        past_simple, past_participle = irregular[v]
        return past_simple if form == 2 else past_participle

    vowels = set("aeiou")

    if v.endswith("e"):
        return v + "d"

    if v.endswith("y") and len(v) > 1 and v[-2] not in vowels:
        return v[:-1] + "ied"

    if (len(v) >= 3 and
            v[-1] not in vowels and v[-1] not in ("w", "x", "y") and
            v[-2] in vowels and
            v[-3] not in vowels):
        return v + v[-1] + "ed"

    return v + "ed"


def make_simple_sentence(mood: bool, verb: str, third_person: bool, subject: str, complement: str) -> str:
    """Obsługa Present Simple (Twierdzące/Przeczące)."""
    subj_cap = subject[0].upper() + subject[1:]

    if mood:
        final_verb = verb
        if third_person:
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

    else:
        aux = "does" if third_person else "do"
        return f"{subj_cap} {aux} not {verb} {complement}."


def make_simple_question(mood: bool, verb: str, third_person: bool, subject: str, complement: str) -> str:
    """Obsługa Present Simple (Pytania)."""
    aux = "Does" if third_person else "Do"

    if mood:
        return f"{aux} {subject} {verb} {complement}?"
    else:
        return f"{aux} {subject} not {verb} {complement}?"


def make_past_sentence(mood: bool, verb: str, subject: str, complement: str) -> str:
    """Obsługa Past Simple."""
    subj_cap = subject[0].upper() + subject[1:]

    if mood:
        v2 = form_of_verb(2, verb)
        return f"{subj_cap} {v2} {complement}."
    else:
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