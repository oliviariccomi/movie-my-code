#!/usr/bin/env python3
"""Screenshot one scene of a Motion film outside the player, with a stub kit.

Usage:
  python3 preview.py --css base.css --shared shared.js --scene scene-flow.js --id flow --at 3.2 12 24 --out shots/

Save the three documents from the film's database (db_get) to files first. The stub kit
covers seg, eo, eio, eob, lerp, streamed and TextFx.fadeFromRight; if the scene uses
another kit function, add it to KIT below. Needs Playwright with Chromium; without it the
script writes the harness page and tells you to open it in a browser and call renderAt(t).
"""
import argparse, os, pathlib, re, sys

KIT = r"""
var seg=(t,a,b)=>t<=a?0:t>=b?1:(t-a)/(b-a), eo=(x)=>1-Math.pow(1-x,3), eio=(x)=>0.5-0.5*Math.cos(Math.PI*x),
    eob=(x,k)=>{k=k||1.5;const s=k;return x<=0?0:x>=1?1:1+(--x)*x*((s+1)*x+s);}, lerp=(a,b,q)=>a+(b-a)*q,
    streamed=(text,t,t0,cps)=>t<t0?'':text.slice(0,Math.floor((t-t0)*cps));
var TextFx={fadeFromRight(el,t,t0){const a=eo(seg(t,t0,t0+0.6));el.style.opacity=a;el.style.transform='translateX('+lerp(24,0,a).toFixed(1)+'px)';}};
var scenes={};
var kit={seg,eo,eio,eob,lerp,streamed,TextFx,stage:document.getElementById('stage'),scene(id,def){scenes[id]=def;},h(html){const d=document.createElement('div');d.innerHTML=html;return d.firstElementChild;},css(text){const st=document.createElement('style');st.textContent=text;document.head.appendChild(st);}};
window.kit=kit; window.scenes=scenes;
"""

PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}
html,body{{margin:0;background:#000}} #stage{{position:relative;width:1920px;height:1080px;overflow:hidden;--sans:Inter,system-ui,sans-serif;--mono:'DM Mono',ui-monospace,monospace}}</style></head>
<body><div id="stage"></div>
<script>{kit}</script>
<script>{shared}</script>
<script>{scene}</script>
<script>var sc=scenes['{id}']; sc.init(kit); window.renderAt=(t)=>sc.render(t);</script>
</body></html>"""

def strip_kit_destructuring(src):
    # the scene's first line `const { seg, eo, ... } = kit;` would collide with the stub globals
    return re.sub(r"^\s*const\s*\{[^}]*\}\s*=\s*kit;\s*", "// kit globals provided by the harness\n", src, count=1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--css", required=True); ap.add_argument("--shared", required=True)
    ap.add_argument("--scene", required=True); ap.add_argument("--id", required=True)
    ap.add_argument("--at", nargs="+", type=float, required=True); ap.add_argument("--out", default="shots")
    a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    page = PAGE.format(css=open(a.css).read(), kit=KIT, shared=open(a.shared).read(),
                       scene=strip_kit_destructuring(open(a.scene).read()), id=a.id)
    html = out / f"preview-{a.id}.html"; html.write_text(page)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(f"Playwright not installed: open {html} in a browser and call renderAt(t) in the console."); return
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(html.resolve().as_uri()); pg.wait_for_timeout(400)
        if errors:
            print("page errors (add the missing kit function to KIT, or fix the scene):"); [print("  ", e) for e in errors]; b.close(); return
        for t in a.at:
            pg.evaluate(f"renderAt({t})"); pg.wait_for_timeout(80)
            # two checks after each render: a drawing at the stage origin (a transform bug), and text blocks that overlap
            report = pg.evaluate("""() => {
              const visible = (e) => { for (let n = e; n && n.id !== 'stage'; n = n.parentElement) if (parseFloat(getComputedStyle(n).opacity) === 0) return false; return true; };
              const skip = (e) => e.id === 'stage' || ['HTML', 'BODY', 'svg'].includes(e.tagName) || ['ground', 'air', 'edge'].some(c => e.classList.contains(c));
              const big = (e) => { const r = e.getBoundingClientRect(); return r.width * r.height > 0.5 * 1920 * 1080; };   // a zoomed window may legitimately cover the origin
              const origin = document.elementsFromPoint(6, 6).filter(e => !skip(e) && visible(e) && !big(e)).map(e => e.tagName + '.' + (e.getAttribute('class') || (e.parentElement && e.parentElement.getAttribute('class')) || '?'));
              // text leaves: elements that own a text node, visible, with a real box
              const leaves = [...document.querySelectorAll('#stage *')].filter(e => visible(e) && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()))
                .map(e => ({ e, r: e.getBoundingClientRect(), t: e.textContent.trim().slice(0, 28) })).filter(o => o.r.width > 2 && o.r.height > 2 && o.r.left < 1920 && o.r.top < 1080);
              const inside = (a, b) => a.e.contains(b.e) || b.e.contains(a.e);
              const pairs = [];
              for (let i = 0; i < leaves.length; i++) for (let j = i + 1; j < leaves.length; j++) {
                const A = leaves[i].r, B = leaves[j].r;
                const w = Math.min(A.right, B.right) - Math.max(A.left, B.left), h = Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top);
                if (w > 4 && h > 4 && !inside(leaves[i], leaves[j])) pairs.push('"' + leaves[i].t + '" x "' + leaves[j].t + '"');
              }
              return { origin, pairs: pairs.slice(0, 8), more: Math.max(0, pairs.length - 8) };
            }""")
            hit = report['origin']; overlaps = report['pairs']
            shot = out / f"{a.id}-{t:g}s.png"; pg.screenshot(path=str(shot))
            msg = ""
            if hit: msg += f"   WARNING: something sits at the origin: {hit}"
            if overlaps: msg += f"   WARNING: text overlaps text: {overlaps}" + (f" (+{report['more']} more)" if report['more'] else "")
            print(f"{shot}{msg}")
        b.close()

if __name__ == "__main__":
    main()
