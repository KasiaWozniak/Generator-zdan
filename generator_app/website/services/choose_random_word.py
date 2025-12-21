import json
import os
import random
from typing import Dict, List, Any

# Cache do przechowywania załadowanych baz wiedzy, aby nie czytać pliku przy każdym żądaniu
_KB_CACHE: Dict[str, Dict[str, Dict[str, List[str]]]] = {}


def _kb_path_for_level(level: str) -> str:
    # Zakładamy, że pliki są w folderze semantic poziom wyżej, zgodnie z Twoją strukturą
    # Dostosuj ścieżkę "../semantic" jeśli struktura folderów jest inna
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join("..\semantic", f"{level}_knowledge_base.json")


def load_knowledge(level: str) -> Dict[str, Any]:
    """
    Ładuje plik JSON dla danego poziomu.
    Struktura: { subject: { verb: [objects...] } }
    """
    if level in _KB_CACHE:
        return _KB_CACHE[level]

    path = _kb_path_for_level(level)
    if not os.path.exists(path):
        # Fallback - próbujemy szukać lokalnie lub rzucamy błąd
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
    """Zwraca listę wszystkich kluczy (podmiotów) dostępnych na danym poziomie."""
    data = load_knowledge(level)
    return list(data.keys())


def verbs_for_subject(subject_key: str, level: str) -> List[str]:
    """Zwraca listę czasowników dla danego klucza podmiotu."""
    data = load_knowledge(level)
    return list(data.get(subject_key, {}).keys())


def random_verb(subject_key: str, level: str) -> str:
    """Losuje czasownik pasujący do podmiotu."""
    verbs = verbs_for_subject(subject_key, level)
    if not verbs:
        raise ValueError(f"Brak czasowników dla podmiotu '{subject_key}' na poziomie {level}")
    return random.choice(verbs)


def objects_for_subject_verb(subject_key: str, verb: str, level: str) -> List[str]:
    """Zwraca listę dopełnień dla pary podmiot-czasownik."""
    data = load_knowledge(level)
    return data.get(subject_key, {}).get(verb, [])


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

    # zakończenie na 'e'
    if v.endswith("e"):
        return v + "d"

    # zakończenie na 'y' po spółgłosce -> 'ied'
    if v.endswith("y") and len(v) > 1 and v[-2] not in vowels:
        return v[:-1] + "ied"

    # podwajanie spółgłoski dla krótkich czasowników
    if (len(v) >= 3 and
            v[-1] not in vowels and v[-1] not in ("w", "x", "y") and
            v[-2] in vowels and
            v[-3] not in vowels):
        return v + v[-1] + "ed"

    # domyślny przypadek
    return v + "ed"