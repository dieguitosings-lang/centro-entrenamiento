"""Genera versiones HTML independientes del Centro de Entrenamiento (sin claude.ai).
   python3 build_standalone.py            -> dist/centro-thiago.html (completo, privado)
   python3 build_standalone.py --public   -> dist/public/index.html (sin datos personales, para GitHub Pages)
"""
import json, glob, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = "--public" in sys.argv

data = {}
for f in sorted(glob.glob(os.path.join(HERE, "seed", "*.json"))):
    c, d = os.path.basename(f)[:-5].split("__")
    data.setdefault(c, {})[d] = json.load(open(f, encoding="utf-8"))

page = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()

def rep(a, b, count=1):
    global page
    assert a in page, a[:80]
    page = page.replace(a, b, count)

if PUBLIC:
    for k in ("todos",):
        data.pop(k, None)
    data.get("meta", {}).pop("grades", None)
    data.get("meta", {}).pop("schedule", None)
    if "info" in data.get("meta", {}):
        data["meta"]["info"] = {"lastUpdate": data["meta"]["info"]["lastUpdate"], "note": "", "log": []}
    txt = json.dumps(data, ensure_ascii=False)
    # El nombre de Thiago se mantiene (pedido de Diego); el de su hermana se cambia.
    _d = "Dan" + "na"; txt = txt.replace(_d, "Ana")
    data = json.loads(txt)
    rep("<title>Centro de Entrenamiento Thiago</title>", "<title>Centro de Entrenamiento</title>")
    rep('Explicación corta para Thiago', 'Explicación corta para el niño')
    rep('dile a Claude: <b>«actualiza el centro de Thiago»</b>', 'se genera una versión nueva del archivo')

# local database shim with the same API as the claude.ai db capability
shim = r'''
function localDB(BASE){
  const KEY="tc_db_v1";let ov={};try{ov=JSON.parse(localStorage.getItem(KEY)||"{}")||{}}catch(e){ov={}}
  const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(ov))}catch(e){}};
  const subs={};
  const coll=c=>{const o=Object.assign({},BASE[c]||{},ov[c]||{});Object.keys(o).forEach(k=>{if(o[k]===null)delete o[k]});return o};
  const snap=c=>{const docs=Object.entries(coll(c)).map(([id,v])=>({id,exists:true,data:()=>v}));return{docs,size:docs.length,empty:!docs.length}};
  const notify=c=>(subs[c]||[]).forEach(f=>{try{f(snap(c))}catch(e){}});
  const put=(c,id,v)=>{(ov[c]=ov[c]||{})[id]=v;save();notify(c)};
  return{
    collection(c){return{onSnapshot(f){(subs[c]=subs[c]||[]).push(f);setTimeout(()=>f(snap(c)),0);return()=>{}},async add(v){const id="local-"+Date.now().toString(36);put(c,id,JSON.parse(JSON.stringify(v)));return{id}}}},
    doc(p){const [c,id]=p.split("/");return{async get(){const v=coll(c)[id];return{exists:!!v,data:()=>v}},async set(v){put(c,id,JSON.parse(JSON.stringify(v)))},async update(v){const cur=coll(c)[id];if(!cur)throw{code:"invalid_argument"};put(c,id,Object.assign({},cur,v))}}},
    exportAll(){return JSON.stringify({app:"centro-entrenamiento",v:1,saved:new Date().toISOString(),ov},null,1)},
    importAll(txt){const d=JSON.parse(txt);if(!d||d.app!=="centro-entrenamiento"||!d.ov)throw new Error("archivo no válido");ov=d.ov;save()}
  };
}
const EMBED=__DATA__;
'''.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))

rep("/* ============ boot ============ */", shim + "/* ============ boot ============ */")
rep('let db=null;try{db=window.claude&&await window.claude.use("db")}catch(e){db=null}', 'const db=localDB(EMBED);S.local=db;')
rep('Abre esta página desde claude.ai para cargar los temas y guardar el progreso.', 'No se pudieron cargar los datos.')

# backup / restore section in Papás
backup = ('''h+='<section class="card" style="display:grid;gap:10px"><h2>Respaldo del progreso</h2><p class="muted small">El progreso se guarda en este dispositivo. Para pasarlo a otra tablet o computadora: descarga el respaldo aquí y cárgalo allá.</p><div class="row"><button class="btn small" id="bkDown">Descargar respaldo</button><label class="btn small ghost" for="bkUp" style="cursor:pointer">Cargar respaldo</label><input type="file" id="bkUp" accept=".json,application/json" hidden></div></section>';\n  ''')
rep("if(info.log&&info.log.length)h+=", backup + "if(info.log&&info.log.length)h+=")
bind = r'''main.innerHTML=h;
  const bd=$("#bkDown");if(bd)bd.onclick=()=>{try{const blob=new Blob([S.local.exportAll()],{type:"application/json"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="respaldo-centro-"+today()+".json";document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},500)}catch(e){toast("No se pudo descargar.")}};
  const bu=$("#bkUp");if(bu)bu.onchange=()=>{const f=bu.files&&bu.files[0];if(!f)return;const r=new FileReader();r.onload=()=>{try{S.local.importAll(r.result);toast("Respaldo cargado");setTimeout(()=>location.reload(),800)}catch(e){toast("Ese archivo no es un respaldo válido.")}};r.readAsText(f)};
  bindTopicButtons();
  main.querySelectorAll("[data-todo]")'''
rep('main.innerHTML=h;\n  bindTopicButtons();\n  main.querySelectorAll("[data-todo]")', bind)

m = re.match(r"\s*(<title>.*?</title>)", page, re.S)
title = m.group(1)
rest = page[m.end():]
style_end = rest.index("</style>") + len("</style>")
head_bits, body = rest[:style_end], rest[style_end:]
doc = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
       '<meta name="theme-color" content="#13213C">\n<meta name="apple-mobile-web-app-capable" content="yes">\n'
       + title + head_bits + "\n</head>\n<body>" + body + "\n</body>\n</html>\n")
if not PUBLIC:
    os.makedirs(os.path.join(HERE, "dist"), exist_ok=True)
    open(os.path.join(HERE, "dist", "centro-artifact.html"), "w", encoding="utf-8").write(title + head_bits + body)
out = os.path.join(HERE, "dist", "public" if PUBLIC else "")
os.makedirs(out, exist_ok=True)
fn = os.path.join(out, "index.html" if PUBLIC else "centro-thiago.html")
open(fn, "w", encoding="utf-8").write(doc)
print(fn, len(doc)//1024, "KB")
