# Scene archetypes

Working geometry and code for each archetype on a 1920 by 1080 stage, built on the kit in
`world.md`. Copy the structure, replace the words and the icons with the project's own,
keep the numbers unless the text makes you recompute them (section 5 of SKILL.md).

Contents
1. Numbered snake flow with icons
2. Cards in a row (agents, hooks)
3. Ladder
4. Loop with a token on a curved track
5. Product screen with callouts and leaders
6. Lessons
7. Title and end card with a solution drawing
8. Timing tables

## 1. Numbered snake flow with icons

Five cards of 540 by 220 in three columns (x 100, 690, 1280) and two rows (y 260, 560),
read left to right on the first row and right to left on the second; the sixth slot (row 2,
column 1) holds a dashed note. Icon box 100 by 100 at (x + 30, y + 54); text at x + 156,
350 wide, centered in a 170 px tall flex column; badge at (x + 474, y + 20). Rails: short
plain lines between consecutive cards, the vertical one from column 3 down.

```js
const { seg, eo, eio, eob, lerp, TextFx } = kit;
const CX = [100, 690, 1280], RY = [260, 560], BW = 540, BH = 220;
const STEPS = [ /* { label: 'Short title', sub: 'One sentence a manager can repeat, under 75 characters (three lines of 24 px Inter in 350 px)' } × 5 */ ];
const POS = [[0, 0], [0, 1], [0, 2], [1, 2], [1, 1]];
const S = [0.8, 4.6, 8.4, 12.2, 16.0];                       // arrival of each step
const RAILS = [[[640, 370], [690, 370]], [[1230, 370], [1280, 370]], [[1550, 480], [1550, 560]], [[1280, 670], [1230, 670]]];
// One icon object per step: svg(c) returns markup in a 100×100 box, bind(q, c) finds its moving parts,
// render(s) animates from s = seconds since the step arrived. Example: a document whose check mark draws itself.
const ICONS = [ {
  svg: (c) => '<g class="' + c + '"><path d="M22 8 h34 l16 16 v68 h-50 z" style="fill:var(--card);stroke:var(--main);stroke-width:4;stroke-linejoin:round"/><path d="M32 42 h30 M32 54 h30 M32 66 h18" style="stroke:var(--tint2);stroke-width:4;stroke-linecap:round"/><g class="' + c + '-ck" transform="translate(74 76)"><circle r="18" style="fill:var(--accent)"/><path class="' + c + '-ct" d="M-9 0 l7 7 l12 -14" style="fill:none;stroke:var(--ground);stroke-width:5;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:40;stroke-dashoffset:40"/></g></g>',
  bind(q, c) { this.ck = q('.' + c + '-ck'); this.ct = q('.' + c + '-ct'); },
  render(s) { this.ck.setAttribute('transform', 'translate(74 76) scale(' + Math.max(0, eob(seg(s, 0.3, 0.8), 1.6)).toFixed(3) + ')'); this.ct.style.strokeDashoffset = (40 * (1 - eo(seg(s, 0.8, 1.4)))).toFixed(1); } },
  /* … four more */ ];
kit.scene('flow', {
  init(kit) {
    let svg = RAILS.map((r, i) => W.rail('flow-r' + i, r)).join(''), words = '';
    STEPS.forEach((b, i) => {
      const x = CX[POS[i][1]], y = RY[POS[i][0]];
      svg += W.block('flow-b' + i, x, y, BW, BH) + '<g class="flow-ig' + i + '" transform="translate(' + (x + 30) + ' ' + (y + 54) + ')">' + ICONS[i].svg('flow-i' + i) + '</g>';
      words += W.tag('flow-w' + i, x + 156, y + 25, 350, '<p class="t2" style="font-size:27px">' + b.label + '</p><p class="cap">' + b.sub + '</p>', 'gap:10px;height:170px;justify-content:center') + W.badge('flow-n' + i, x + BW - 62, y + 20, i + 1);
    });
    svg += W.note('flow-note', 100, 560, 540, 220) + W.signal('flow-sig');
    words += W.tag('flow-nw', 136, 585, 468, '<p class="t3">A measured fact</p><p class="cap">Its one-sentence meaning.</p>', 'gap:10px;height:170px;justify-content:center');
    kit.stage.append(kit.h('<div class="ground"><div class="air"></div><svg class="art" width="1920" height="1080" viewBox="0 0 1920 1080">' + svg + '</svg>' + words +
      '<div class="words flow-h" style="left:100px;top:66px;width:1300px;gap:12px"><p class="chip" style="background:var(--main);color:var(--ground)">Part 1</p><h2 class="t1">From input to outcome</h2><p class="cap">What happens between A and B.</p></div>' +
      '<div class="words flow-f" style="left:100px;top:850px;width:1720px"><p class="sub">The one sentence to take away.</p></div></div>'));
    const q = (s) => kit.stage.querySelector(s);
    this.sig = q('.flow-sig'); this.h = q('.flow-h h2'); this.hc = q('.flow-h .cap'); this.f = q('.flow-f p'); this.note = q('.flow-note'); this.nw = q('.flow-nw');
    this.blocks = STEPS.map((b, i) => { ICONS[i].bind(q, 'flow-i' + i); return { i, g: q('.flow-b' + i), ig: q('.flow-ig' + i), w: q('.flow-w' + i), n: q('.flow-n' + i), lit: q('.flow-b' + i + ' .lit'), x: CX[POS[i][1]], y: RY[POS[i][0]] }; });
    this.rails = RAILS.map((r, i) => ({ r, el: q('.flow-r' + i) }));
  },
  render(t) {
    TextFx.fadeFromRight(this.h, t, -0.3); this.hc.style.opacity = eo(seg(t, 0.8, 1.4));
    for (const b of this.blocks) {
      const a = eo(seg(t, S[b.i], S[b.i] + 0.6)), dy = lerp(22, 0, a);
      b.g.style.opacity = a; b.w.style.opacity = a; b.n.style.opacity = a; b.ig.style.opacity = a;
      b.g.style.transform = 'translate(' + b.x + 'px, ' + (b.y + dy).toFixed(1) + 'px)';
      b.ig.setAttribute('transform', 'translate(' + (b.x + 30) + ' ' + (b.y + 54 + dy).toFixed(1) + ')');
      b.w.style.transform = 'translateY(' + dy.toFixed(1) + 'px)'; b.n.style.transform = b.w.style.transform;
      b.lit.style.opacity = (Math.max(0, 1 - Math.abs(t - (S[b.i] + 0.7)) / 1.6) * 0.95).toFixed(3);
      ICONS[b.i].render(t - S[b.i]);
    }
    let shown = false;
    this.rails.forEach((x, i) => {
      const t1 = S[i + 1]; x.el.style.opacity = eo(seg(t, t1 - 1.0, t1 - 0.6));
      const q = seg(t, t1 - 0.8, t1);
      if (q > 0 && q < 1) { const p = W.along(x.r, eio(q)); this.sig.setAttribute('transform', 'translate(' + p[0].toFixed(1) + ' ' + p[1].toFixed(1) + ')'); shown = true; }
    });
    this.sig.style.opacity = shown ? 1 : 0;
    const no = eo(seg(t, S[4] + 2.0, S[4] + 2.6)); this.note.style.opacity = no; this.nw.style.opacity = no;
    TextFx.fadeFromRight(this.f, t, 20.5);
  },
});
```

