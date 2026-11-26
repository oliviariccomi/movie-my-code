# The world: base.css and shared.js

One world for the whole film. Put the four brand colors in `base.css`, mix every other tone
from them, and keep every recurring drawing in `shared.js` on `window.W`. The code below is
a working kit for a 1920 by 1080 film; change the four hex values and nothing else needs
to change.

## base.css

The first line holds the four colors as plain hex, each once (the player reads them to
offer palettes). Everything else is a mix of those four.

```css
#stage { --ground:#F5F5F7; --main:#2E5E8C; --second:#16213E; --accent:#E8742C; color:var(--second); font-family:var(--sans, system-ui, sans-serif);
  --card:var(--ground); --hair:color-mix(in srgb, var(--second) 16%, transparent); --shade:color-mix(in srgb, var(--second) 10%, transparent); --ink2:color-mix(in srgb, var(--second) 66%, var(--ground));
  --tint:color-mix(in srgb, var(--main) 10%, var(--ground)); --tint2:color-mix(in srgb, var(--main) 24%, var(--ground)); --lav:color-mix(in srgb, var(--main) 50%, var(--ground));
  --dark:var(--second); --dark2:color-mix(in srgb, var(--second) 80%, var(--main)); --dark3:color-mix(in srgb, var(--second) 88%, var(--ground)); --dark-hair:color-mix(in srgb, var(--ground) 22%, transparent); --dark-ink2:color-mix(in srgb, var(--ground) 62%, var(--second));
  --glow:color-mix(in srgb, var(--accent) 28%, transparent) }
.ground { position:absolute; inset:0; background:var(--ground) }
.air { position:absolute; inset:0; background:color-mix(in srgb, var(--ground) 94%, var(--main)) }
.art { position:absolute; left:0; top:0; overflow:visible }
.cam { position:absolute; left:0; top:0; width:1920px; height:1080px; transform-origin:0 0 }
.words { position:absolute; margin:0; display:flex; flex-direction:column; gap:18px } .words > * { margin:0 }
.line { font-size:88px; line-height:1.05; font-weight:700; letter-spacing:-0.01em } .sub { font-size:36px; line-height:1.3; font-weight:400 }
.t1 { font-size:64px; line-height:1.08; font-weight:700; letter-spacing:-0.01em } .t2 { font-size:34px; line-height:1.1; font-weight:700 } .t3 { font-size:28px; line-height:1.25; font-weight:600 }
.cap { font-size:24px; line-height:1.3; color:var(--ink2) } .cap2 { font-size:22px; line-height:1.3; color:var(--ink2) }
.mono { font-family:var(--mono, ui-monospace, monospace) }
.chip { display:inline-block; align-self:flex-start; padding:6px 14px; border-radius:999px; font-size:20px; font-weight:600; letter-spacing:.05em; text-transform:uppercase }
.onDark { color:var(--ground) } .onDark .cap, .onDark .cap2 { color:var(--dark-ink2) }
.edge { position:absolute; inset:0; background:radial-gradient(90% 80% at 50% 50%, transparent 60%, color-mix(in srgb, var(--main) 9%, transparent)) }
```

`fonts` in `scenes.json`: `{"sans":{"family":"Inter","or":"instrument-sans"},"mono":{"family":"DM Mono","or":"dm-mono"}}`
when the brand uses Helvetica or Arial; otherwise the brand's Google family in `sans`.

Cards must read against the ground. The kit keeps `--card` equal to the brand ground and
tints the field behind it with `.air` (ground mixed 6% toward main), so cards float on a
faintly colored field. If the brand ground is a mid grey or darker, that is not enough:
set `.air` darker (12 to 18% toward main) or make `--card` the lightest of the four
colors, until a card stands out at a glance. Check the contrast of `--ink2` on `--card`
(4.5 to 1 at least) whenever you change either; 66% of the ink is the safe default, 62%
sits on the limit with a light ink.

## shared.js

