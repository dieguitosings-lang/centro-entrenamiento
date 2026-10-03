"""Incrusta en index.html las imágenes (SVG) de todos los emojis que usa la plataforma.
Así se ven iguales y nítidas en cualquier dispositivo (Windows, tablet Fire, iPad), aunque
el sistema no tenga ese emoji. Imágenes: Twemoji (CC-BY 4.0) + 3 dibujos propios."""
import re, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TW = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "twemoji")
if not os.path.isdir(TW) or not os.listdir(TW):
    # Descarga las imágenes de Twemoji desde npm la primera vez (no se guardan en el repositorio).
    import subprocess, tarfile, glob as _g
    os.makedirs(TW, exist_ok=True)
    subprocess.run(["npm", "pack", "@twemoji/svg@15.0.0", "--silent"], cwd=TW, check=True)
    tgz = _g.glob(os.path.join(TW, "*.tgz"))[0]
    with tarfile.open(tgz) as tf:
        for m in tf.getmembers():
            if m.name.endswith(".svg"):
                m.name = os.path.basename(m.name); tf.extract(m, TW)
    os.remove(tgz)
from content_vocab import VOCAB

CUSTOM = {
 "#antennae": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'><path d='M14 20C12 11 8 6 4 5M22 20C24 11 28 6 32 5' fill='none' stroke='#3B2A1A' stroke-width='2.4' stroke-linecap='round'/><circle cx='4' cy='5' r='3' fill='#F4900C'/><circle cx='32' cy='5' r='3' fill='#F4900C'/><ellipse cx='18' cy='26' rx='9' ry='8' fill='#8B5A2B'/><circle cx='14.5' cy='24.5' r='2' fill='#fff'/><circle cx='21.5' cy='24.5' r='2' fill='#fff'/><circle cx='14.8' cy='24.8' r='1' fill='#292F33'/><circle cx='21.8' cy='24.8' r='1' fill='#292F33'/></svg>",
 "#stomach": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'><path d='M13 3c0 5 1 8 4 10 5-2 12 0 14 7 2 8-4 14-12 14-6 0-10-3-12-7-1-3 2-5 4-3 2 3 5 4 8 3 4-2 3-8-1-9-3-1-5 0-7-2-3-3-3-8-3-13z' fill='#F4ABBA' stroke='#C2185B' stroke-width='1.6' stroke-linejoin='round'/><path d='M19 20c3 0 5 2 5 5' fill='none' stroke='#C2185B' stroke-width='1.4' stroke-linecap='round'/></svg>",
 "#skeleton": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'><g fill='none' stroke='#8899A6' stroke-width='3' stroke-linecap='round'><path d='M18 11v13M11 14.5h14M11.5 18h13M12.5 21.5h11M12 14l-6 8M24 14l6 8M18 24l-5 10M18 24l5 10'/></g><circle cx='18' cy='6' r='5.5' fill='#E1E8ED' stroke='#8899A6' stroke-width='2'/><circle cx='16' cy='5.6' r='1.3' fill='#292F33'/><circle cx='20' cy='5.6' r='1.3' fill='#292F33'/></svg>",
 "#spine": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'><path d='M18 2v32' stroke='#F4C542' stroke-width='3' stroke-linecap='round'/><g fill='#F5E1C0' stroke='#B08954' stroke-width='1.5'><rect x='12' y='2.5' width='12' height='4.2' rx='2'/><rect x='11.5' y='8.2' width='13' height='4.4' rx='2.1'/><rect x='11' y='14.1' width='14' height='4.6' rx='2.2'/><rect x='11' y='20.2' width='14' height='4.6' rx='2.2'/><rect x='11.5' y='26.3' width='13' height='4.4' rx='2.1'/></g><g stroke='#B08954' stroke-width='1.5' stroke-linecap='round'><path d='M12 4.6H8.5M24 4.6h3.5M11.5 10.4H8M24.5 10.4H28M11 16.4H7.5M25 16.4h3.5M11 22.5H7.5M25 22.5h3.5M11.5 28.5H8M24.5 28.5H28'/></g></svg>",
 "#neuron": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'><g fill='none' stroke='#D6336C' stroke-width='2' stroke-linecap='round'><path d='M9 12L4 6M9 12L2 13M10 16l-5 6M13 9l-1-6M15 10l5-6'/><path d='M16 16c6 3 9 6 12 12'/><path d='M28 28l5 1M28 28l1 5M28 28l4-3'/></g><circle cx='12' cy='13' r='5.5' fill='#FFB3C7' stroke='#D6336C' stroke-width='2'/><circle cx='12' cy='13' r='2' fill='#D6336C'/><path d='M22 5l-2 5h3l-2 5' fill='none' stroke='#F4900C' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'/></svg>",
 "#ribcage": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'><rect x='16.5' y='3' width='3' height='30' rx='1.5' fill='#8899A6'/><g fill='none' stroke='#99AAB5' stroke-width='3' stroke-linecap='round'><path d='M16 8c-6 0-10 2-11 5M20 8c6 0 10 2 11 5M16 13c-6 0-9 2-10 5M20 13c6 0 9 2 10 5M16 18c-5 0-8 2-9 5M20 18c5 0 8 2 9 5M16 23c-4 0-6 1.5-7 4M20 23c4 0 6 1.5 7 4'/></g></svg>",
}
pat = re.compile(r'(?:[\U0001F000-\U0001FAFF☀-➿⬀-⯿⌀-⏿](?:️)?(?:‍[\U0001F000-\U0001FAFF☀-➿](?:️)?)*)')

def code(e):
    cps = [f"{ord(c):x}" for c in e]
    if "200d" not in cps:
        cps = [c for c in cps if c != "fe0f"]
    return "-".join(cps)

used = set()
for g in VOCAB:
    for w in g["words"]:
        used.add(w[2])
src = open(os.path.join(HERE, "build_seed.py"), encoding="utf-8").read()
used |= set(pat.findall(src.split("ANIMALS = [")[1].split("]\n")[0]))
page = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
body = re.sub(r"/\*EMO_START\*/.*?/\*EMO_END\*/", "", page, flags=re.S)
bl = body.split("function badgeList")[1].split("];")[0]
used |= set(pat.findall(bl))
used |= {"🔒", "🏀"}
for f in ("content_eng.py", "content_mat.py", "content_len.py"):
    used |= set(pat.findall(open(os.path.join(HERE, f), encoding="utf-8").read()))

def uri(svg):
    svg = re.sub(r"\s+", " ", svg).replace('"', "'")
    for a, b in (("%", "%25"), ("#", "%23"), ("<", "%3C"), (">", "%3E"), ("\n", " ")):
        svg = svg.replace(a, b)
    return "data:image/svg+xml," + svg

emo, missing = {}, []
for e in sorted(used):
    if e in CUSTOM:
        emo[e] = uri(CUSTOM[e]); continue
    f = os.path.join(TW, code(e) + ".svg")
    if os.path.exists(f):
        emo[e.replace("️", "")] = uri(open(f, encoding="utf-8").read())
    else:
        missing.append(e)
if missing:
    sys.exit("Sin imagen para: " + " ".join(missing))
block = "/*EMO_START*/const EMO=" + json.dumps(emo, ensure_ascii=False) + ";/*EMO_END*/"
if "/*EMO_START*/" in page:
    page = re.sub(r"/\*EMO_START\*/.*?/\*EMO_END\*/", lambda m: block, page, flags=re.S)
else:
    page = page.replace("/* ============ utils ============ */", block + "\n/* ============ utils ============ */", 1)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
print(len(emo), "imágenes,", sum(len(v) for v in emo.values()) // 1024, "KB")
