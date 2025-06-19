import json
import random
from pathlib import Path

# Load kamus.json (cleaned previously)
kamus_path = "/data/kamus.json"
with open(kamus_path, "r", encoding="utf-8") as f:
    kamus = json.load(f)

# Normalize kamus to lowercase keys and values (pick first translation)
kamus_norm = {}
for indo, osing in kamus.items():
    indo_clean = indo.strip().lower()
    osing_clean = osing.split(",")[0].strip().lower()
    kamus_norm[indo_clean] = osing_clean

# Template patterns and vocabulary
subjects = {
    "saya": "isun", "aku": "isun", "kamu": "riko", "dia": "yane",
    "bapak": "bapak", "ibu": "mak", "anak": "lare", "nenek": "embyah", "mereka": "wong-wong"
}

verbs = {
    "melihat": "ndeleng", "membawa": "nggowo", "mengambil": "njuwut",
    "memasak": "ngolah", "menyapu": "nyapu", "mencium": "ngambung",
    "memanggil": "ngundang", "memukul": "nyampat", "menyimpan": "nyimpen"
}

objects = {
    "air": "byanyu", "bunga": "kembang", "pisau": "lading", "anak": "lare",
    "sayur": "jangan", "nasi": "sek", "buku": "buku", "pisang": "gedhang", "kunci": "kunci"
}

locations = {
    "dapur": "pawon", "pasar": "pasar", "rumah": "umah", "sungai": "kali", "bukit": "puthuk"
}

# Sentence patterns (Indonesia, Osing)
patterns = [
    ("{subj} {verb} {obj}", "{subj_o} {verb_o} {obj_o}"),
    ("{subj} {verb} {obj} di {loc}", "{subj_o} {verb_o} {obj_o} nong {loc_o}"),
    ("{subj} {verb} {obj} dari {loc}", "{subj_o} {verb_o} {obj_o} teko {loc_o}"),
    ("{subj} {verb} {obj} ke {loc}", "{subj_o} {verb_o} {obj_o} nyang {loc_o}"),
]

# Generate accurate translations
output = []
for _ in range(5000):
    pattern_indo, pattern_osing = random.choice(patterns)

    subj = random.choice(list(subjects.keys()))
    verb = random.choice(list(verbs.keys()))
    obj = random.choice(list(objects.keys()))
    loc = random.choice(list(locations.keys()))

    indo_sentence = pattern_indo.format(subj=subj, verb=verb, obj=obj, loc=loc)
    osing_sentence = pattern_osing.format(
        subj_o=subjects[subj], verb_o=verbs[verb], obj_o=objects[obj], loc_o=locations[loc]
    )
    output.append((indo_sentence, osing_sentence))

# Save to CSV
output_path = "/mnt/data/korpus_paralel_indo_osing_benar.csv"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("indonesia,osing\n")
    for indo, osing in output:
        f.write(f"\"{indo}\",\"{osing}\"\n")

output_path
