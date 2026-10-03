"""Prueba la página construida en un navegador sin pantalla, con ancho de tablet (800x1280).
   python3 test_build.py                 -> prueba con la fecha de hoy
   python3 test_build.py 2026-10-06 ...  -> prueba simulando esas fechas (19:00 hora de Ecuador)
Imprime el plan de cada día y los errores de la página. Si hay errores, NO publicar."""
import asyncio, json, sys, os, datetime
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
URL = "file://" + os.path.join(HERE, "dist", "public", "index.html")
MOCK = """
window.__spoken=[];
const V=[{name:'Google US English',lang:'en-US',localService:false,voiceURI:'g'},{name:'Google español de Estados Unidos',lang:'es-US',localService:false,voiceURI:'ge'}];
window.SpeechSynthesisUtterance=function(t){this.text=t};
const SS={_q:[],getVoices:()=>V,addEventListener(){},cancel(){const q=this._q;this._q=[];q.forEach(u=>u.onerror&&u.onerror())},
 speak(u){this._q.push(u);setTimeout(()=>{const i=this._q.indexOf(u);if(i>=0){this._q.splice(i,1);u.onend&&u.onend()}},u.text.length*5)}};
Object.defineProperty(window,'speechSynthesis',{value:SS,configurable:true});
"""
def fake(iso):
    return "(()=>{const D=Date,off=new D('%s').getTime()-D.now();class F extends D{constructor(...a){if(a.length)super(...a);else super(D.now()+off)}static now(){return D.now()+off}};window.Date=F})();" % iso
PLAN = "()=>document.querySelector('.track')?('plan: '+__tc.S.plan.blocks.map(b=>b.kind+' · '+b.title).join(' / ')):('sin plan: '+document.querySelector('.hero h2').textContent)"
async def main(dates):
    bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else None)
        for d in dates:
            pg = await b.new_page(viewport={"width": 800, "height": 1280})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "TUNNEL" not in m.text and "net::" not in m.text else None)
            await pg.add_init_script(MOCK)
            if d: await pg.add_init_script(fake(d + "T19:00:00-05:00"))
            await pg.goto(URL); await pg.wait_for_timeout(900)
            print(d or "hoy", "->", await pg.evaluate(PLAN))
            for v in ["materias", "palabras", "poder", "hoy"]:
                await pg.click(f'nav.tabs button[data-view="{v}"]'); await pg.wait_for_timeout(150)
            await pg.click("#hudPapas"); await pg.wait_for_timeout(150)
            await pg.evaluate("()=>Object.keys(__tc.S.topics).forEach(id=>{__tc.openTopic(id)})")
            await pg.evaluate("()=>Object.keys(__tc.S.topics).filter(id=>(__tc.S.topics[id].quiz||[]).length).forEach(id=>__tc.startQuiz(id))")
            await pg.evaluate("()=>__tc.startDrill('mix')"); await pg.wait_for_timeout(100)
            if errs: bad += 1; print("   ERRORES:", errs)
            await pg.close()
        await b.close()
    print("OK, sin errores" if not bad else "HAY ERRORES: no publicar")
    sys.exit(1 if bad else 0)
args = sys.argv[1:] or [None]
asyncio.run(main(args))