```js
// Paper cards on a faintly tinted ground, thin rails, one accent signal that travels them.
window.W = {
  // point at fraction q along a polyline [[x,y],...]
  along(pts, q) {
    const segs = []; let L = 0;
    for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); segs.push(d); L += d; }
    let d = Math.max(0, Math.min(1, q)) * L;
    for (let i = 0; i < segs.length; i++) {
      if (d <= segs[i] || i === segs.length - 1) { const p = segs[i] ? Math.min(1, d / segs[i]) : 0; return [pts[i][0] + (pts[i + 1][0] - pts[i][0]) * p, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * p]; }
      d -= segs[i];
    }
    return pts[pts.length - 1];
  },
  // fraction of a polyline at which a point lies (nearest point on the polyline); computed once at init for a loop station
  fracOf(pts, p) {
    let best = 0, bestD = Infinity, L = 0, acc = 0;
    for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    for (let i = 1; i < pts.length; i++) {
      const ax = pts[i - 1][0], ay = pts[i - 1][1], bx = pts[i][0], by = pts[i][1], dx = bx - ax, dy = by - ay, len = Math.hypot(dx, dy) || 1;
      const u = Math.max(0, Math.min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (len * len)));
      const d = Math.hypot(ax + dx * u - p[0], ay + dy * u - p[1]);
      if (d < bestD) { bestD = d; best = (acc + len * u) / L; }
      acc += len;
    }
    return best;
  },
  // camera on a .cam layer: (cx, cy) lands at stage center, z is the zoom
  cam(el, cx, cy, z) { el.style.transform = 'translate(' + (960 - cx * z).toFixed(2) + 'px,' + (540 - cy * z).toFixed(2) + 'px) scale(' + z.toFixed(4) + ')'; },
  // a group of words placed by its top-left edge; extra is more inline style, no quotes inside
  tag(cls, x, y, w, html, extra) { return '<div class="words ' + cls + '" style="left:' + x + 'px;top:' + y + 'px;width:' + w + 'px;' + (extra || '') + '">' + html + '</div>'; },
  // a paper card with a soft shadow and a left accent bar; .lit is the accent outline a scene turns up on arrival
  block(cls, x, y, w, h) {
    return '<g class="' + cls + '" transform="translate(' + x + ' ' + y + ')">' +
      '<rect x="6" y="8" width="' + w + '" height="' + h + '" rx="14" style="fill:var(--shade)"/>' +
      '<rect width="' + w + '" height="' + h + '" rx="14" style="fill:var(--card);stroke:var(--hair);stroke-width:2"/>' +
      '<rect width="10" height="' + h + '" rx="5" style="fill:var(--main)"/>' +
      '<rect width="' + w + '" height="' + h + '" rx="14" class="lit" style="fill:none;stroke:var(--accent);stroke-width:5;opacity:0"/></g>';
  },
  // a dashed note card for a side fact
  note(cls, x, y, w, h) { return '<rect class="' + cls + '" x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="14" style="fill:var(--tint);stroke:var(--main);stroke-width:2;stroke-dasharray:10 8"/>'; },
  // a window frame: light paper, or the dark variant for a screen or a terminal
  win(cls, x, y, w, h, dark) {
    return '<g class="' + cls + '" transform="translate(' + x + ' ' + y + ')">' +
      '<rect x="8" y="12" width="' + w + '" height="' + h + '" rx="16" style="fill:var(--shade)"/>' +
      '<rect width="' + w + '" height="' + h + '" rx="16" style="fill:' + (dark ? 'var(--dark)' : 'var(--card)') + ';stroke:' + (dark ? 'var(--dark2)' : 'var(--hair)') + ';stroke-width:2"/>' +
      '<path d="M0 46 H' + w + '" style="stroke:' + (dark ? 'var(--dark-hair)' : 'var(--hair)') + ';stroke-width:2"/>' +
      [26, 52, 78].map((cx) => '<circle cx="' + cx + '" cy="23" r="7" style="fill:' + (dark ? 'var(--dark2)' : 'var(--tint2)') + '"/>').join('') + '</g>';
  },
  // a plain rail between two points; connections are always this line, never an arrowhead
  rail(cls, pts) { return '<path class="' + cls + '" d="M' + pts.map((p) => p.join(' ')).join(' L') + '" style="fill:none;stroke:var(--tint2);stroke-width:6;stroke-linecap:round"/>'; },
  // the accent signal that travels the rails
  signal(cls) { return '<g class="' + cls + '"><circle r="30" style="fill:var(--glow)"/><circle r="12" style="fill:var(--accent)"/></g>'; },
  // a number badge for a step, as HTML so the number stays text
  badge(cls, x, y, n) { return W.tag(cls, x, y, 40, '<p class="mono" style="width:36px;height:36px;border-radius:50%;background:var(--main);color:var(--ground);font-size:19px;line-height:36px;text-align:center">' + n + '</p>'); },
  // a microphone on a stand, for any voice input
  mic(cls, x, y, s) {
    return '<g class="' + cls + '" transform="translate(' + x + ' ' + y + ') scale(' + s + ')">' +
      '<path d="M0 30 v36 M-34 66 h68" style="stroke:var(--second);stroke-width:9;stroke-linecap:round"/>' +
      '<path d="M-52 -22 a52 52 0 0 0 104 0" style="fill:none;stroke:var(--second);stroke-width:9;stroke-linecap:round"/>' +
      '<rect x="-30" y="-100" width="60" height="116" rx="30" style="fill:var(--main)"/>' +
      '<path d="M-15 -74 h30 M-15 -54 h30 M-15 -34 h30" style="stroke:var(--ground);stroke-width:4;stroke-linecap:round"/></g>';
  },
  // a waveform of n bars from t alone; live false gives a flat idle line
  wave(x, y, w, n, t, amp, seed, live) {
    let d = '';
    for (let i = 0; i < n; i++) {
      const px = x + i * (w / n);
      const a = amp * (live ? 0.3 + 0.7 * Math.abs(Math.sin(i * 1.7 + seed) * Math.sin(t * 5.3 + i * 0.9)) : 0.12);
      d += 'M' + px.toFixed(1) + ' ' + (y - a).toFixed(1) + ' V' + (y + a).toFixed(1) + ' ';
    }
    return d;
  },
};
```