Icon ideas that have read well at 100 px: a microphone with a boiling waveform; a server
stack with a padlock whose shackle closes; a waveform becoming three text bars that grow;
a bar with an accent chip that shrinks to a dot while structured bars appear; a document
with a check that draws itself; a document sliding into a dashed template; a chip with a
pulsing core; a magnifier descending onto an accent line in a list; a stamp band landing
on a document with overshoot; a ledger whose rows fill while a clock hand turns.

## 2. Cards in a row (agents, hooks)

Four cards 400 wide at x 100, 540, 980, 1420, y 230; height from the longest card (agents
470, hooks 380). Inside: a chip (role or trigger), a name at 29 px (monospace for a hook or
a command), three or four `cap2` lines with `padding-left:18px;border-left:3px solid
var(--tint2)` whose border turns accent as each lands. A wide bar below (100, 740, 1720,
130) for the sentence that binds them, a `sub` footer at 920. Entrances: card i at
1 + 6i seconds, its lines every 0.9 s; bar at 24.5; footer at 27 in a 29-second scene.

```js
// init, per card c (x from the column, t = 1 + 6i): the block, then one words group
svg += W.block('ag-b' + i, c.x, 230, 400, 470);
words += W.tag('ag-w' + i, c.x + 32, 262, 336, '<p class="chip" style="background:var(--tint2);color:var(--second)">' + c.role + '</p><p class="t2" style="font-size:29px">' + c.name + '</p>' +
  c.lines.map((l) => '<p class="cap2 ag-l" style="padding-left:18px;border-left:3px solid var(--tint2)">' + l + '</p>').join(''), 'gap:14px');
// bind: c.does = [...q('.ag-w' + i).querySelectorAll('.ag-l')]
// render: the card enters like a flow card (opacity and a 22 px slide); then its lines:
c.does.forEach((el, i) => { const b = eo(seg(t, c.t + 1.0 + i * 0.9, c.t + 1.5 + i * 0.9)); el.style.opacity = b; el.style.transform = 'translateX(' + lerp(-12, 0, b).toFixed(1) + 'px)'; el.style.borderLeftColor = b > 0.99 ? 'var(--accent)' : 'var(--tint2)'; });
```

