import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content_mat import MAT
from content_eng import ENG, NAT, ENV
from content_len import LEN, SOC, FR, DIG
from content_vocab import VOCAB
from spelling_bee import SPELLING

OUT = os.path.join(os.path.dirname(__file__), "seed")
os.makedirs(OUT, exist_ok=True)
for _f in os.listdir(OUT):  # empezar limpio: así un tema borrado no queda viejo en la página
    if _f.endswith(".json"): os.remove(os.path.join(OUT, _f))
writes = []

def put(coll, did, data):
    path = os.path.join(OUT, f"{coll}__{did}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    writes.append({"op": "set", "collection": coll, "doc_id": did, "file_path": path})

# Fecha en que cada tema llegó desde Teams (los nuevos salen primero en el plan).
ADDED = {**{k: "2026-09-29" for k in ("s-nombres", "f-lieux", "f-temps", "f-valise", "f-activites", "f-jours", "d-word")},
         **{k: "2026-10-03" for k in ("l-verbo", "m-propiedades")},
         "m-mult2": "2026-10-06"}
order = 0
for group in (MAT, ENG, NAT, ENV, LEN, SOC, FR, DIG):
    for t in group:
        order += 1
        assert len(t["quiz"]) >= 3, t["id"]
        for q in t["quiz"]:
            assert 0 <= q[2] < len(q[1]), (t["id"], q[0])
        put("topics", t["id"], {
            "subject": t["s"], "quim": t["q"], "status": t["st"], "priority": t["p"],
            "title": t["t"], "kid": t["kid"], "points": t["pts"],
            "quiz": [dict({"q": q[0], "o": q[1], "a": q[2], "e": q[3]}, **({"listen": q[4]} if len(q) > 4 else {})) for q in t["quiz"]],
            "videos": [{"title": v[0], "yt": v[1]} for v in t.get("videos", [])],
            "listen": t.get("listen", []), "table": t.get("table"),
            "order": order, "added": ADDED.get(t["id"], "2026-09-26"), "source": "teams"})

for i, g in enumerate(VOCAB):
    put("vocab", g["id"], {"name": g["name"], "week": g["week"], "note": g.get("note", ""), "order": i,
        "words": [{"w": w[0], "es": w[1], "emoji": w[2], "type": w[3], "ex": w[4]} for w in g["words"]]})

ANIMALS = [
 ("butterfly", "🦋", "small and colorful", "two wings and six legs", "fly"),
 ("ladybug", "🐞", "small and red", "black spots and six legs", "fly"),
 ("bee", "🐝", "small, yellow and black", "two wings and six legs", "make honey"),
 ("ant", "🐜", "tiny and black", "six legs and two antennae", "carry food"),
 ("spider", "🕷️", "small and black", "eight legs", "make webs"),
 ("snail", "🐌", "slow", "a shell", "crawl"),
 ("worm", "🪱", "long and brown", "no legs", "dig in the soil"),
 ("caterpillar", "🐛", "long and green", "many legs", "eat leaves"),
 ("grasshopper", "🦗", "green", "six long legs", "jump very high"),
 ("frog", "🐸", "green", "four legs", "jump and swim"),
]
put("meta", "week", {"start": "2026-10-05", "end": "2026-10-09", "label": "Semana del 5 al 9 de octubre",
  "ing": {"goals": ["Jueves 8: Homework #3 — página 14 del Wellness Book",
                    "Jueves 8: Homework #4 — leer en Highlights los libros #9 «The Ghost Room» y #10 «Ray's Rough Day»",
                    "Repasar: Unit 5 (12 animales) y was / were / wasn't / weren't",
                    "Siempre: pronouns, present simple y present continuous"],
          "topics": ["e-garden", "e-waswere", "e-spelling", "e-pronouns", "e-simple", "e-continuous"],
          "vocab": ["garden", "animalparts", "describe"]},
  "animals": [{"w": a[0], "emoji": a[1], "is": a[2], "has": a[3], "can": a[4]} for a in ANIMALS]})

put("meta", "spelling", {"title": "4th Grade Spelling Bee Study List", "words": SPELLING})

events = [
 ("ev-1006-stem", "2026-10-06", "nat", "otro", "AquaMisión: ¡Que no se hunda! (School Projects)",
  "Proyecto STEM: construir en grupo un barquito que flote y lleve carga. Llevar papel aluminio, unidades de carga iguales (monedas, pompones o fichas), una hoja, lápiz y algo de color verde.", []),
 ("ev-1007-soc", "2026-10-07", "soc", "leccion", "Lección #1 de Sociales (9:30)",
  "Temas: «Muchas provincias juntas hacen nuestro país» y «¿Cómo se llaman las provincias del Ecuador?». La profe pide estudiar el Trabajo individual y la Tarea #1.", ["s-nombres", "s-provincias"]),
 ("ev-1007-nat", "2026-10-07", "nat", "tarea", "Natural Science: llevar impresa la hoja «Human Body Worksheet 1st part»",
  "Tarea «Coeducation» de Miss Sheyla: «Please bring the following worksheet!». Vence el miércoles 7 a las 7:30.", []),
 ("ev-1008-mat", "2026-10-08", "mat", "tarea", "Tarea N°3 de Matemática (en hojas de carpeta, NO imprimir)",
  "Propiedad conmutativa, asociativa y distributiva; multiplicaciones por una cifra (como 22 × 3) y 2 problemas. Se entrega en la hora de clase, el jueves 8. Debe hacerla él solo, con buena letra y números claros.", ["m-propiedades", "m-mult2", "m-probmult"]),
 ("ev-1008-hw3", "2026-10-08", "ing", "tarea", "Homework #3: Wellness Book pág. 14", "Language Arts. Vence el jueves 8 a las 7:00.", []),
 ("ev-1008-hw4", "2026-10-08", "ing", "tarea", "Homework #4: Highlights (libros #9 y #10)", "Leer en la plataforma Highlights: «The Ghost Room» y «Ray's Rough Day». Vence el jueves 8 a las 7:00.", []),
 ("ev-0928-oral", "2026-09-28", "ing", "exposicion", "Oral presentation: My Garden Animal",
  "Llevar plastilina de colores. Modelar un animal del jardín y decir 5 frases (This is… It is… It has… It can… It lives in…). 10 puntos.", ["e-garden"]),
 ("ev-0930-soc", "2026-09-30", "soc", "tarea", "Trabajo individual N°2 de Sociales (en clase)",
  "Llevar en la carpeta los anexos «¿Cómo se llaman las provincias?». Temas: origen del nombre de las provincias, apodos de Quito, Ambato, Portoviejo y Machala, provincias con nombres de ríos y de volcanes.", ["s-nombres", "s-provincias"]),
 ("ev-0930-nat", "2026-09-30", "nat", "tarea", "Human Body worksheet (llevarla impresa)",
  "Hoja del esqueleto: nombres de los huesos (skull, sternum, rib, vertebra, humerus, radius, ulna, pelvis, femur, patella, tibia, fibula) y verdadero o falso.", ["n-skeleton"]),
 ("ev-0930-spell", "2026-09-30", "ing", "otro", "Spelling Bee (sin nota)",
  "Te pedirán deletrear una palabra de la lista de 200 palabras (4th Grade Spelling Bee Study List).", ["e-spelling"]),
 ("ev-0929-len", "2026-09-29", "len", "leccion", "Lección #1 de Lengua",
  "Temas de la lección (canal 5. EVALUACIONES): el catálogo y sus características, juego de roles y pronombres personales. Pronombres aún no se vio en clase: repasarlo en casa.", ["l-catalogo", "l-roles", "l-pronombres"]),
 ("ev-1001-quiz", "2026-10-01", "ing", "leccion", "Written Quiz de Language Arts",
  "Unit 5: 12 animales (ant, bat, bee, beetle, butterfly, frog, hedgehog, lizard, owl, rabbit, snail, spider), can jump / can fly / doesn't have legs, y was / were / wasn't / weren't.", ["e-garden", "e-waswere", "e-instrucciones"]),
 ("ev-1001-mat", "2026-10-01", "mat", "tarea", "Tarea N°2 de Matemática (en hojas de carpeta)",
  "Multiplicación: completar espacios, relacionar cada multiplicación con su resultado, grupos iguales, factor que falta y problemas (datos, operación, respuesta). Se entrega en la hora clase.", ["m-mult", "m-probmult"]),
 ("ev-1002-mat", "2026-10-02", "mat", "leccion", "Lección semanal N°1 de Matemática",
  "La multiplicación (concepto, términos, suma abreviada), graficar monedas según su valor, problemas de razonamiento.", ["m-mult", "m-monedas", "m-probmult"]),
]
PRIO = {"ev-1008-mat": 1, "ev-1008-hw3": 2, "ev-1008-hw4": 3, "ev-0930-soc": 1, "ev-0930-nat": 2, "ev-0930-spell": 3, "ev-1001-quiz": 1, "ev-1001-mat": 2}
for eid, d, s, k, title, detail, tops in events:
    doc = {"date": d, "subject": s, "kind": k, "title": title, "detail": detail, "topics": tops, "done": d < "2026-10-06", "prio": PRIO.get(eid, 5)}
    if "e-spelling" in tops: doc["spell"] = True
    put("events", eid, doc)

# Datos privados (pendientes de papás, notas, horario, registro): NO van en el repositorio público.
# Viven en private.json (copia en Google Drive). Si no existe, se genera sin ellos.
PRIV = os.path.join(os.path.dirname(__file__), "private.json")
if os.path.exists(PRIV):
    priv = json.load(open(PRIV, encoding="utf-8"))
    for tid, doc in priv.get("todos", {}).items():
        put("todos", tid, doc)
    for k, doc in priv.get("meta", {}).items():
        put("meta", k, doc)
else:
    import datetime
    put("meta", "info", {"lastUpdate": datetime.date.today().isoformat(), "note": "", "log": []})

json.dump(writes, open(os.path.join(os.path.dirname(__file__), "writes.json"), "w"), ensure_ascii=False, indent=0)
print(len(writes), "writes;", order, "topics")
