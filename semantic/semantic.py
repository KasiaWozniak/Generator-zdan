import json
from collections import defaultdict
import spacy
import textacy
from textacy import extract
from spacy.cli import download as spacy_download

try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    spacy_download("en_core_web_lg")
    nlp = spacy.load("en_core_web_lg")


def get_generalized_text(tokens):
    mapping = {
        "PERSON": "person",
        "GPE": "city",
        "ORG": "company",
        "FAC": "building",
        "DATE": "time"
    }
    found_mapping = None
    # Szukamy, czy którykolwiek z tokenów w liście ma przypisaną kategorię NER
    for tok in tokens:
        if tok.text[0].isupper() and not tok.is_sent_start:
            if tok.ent_type_ in mapping:
                found_mapping = mapping[tok.ent_type_]
            else:
                return None
        elif tok.is_sent_start and tok.ent_type_ in mapping:
            found_mapping = mapping[tok.ent_type_]
    if found_mapping:
        return found_mapping

    token_indices = {t.i for t in tokens}
    root_token = tokens[0]
    for t in tokens:
        if t.head.i not in token_indices:
            root_token = t
            break
    # Jeśli nie znaleziono nazwy własnej, zwracamy połączone lematy (np. "the", "snail")
    return root_token.lemma_


def extract_svo_relations(files):
    group = files[0].split('/')[0]
    print("Group", group)
    knowledge_base = defaultdict(lambda: defaultdict(set))
    for path in files:
        print("Path", path)
        try:
            with open(path, 'r', encoding="utf8") as f:
                text = f.read()
        except FileNotFoundError:
            continue

        doc = nlp(text)
        svo_list = list(textacy.extract.subject_verb_object_triples(doc))

        for subj, verb, obj in svo_list:
            subj_text = get_generalized_text(subj)
            verb_text = " ".join(tok.lemma_ for tok in verb)
            obj_text = get_generalized_text(obj)
            if subj_text is None or obj_text is None:
                continue
            if len(verb_text.split()) == 1 and subj_text.islower():
                knowledge_base[subj_text][verb_text].add(obj_text)

    final_data = {}
    for subj, verbs in knowledge_base.items():
        final_data[subj] = {v: list(objs) for v, objs in verbs.items()}

    with open(f"{group}_knowledge_base.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)


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
    'B1_B2/HarryPotter5_2.txt',
    'B1_B2/HarryPotter6.txt',
    'B1_B2/HarryPotter7.txt',
    'B1_B2/HarryPotter7_2.txt',
]

files_B2_C1 = [
    'B2_C1/ManCalledOve.txt',
    'B2_C1/Level3.txt',
    'B2_C1/TheHobbit.txt',
    'B2_C1/OfMiceAndMen.txt',
]

extract_svo_relations(files_A2_B1)
extract_svo_relations(files_B1_B2)
extract_svo_relations(files_B2_C1)