## Conventions every scene follows

- Class names start with the scene id (`flow-b2`), so the page's layer list stays readable.
- A scene appends one root: `<div class="ground"><div class="air"></div><svg class="art" width="1920" height="1080" viewBox="0 0 1920 1080">…</svg>…words…</div>`.
- Words are HTML in `.words` groups; nothing textual goes in SVG.
- `render(t)` sets every varying style from `t`; entrances use `eo(seg(t, t0, t0 + 0.6))`
  for opacity and `lerp(22, 0, a)` for a small slide; an arrival light is
  `Math.max(0, 1 - Math.abs(t - (t0 + 0.7)) / 1.6)` on `.lit`.
- Markup in single quotes, `style="…"` in double quotes, no quotes inside a style.
- SVG groups are positioned and animated with the `transform` attribute only; CSS
  `style.transform` on a group overrides the attribute and drops the drawing at (0,0).
  HTML `.words` blocks take `style.transform`.

## Connection variants

One style per film. Replace `rail` and `signal` in the kit with one of these pairs when
the user asks; nothing else changes, because every scene calls the same two functions.

```js
// dashed rail (a tentative or optional link)
rail(cls, pts) { return '<path class="' + cls + '" d="M' + pts.map((p) => p.join(' ')).join(' L') + '" style="fill:none;stroke:var(--tint2);stroke-width:6;stroke-linecap:round;stroke-dasharray:14 14"/>'; },
// rail with an arrowhead at its end (define the marker once, in the first scene's svg: <defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" style="fill:var(--tint2)"/></marker></defs>)
rail(cls, pts) { return '<path class="' + cls + '" d="M' + pts.map((p) => p.join(' ')).join(' L') + '" marker-end="url(#arrow)" style="fill:none;stroke:var(--tint2);stroke-width:6;stroke-linecap:round"/>'; },
// comet: the dot with a fading tail; the scene sets the tail's direction with rotate(angle) in the same transform
signal(cls) { return '<g class="' + cls + '"><path d="M0 0 L-70 -7 L-70 7 Z" style="fill:var(--glow)"/><circle r="30" style="fill:var(--glow)"/><circle r="12" style="fill:var(--accent)"/></g>'; },
// pulse: no dot; the rail itself lights from start to end (set stroke-dashoffset from q in render: offset = length * (1 - q))
signal(cls) { return '<g class="' + cls + '"></g>'; },
// nothing travels: rails simply appear; keep signal() returning an empty group so scenes still find it
```

With arrowheads, every rail in the film carries one; with the pulse or nothing, the scene's
rail-lighting code (`x.el.style.opacity = eo(seg(t, t1 - 1.0, t1 - 0.6))`) is what marks
the beat. The user's choice goes in the reply in one line ("connections: dashed rails,
comet signal").
