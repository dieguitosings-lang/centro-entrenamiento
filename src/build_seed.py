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
         "m-mult2": "2026-10-27",
         **{k: "2026-10-09" for k in ("l-conjugacion", "l-silaba", "s-autoridades")},
         **{k: "2026-10-14" for k in ("v-forces", "v-magnets", "s-tradiciones")},
         "m-azar": "2026-10-18", "s-turismo": "2026-10-20", "d-iconos": "2026-10-22", "l-teatro": "2026-10-23"}
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
put("meta", "week", {"start": "2026-10-26", "end": "2026-10-30", "label": "Semana del 26 al 30 de octubre",
  "ing": {"goals": ["Repasar: Unit 5 (12 animales) y was / were / wasn't / weren't",
                    "Siempre: pronouns, present simple y present continuous"],
          "topics": ["e-garden", "e-waswere", "e-spelling", "e-pronouns", "e-simple", "e-continuous"],
          "vocab": ["garden", "animalparts", "describe"]},
  "animals": [{"w": a[0], "emoji": a[1], "is": a[2], "has": a[3], "can": a[4]} for a in ANIMALS]})

put("meta", "spelling", {"title": "4th Grade Spelling Bee Study List", "words": SPELLING})

# Música (MÚSICA 4C): videos para practicar la melódica con el piano del centro.
put("meta", "musica", {"songs": [
  {"id": "piratas", "n": 2, "title": "Piratas del Caribe", "yt": "JwEJk_LC1JY", "key": "Re menor (Dm)", "added": "2026-10-28",
   "task": "Actividad asincrónica del 28/10: tocar con el video de la canción #2 durante 15 minutos, subiendo la velocidad poco a poco. Si hace falta, 1 minuto de pausa entre cada velocidad.",
   "plan": [{"r": 0.5, "min": 5}, {"r": 0.65, "min": 5}, {"r": 0.75, "min": 5}], "rest": 1}],
  "note": "La partitura «Piratas del caribe Dm» está en Teams (Música 4C, canal General)."})