## 3. Ladder

Five cards 340 by 240 at x 60, 420, 780, 1140, 1500 and y 720, 600, 480, 360, 240; title
30 px, body 26 px, both centered in a 196 px column. A signal token sits on the first step
and hops up one step every 2.6 s with an 0.8 s arc (`py -= 90 * sin(pi * q)` on the hop,
not on the last hold); each step lights on landing. Heading with the key sentence at the
top left (the top steps are to its right, so widths must not meet), footer at 985.

Any number of steps from three to five: lay them out from `N = STEPS.length` (x spaced
360 apart from 60, y descending 120 per step from 720) and let the hop loop use `N - 1`
as its last index.

```js
const N = STEPS.length, LAST = N - 1, hop = (i) => 2.0 + i * 2.6, D = 0.8;
let i = 0; while (i < LAST && t >= hop(i + 1)) i++;
const q = seg(t, hop(i), hop(i) + D), a = STEPS[i], b = STEPS[Math.min(LAST, i + 1)], e = eio(q);
const px = lerp(a.x + 170, b.x + 170, e), py = lerp(a.y - 40, b.y - 40, e) - (i < LAST ? 90 : 0) * Math.sin(Math.PI * q);
```

## 4. Loop with a token on a curved track

Track: `M400 240 H1520 Q1660 240 1660 380 V680 Q1660 820 1520 820 H400 Q260 820 260 680
V380 Q260 240 400 240 Z` (240 to 820 tall: labels under the bottom row wrap to two lines
and still clear a footer at y 1000 by 50 px). The token's path samples the four corners, so it never cuts them:

```js
const qb = (p0, c, p1, n) => { const out = []; for (let i = 1; i <= n; i++) { const u = i / n, a = (1 - u) * (1 - u), b = 2 * (1 - u) * u, d = u * u; out.push([a * p0[0] + b * c[0] + d * p1[0], a * p0[1] + b * c[1] + d * p1[1]]); } return out; };
const LOOP = [[400, 240], [1520, 240], ...qb([1520, 240], [1660, 240], [1660, 380], 10), [1660, 680], ...qb([1660, 680], [1660, 820], [1520, 820], 10), [400, 820], ...qb([400, 820], [260, 820], [260, 680], 10), [260, 380], ...qb([260, 380], [260, 240], [400, 240], 10)];
```

