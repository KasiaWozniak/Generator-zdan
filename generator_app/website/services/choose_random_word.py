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


def form_of_verb(form: int, verb: str) -> str:
    if form not in (2, 3):
        raise ValueError("form must be 2 or 3")

    if not verb or not isinstance(verb, str):
        raise ValueError("verb must be a non-empty string")

    v = verb.lower()

    irregular = {
        "be": ("was", "been"), # TODO: jeśli "was" pojawi się po "we", "you", "they" lub rzeczowniku w liczbie mnogiej to zmienić na "were"
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
        "sow": ("sowed", "sown, sowed"),
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


def random_verb_2():
    return form_of_verb(2, random_word("verbs"))


def random_verb_3():
    return form_of_verb(3, random_word("verbs"))