events = [
 ("ev-1030-natquiz", "2026-10-30", "nat", "leccion", "Natural Science: Pop Quiz «The Digestive System» (formulario en Teams, vence 8:00)",
  "Tarea publicada el 28/10 (10 puntos, 1 solo envío). Es un formulario en línea que cuenta como taller acumulativo: leer bien cada pregunta, usar la presentación de PowerPoint publicada con la tarea, revisar las respuestas antes de enviar y completarlo dentro de las 48 horas. Se responde en Teams.", ["n-digestion"]),
 ("ev-1030-natasinc", "2026-10-30", "nat", "tarea", "Natural Science: Asynchronous Activity (Wordwall, vence 7:59)",
  "Abrir el enlace de Wordwall que está en la tarea de Teams, resolverlo y subir la captura de pantalla a la tarea.", ["n-digestion"]),
 ("ev-1030-hl", "2026-10-30", "ing", "tarea", "Language Arts: Highlights «Spaghetti Catastrophe» (vence 7:00)",
  "Asynchronous Class Activity: leer el libro en la plataforma Highlights y resolver las actividades. Se revisa en la plataforma y cuenta para la nota de deberes (Homework).", []),
 ("ev-1103-hl", "2026-11-03", "ing", "tarea", "Language Arts: Highlights «The Case of the Missing Left Shoe»",
  "Segundo libro de la misma tarea: leerlo en Highlights y resolver las actividades hasta el martes 3 de noviembre.", []),
 ("ev-1104-fr7", "2026-11-04", "fr", "tarea", "Francés: Tache «Activité 7: Les destinations de vacances» (vence 7:00)",
  "Completar la actividad 7, enviar la foto a la tarea en Teams y presentarla la próxima semana. 10 puntos. Primer ejercicio: escuchar y unir a cada niño con su destino de vacaciones (Liveworksheets). La profe adjuntó la hoja por si no la tiene.", ["f-lieux"]),
 ("ev-1104-socasinc", "2026-11-04", "soc", "tarea", "Sociales: Actividad asincrónica de la semana 27 (imprimir, vence 10:00)",
  "Imprimir y desarrollar la actividad; luego pegarla en el cuaderno o archivarla en la carpeta. Tema: frutas autóctonas y saludables de cada región natural del Ecuador (Sierra, Costa, Amazonía), el trabajo de los agricultores y la feria saludable. 10 puntos.", []),
 ("ev-1029-matasinc", "2026-10-29", "mat", "tarea", "Matemática: Actividad asincrónica (multiplicar por una cifra, vence 23:59)",
  "Tarea publicada el 27/10: «Realizar la actividad y subirla en el tiempo establecido». Hoja de 10 puntos del segundo parcial: 10 multiplicaciones de 3 cifras por 1 cifra y ubicar los factores en forma vertical (C, D, U) antes de resolver. Se resuelve en la hoja y se sube la foto a Teams.", ["m-mult2"]),
 ("ev-1029-lenfisico", "2026-10-29", "len", "tarea", "Lengua: presentar en físico las 2 hojas de las actividades asincrónicas",
  "Las dos actividades asincrónicas del 27/10 (separar palabras en sílabas y escribir la sílaba tónica) ya están subidas a Teams, pero la Miss pide presentar las hojas en físico para su revisión. No dice fecha: llevarlas a la próxima clase de Lengua.", ["l-silaba"]),
 ("ev-1030-batido", "2026-10-30", "len", "otro", "Proyecto «Sabores»: enviar ingredientes del batido de frutilla (Grupo 2)",
  "Comunicado del 23/10: la semana del 26 al 30 de octubre practican el proyecto en clase y termina con una exposición interna. Thiago está en el Grupo 2, «Batido de frutilla». Ingredientes para 2 porciones por grupo: leche, frutilla, azúcar, vasos, colador y licuadora. Hay que anotar el precio por unidad de cada producto (para calcular el costo del batido, con envases y logos). Cada grupo envía 30 recuerdos para los niños que visitan y 10 para las autoridades, con el logo adhesivo de su producto.", ["l-anuncio"]),
 ("ev-1026-proyecto", "2026-10-26", "len", "otro", "Semana del proyecto interdisciplinario «Sabores que forman parte de nuestra cultura» (26 al 30/10)",
  "Integra Lengua, Matemática y Sociales. Practican en grupos durante las clases y al final hay una exposición interna para compañeros y docentes. Repasar: anuncio publicitario (eslogan, adjetivos llamativos), precios y costos.", ["l-anuncio"]),
 ("ev-1027-mat5", "2026-10-27", "mat", "tarea", "Matemática: Tarea N°5 (en la carpeta, NO imprimir, vence 12:30)",
  "La profe la volvió a subir el 22/10 porque la pregunta 2 tenía un error. Se recibe el martes en clase. Temas: posibilidades al lanzar dos monedas, seguro / posible / imposible con un dado y tabla de frecuencia (conteo con rayitas).", ["m-azar"]),
 ("ev-1027-hl", "2026-10-27", "ing", "tarea", "Language Arts: Highlights Books (plataforma Highlights, vence 23:59)",
  "Leer en la plataforma Highlights los libros «When Cat and Rat Were Friends» y «Omar and the Camel».", []),
 ("ev-1026-lt5", "2026-10-26", "len", "tarea", "Lengua: Tarea #5 Sílaba tónica (vence 23:59)",
  "Copiar en el cuaderno, resolver las actividades, tomar foto y subirla a Teams.", ["l-silaba"]),
 ("ev-1020-dig", "2026-10-20", "dig", "leccion", "Computación: fichas de iconos de Word y lección",
  "Publicado el 13/10: fichas de cartulina de 10 × 5 cm, adelante el icono y atrás el nombre (cursiva, subrayado, tachado, subíndice, superíndice, resaltado, color, tamaño y tipo de letra, alinear izquierda, centrar, derecha, justificar). Presentar y dar lección «el próximo martes».", ["d-iconos"]),
 ("ev-1028-fr", "2026-10-28", "fr", "tarea", "Francés: Tache «Dossier: Activité 4» (presentar en la próxima clase, vence 7:00)",
  "Completar la actividad 4 en la carpeta (dossier) y presentarla en la próxima clase. La pregunta 1 se hace en clase. Tema: «Quel temps fait-il ?» (el clima): verdadero o falso con el mapa de Francia, qué tiempo hace cada día y qué tiempo hay según los dibujos. 10 puntos.", ["f-temps", "f-jours"]),
 ("ev-1021-nat", "2026-10-21", "nat", "tarea", "Natural Science: Worksheet 6 «The Digestion» (llevar impresa a la Coeducative Class, 7:00)",
  "Tarea «Coeducative Class»: imprimir la hoja «4TH NAT SCIENCE HUMAN BODY WORKSHEET 1ST PART-6» y llevarla. Tema: the digestion (el viaje de la comida y sus etapas).", ["n-digestion"]),
 ("ev-1021-socti5", "2026-10-21", "soc", "leccion", "Sociales: Trabajo individual N°5 «El turismo es superimportante» (llevar impreso, 8:00)",
  "Tarea «RECURSOS_SEMANA # 26»: llevar impresos el Trabajo individual N°5 y los anexos, con nombre y apellido. Tipos de turismo, verdadero o falso, Quito y Cuenca Patrimonio Cultural de la Humanidad.", ["s-turismo"]),
 ("ev-1026-pleno", "2026-10-26", "mat", "tarea", "Matemática: Actividad de refuerzo en PLENO (plataforma Santillana)",
  "Hacer la actividad en la plataforma Santillana. Se cierra el lunes 26 de octubre a las 23:59.", []),
 ("ev-1019-proyecto", "2026-10-19", "len", "otro", "Semana del proyecto interdisciplinario (Lengua, Matemática y Sociales)",
  "La Miss de Lengua avisó el 15/10 que esta semana harán un proyecto en grupos, pero con nota individual. Cuenta como la lección acumulativa del I parcial del II quimestre en las 3 materias. No publicaron el día exacto. Materiales: marcadores gruesos, lápices de colores, imágenes de productos agrícolas de las 4 regiones del Ecuador, tijeras y gomero. Comunicado del 22/10 (Sociales): se llama «Sabores que forman parte de nuestra cultura». Cada niño diseña, calcula y hace la publicidad de un producto saludable (un waffle o un snack nutritivo). Lengua: texto publicitario, adjetivos llamativos, eslogan, nombre de la marca y mensaje para el afiche. Sociales: origen de los ingredientes (frutas locales, maíz, quinua) y la comida de cada región. Matemática: porciones, figuras geométricas en los empaques, precios y encuestas sencillas.", []),
 ("ev-1020-env2", "2026-10-20", "env", "tarea", "Env. Science: Homework #2 Magnetics (Wordwall)",
  "Abrir el enlace de Wordwall que está en la tarea de Teams, resolverlo y publicar el puntaje en la tarea. Vence el martes 20 a las 7:00.", ["v-magnets"]),
 ("ev-1020-env1", "2026-10-20", "env", "tarea", "Env. Science: Homework #1 Forces: Push and Pull (Wordwall)",
  "Abrir el enlace de Wordwall que está en la tarea de Teams, resolverlo y publicar el puntaje en la tarea. 10 puntos. Vence el martes 20 a las 7:30.", ["v-forces"]),
 ("ev-1015-hw5", "2026-10-15", "ing", "tarea", "Language Arts: Homework #5 Listening (llevar la hoja impresa)",
  "Imprimir la hoja, escuchar los audios 5.1 y 5.2, resolverla y llevarla a clase. Cuenta como actividad de recuperación (pág. 66 del workbook). Vence el jueves 15 a las 7:00.", []),
 ("ev-1015-lt4", "2026-10-15", "len", "tarea", "Lengua: Tarea #4 (libro págs. 118, 119 y 120)",
  "Realizar las actividades del libro, tomar foto y subirla a Teams. Vence el jueves 15 a las 23:59.", []),
 ("ev-1014-ws4", "2026-10-14", "nat", "tarea", "Natural Science: Worksheet #4 (llevar impresa)",
  "«Please print the following page and bring it to class». Vencía el miércoles 14 a las 7:00.", []),
 ("ev-1014-socti4", "2026-10-14", "soc", "leccion", "Trabajo individual N°4 de Sociales (en clase)",
  "Tarea «Recursos»: llevar impresos el Trabajo individual N°4 y el anexo de la semana 25 con nombre y apellido, más goma en barra y tijeras. Temas: tradiciones, lugares y personajes emblemáticos de las provincias.", ["s-tradiciones"]),
 ("ev-1013-len", "2026-10-13", "len", "leccion", "Lección #2 de Lengua",
  "Temas (canal 5. EVALUACIONES): anuncio publicitario (concepto, elementos y ejemplos), el verbo y los tiempos verbales, y conjugar verbos con los pronombres personales. Ojo con las tildes.", ["l-anuncio", "l-verbo", "l-conjugacion", "l-pronombres"]),
 ("ev-1013-lt2", "2026-10-13", "len", "tarea", "Lengua: Tarea #2 El anuncio publicitario (libro págs. 112-113)",
  "La pág. 112 se hizo en clase; completar lo que falte. Vence el martes 13 a las 23:59.", ["l-anuncio"]),
 ("ev-1013-lt3", "2026-10-13", "len", "tarea", "Lengua: Tarea #3 El verbo y sus tiempos (en el cuaderno)",
  "Copiar los ejercicios en el cuaderno, resolverlos, tomar foto y subirla a Teams. Pronombres, verbos en presente y conjugación en pasado y futuro, con tildes. Vence el martes 13 a las 23:59.", ["l-conjugacion", "l-verbo", "l-pronombres"]),
 ("ev-1014-fr", "2026-10-14", "fr", "tarea", "Francés: Tache 1 (activité 1, pages 1-2)",
  "Completar la actividad 1, páginas 1 y 2 (la hoja está en su carpeta, tema «Mes vacances») y presentarla en la próxima clase. Vence el miércoles 14 a las 7:00.", ["f-lieux", "f-temps"]),
 ("ev-1014-soc", "2026-10-14", "soc", "tarea", "Tarea de Sociales: autoridades de la provincia (imprimir y pegar en el cuaderno)",
  "Mapa de autoridades provinciales (elegidas por votación y la que nombra el presidente), 3 responsabilidades, crucigrama de ciudades y recortar y pegar la bandera y el escudo de la provincia que más te gusta. Vence el miércoles 14 a las 8:30.", ["s-autoridades", "s-provincias"]),
 ("ev-1014-mat", "2026-10-14", "mat", "tarea", "Tarea N°4 de Matemática (en hojas de carpeta, NO imprimir)",
  "Completar productos de las tablas, propiedad asociativa, propiedad distributiva, 4 multiplicaciones de 3 cifras por 1 cifra y 2 problemas (datos, operación y respuesta). Con nombre y paralelo, buena letra y números claros. Ojo: la profe escribió que se recibe el miércoles 14 en clase, pero Teams dice jueves 15 a las 13:30. Tenerla lista el miércoles.", ["m-mult2", "m-propiedades", "m-probmult", "m-mult"]),
 ("ev-1016-pleno", "2026-10-16", "mat", "tarea", "Matemática: actividad en PLENO",
  "La profe pide enviar la actividad en PLENO hasta el viernes 16/10.", []),
 ("ev-1016-mat", "2026-10-16", "mat", "leccion", "Lección semanal N°2 de Matemática",
  "Temas: la multiplicación (concepto y términos), propiedades de la multiplicación (concepto y ejercicios), problemas de razonamiento y TABLAS DE MULTIPLICAR.", ["m-mult", "m-propiedades", "m-probmult", "m-mult2"]),
 ("ev-1008-soc", "2026-10-08", "soc", "tarea", "Sociales: llevar los anexos «Símbolos y autoridades de mi provincia» y el Trabajo individual",
  "Tarea «Recursos»: «Traer para mañana los siguientes archivos». Vencía el jueves 8 a las 8:00.", ["s-autoridades"]),
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
PRIO = {"ev-1030-natquiz": 1, "ev-1030-natasinc": 2, "ev-1030-hl": 3, "ev-1104-fr7": 1, "ev-1104-socasinc": 2, "ev-1029-matasinc": 1, "ev-1029-lenfisico": 2, "ev-1027-mat5": 1, "ev-1027-hl": 2, "ev-1028-fr": 1, "ev-1021-nat": 1, "ev-1021-socti5": 2, "ev-1020-env2": 1, "ev-1020-env1": 2, "ev-1015-hw5": 1, "ev-1015-lt4": 2, "ev-1014-socti4": 1, "ev-1013-len": 1, "ev-1013-lt3": 2, "ev-1013-lt2": 3, "ev-1014-soc": 1, "ev-1014-fr": 2, "ev-1014-mat": 3, "ev-1016-mat": 1, "ev-1016-pleno": 2, "ev-1008-mat": 1, "ev-1008-hw3": 2, "ev-1008-hw4": 3, "ev-0930-soc": 1, "ev-0930-nat": 2, "ev-0930-spell": 3, "ev-1001-quiz": 1, "ev-1001-mat": 2}
for eid, d, s, k, title, detail, tops in events:
    doc = {"date": d, "subject": s, "kind": k, "title": title, "detail": detail, "topics": tops, "done": d <= "2026-10-28" or eid in ("ev-1020-env1", "ev-1020-env2", "ev-1029-matasinc"), "prio": PRIO.get(eid, 5)}
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