Eight stations on the straight stretches, each a 22 px circle with a 10 px dot that turns
accent once passed; labels outside the track (above the top row at y 130, below the bottom
row at y 850, beside the sides at x 10 and 1700, 210 wide), 28 px title and 22 px line; one
card in the middle (560, 425, 800, 210) with the rule the loop obeys. The token completes
the first lap in about 13 seconds and then keeps circling at the same pace until the cut
(`lap = (t - Q0) / (Q1 - Q0); q = t < Q0 ? 0 : lap - Math.floor(lap)`): a token that
stops dead in a corner reads as a glitch, and a loop that keeps turning is the point. Compute each
station's fraction once at init with `W.fracOf(LOOP, point)` from `world.md` and keep it
in the scene's state (a station is lit when `q >= frac`); never read a position back from
the DOM in render.

## 5. Product screen with callouts and leaders

Build the window at 1440 by 900 at stage (240, 90) inside a `.cam` layer, dark theme or
the product's own, with panels as `position:absolute` divs and all words in `.words`
groups. Drive the interaction from a table of moments:

```js
const T = { live: 3.0, end: 12.0, editor: 13.0, confirm: 15.5, gen: 17.5, draft: 21.0 };
// camera: whole window until 4.5 (the establishing view a presenter needs), push to the working panel 4.5–6.0,
// hold, pan to the result panel 17.2–18.8, hold. Z comes from the product's smallest UI text: 24 / px, so a
// 15 px body wants 1.6 and 12.5 px notes 1.9; the example below is for a 16 px product.
const a = eio(seg(t, 4.5, 6.0)), b = eio(seg(t, 17.2, 18.8));
let cx = lerp(960, 930, a), cy = lerp(540, 520, a), z = lerp(1, 1.5, a);
cx = lerp(cx, 1300, b); cy = lerp(cy, 500, b); z = lerp(z, 1.5, b) + 0.012 * seg(t, 18.8, 29);
W.cam(this.cam, cx, cy, z);
```

A real page is usually taller than the 900 px window (three sections of a control panel
run to about 2200 px). Measure each section's real height before fixing the next one's
top (count its rows, inputs, hints and buttons with the proportion rule, or render it once
with `scripts/preview.py`): a section top typed from a guess puts one section's buttons
over the next section's heading, and the camera then frames the overlap for ten seconds. The runner refuses scrolled elements, so the page does not scroll:
its main column moves by a transform, with the section tops fixed at init so the offsets
are known, and the camera pans in window space while the column slides under it:

```js
const TOP = { setup: 0, run: 760, results: 1520 };           // section tops in page px, fixed at init
const sy = lerp(TOP.setup, TOP.run, eio(seg(t, 12.6, 14.0)));  // the pan: one section top to the next
this.col.style.transform = 'translateY(' + (-sy).toFixed(1) + 'px)';   // the column slides; the camera stays on the window
```

Typing with a provisional tail (two `<p>` elements in one `.words` group: the confirmed
part in the ink color, the tail in the muted color), a button press and a state chip:

```js
// init: this.fin = q('.scr-fin'); this.part = q('.scr-part');  (both <p> inside one .words)
const live = t >= T.live && t < T.end;
const txt = streamed(TEXT, t, T.live, 17), ws = txt ? txt.split(' ') : [];   // 17 characters a second reads as real dictation
const cut = live ? Math.max(0, ws.length - 3) : ws.length;                   // the last three words stay provisional while live
this.fin.textContent = ws.slice(0, cut).join(' ');
this.part.textContent = ws.slice(cut).join(' ');
const flash = (el, tp) => { const f = t < tp ? 0 : 1 - seg(t, tp, tp + 0.7); el.style.background = f > 0 ? 'color-mix(in srgb, var(--accent) ' + Math.round(f * 100) + '%, var(--dark))' : 'var(--dark)'; };
flash(this.okButton, T.confirm);                                             // a press is a flash that decays; before tp it must be 0, or the button sits lit from the start
const confirmed = t >= T.confirm + 0.4;
this.chip.textContent = confirmed ? 'Confirmed' : 'Transcribed';            // a state chip flips text and color at the moment
this.chip.style.background = confirmed ? 'var(--accent)' : 'var(--lav)';
```

Callouts live at stage level, outside the camera layer, each with its window of time, a
position in an empty area under that camera state, and a leader that runs through gutters:

```js
const CALL = [
  { t0: 0.5, t1: 4.3, x: 272, y: 800, w: 320, fs: 22, text: '…', lead: 'M275 798 V588 H296', dot: [300, 588] },
  { t0: 6.4, t1: 12.6, x: 560, y: 680, w: 520, fs: 24, text: '…', lead: 'M820 678 V446', dot: [820, 446] },
  { t0: 19.2, t1: 22.2, x: 330, y: 720, w: 520, fs: 24, text: '…', lead: 'M850 760 H900 V260 H926', dot: [930, 260] },
];
// markup: a .words div per callout with padding 18px 24px, border-left 6px accent, a 96% ground background, a soft shadow;
// one SVG layer after them with a 3 px accent path and a 7 px dot per callout
// render: a = eo(seg(t, c.t0, c.t0 + 0.5)) * (1 - seg(t, c.t1 - 0.3, c.t1)); callout and leader share a
```

Position check for every callout: for the camera state in which it shows, map every text
block of the window to stage space (`x = 960 + (240 + wx - cx) * z`, `y = 540 + (90 + wy -
cy) * z`) and keep the callout's rectangle and the leader's segments clear of all of them.

## 6. Lessons

Rows at y 230, 420, 610, 800: an accent badge at x 140, a 44 px claim, a 30 px evidence
line, a hairline at y + 156; one row every 5 seconds, claim first, evidence 1.4 s later.

## 7. Title and end card with a solution drawing

Words on the left (left 120, width 840): `line` title, `sub`, `cap` byline. The drawing on
the right from x 990: the solution itself, simply drawn, with one or two motions driven by
`t` (a waveform that boils, bars that grow, a signal that crosses two rails, an accent
outline that lights). Two cards in the drawing share one size (280 by 360). The end card
reuses the drawing at lower opacity with a different byline.

## 8. Timing tables

| Scene archetype | Duration | Entrances |
|---|---|---|
| Title, end | 8 | title at 0 (started early), sub at 0.5, byline at 1.4 |
| One-picture task | 20 | heading at 0, stations every 2–4 s, footer at 16–17 |
| Snake flow | 24 | steps at 0.8, 4.6, 8.4, 12.2, 16.0; note at 18; footer at 20.5 |
| Design rules | 14 | cards at 0.8, 4.6, 8.4; footer at 11.6 |
| Product screen | 28–30 | see section 5 |
| Part-two title | 6 | chip at 1.0, title at 1.3, sub at 2.3 |
| Cards in a row | 27–30 | cards at 1, 7, 13, 19; bar at 24.5; footer at 27 |
| Repo as memory | 27–30 | tree lines every 0.12 s; notes every 4.5 s; footer 1.5 s before the end |
| Loop | 20 | token 2–15, hold to the end |
| Commands and skills | 23 | rows every 1.6 s; skill cards at 10.5 and 14; footer at 18.5 |
| Ladder | 20 | steps every 0.3 s; hops from 2.0 every 2.6 s; key line at 14.5; footer at 16.5 |
| Hooks | 27 | cards at 1, 5.5, 10, 14.5; bar at 19; footer at 21.5 |
| Lessons | 21–22 | rows at 1, 6, 11, 16 |
