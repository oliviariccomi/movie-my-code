---
name: movie-my-code
description: "Make a movie of the user's code: a narrated explainer film (a Motion artifact) that presents any software project, from its documents or straight from its code repository in any language or stack, to management, a client or a team, in two parts, the solution with its workflow and then how it was built (agents, rules, hooks, commands and the review loop, when the project was built with AI agents). Use this skill whenever the user asks for a video, film, animation, slides as a video, a motion piece or a visual walkthrough of a project, a codebase, an architecture, a pipeline, a workflow, a process or an agentic setup, especially when they will talk over it live, even if they never say Motion or explainer. Also use it to revise such a film from the user's comments anchored on the artifact."
---

# movie-my-code: a movie of any project, from its docs or its code

A film for a meeting is not a slide deck: things arrive in an order, one at a time, and the
presenter talks over them. Everything below follows from three facts about the audience:
they watch while listening to a person, they cannot pause, and they decide in minutes
whether the project is under control. So the film shows one idea at a time, in words a
manager can repeat, with enough air for the speaker, and it never shows anything that is
not true of the project.

The film is built with the Motion artifact type (a film written as code: scenes in
HTML/SVG/JS driven by a time `t`). This skill says what to put on screen, how to pace it,
how to size it and how to run the review loop. The Motion type's own pages say how to write
scenes; read them first, then this.

## 0. Inputs: what the request sets, and where it lands in the film

Everything a user can set is read from the request first, then from the Motion style form
(asked once, only for what the request left open), and it lands in one place in the code,
so a later change touches one line:

| Parameter | Said in the request as | Lands in | Default when unsaid |
|---|---|---|---|
| Colors | four hex values in role order: ground, main, second (the ink), accent; or "use our design system" | the first line of `base.css` (`--ground`, `--main`, `--second`, `--accent`), repeated as `palettes` and `background` in `scenes.json`; every other tone is mixed from them | the style form's palette |
| Typeface | the brand family | `fonts` in `scenes.json` (Google family; Helvetica and Arial map to Inter) | Inter + DM Mono |
| Total length | "under N minutes", "keep it short" | the `dur` of each scene in `scenes.json`, in seconds; the film is their sum, capped at 299 | 4 to 5 minutes narrated, 2 to 3 with a score |
| Pacing | "I will talk over it live" or "it plays on its own" | the arrival times at the top of each scene module (`S = [...]` for a flow, `T = {...}` for a screen, hop interval for a ladder) and the scene's `dur` | live voice: content scenes 20 to 30 s, no score |
| Music | "no music" / "with music" | the score module (`modules/score.js`), present or absent | none when narrated |
| Audience and language | "for management, in English" | the words on every card | ask |

To change a parameter after the film exists, edit the one place named above and keep ids
stable: a longer scene is its `dur` plus wider spacing in its `S` array; a new palette is
the four hex values only. The stage is always 1920 by 1080 at 30 fps.

## 1. Gather the material before any design

Read what the user has: project summary, decisions, working method, architecture notes,
measurements. When the material is a code repository (any language or stack), read it
in this order and stop when the picture is clear: the README and any docs folder; the
rules files for agents if present (AGENTS.md, CLAUDE.md, .cursorrules, a decisions log);
the entry points (main, the web host, the CLI, the scheduled jobs) and from there the one
path a request or a piece of data takes through the modules, which becomes the flow;
the interfaces or adapters at the edges (external services, storage, models), which
become the design rules; the configuration and the data files, which say what is
switchable; the tests and any evaluation scripts, which are the only source of numbers;
and the agent tooling (.claude or similar folders, hooks, commands, CI gates), which
becomes part two. Name components on screen by what they do, not by their class or file
name, and keep the real names for the small line under the title. Then write down, for
yourself, the facts the film may state:

- what the product does, for whom, and the one sentence that frames it (for anything
  clinical, legal or safety-related: the tool supports, the human decides; say it more
  than once in the film)
- the workflow as steps a non-engineer can follow (five steps per flow is the limit the eye
  takes in at once; split a long flow into two scenes of five)
- the three or four design rules that shape the architecture, in plain words
- numbers that were actually measured (how many cases tested, seconds, cost); none of
  these are invented, rounded up or extrapolated, and the film says "tested so far on N"
  rather than implying a finished evaluation
- if the project was built with AI agents: which agents, what each does well, where the
  knowledge lives (rules file, decision log, wiki), the enforcement ladder (rule, scoped
  rule, prompt, deny rules and hooks, server-side policy), the hooks and what each one
  refuses, the commands or skills that carry the method, the loop of one work item, and
  two to four lessons with their evidence

Ask the user only what changes the film and only they know: audience and language,
whether they narrate live (then no music and slower pacing), and the brand colors if there
is no design system. Decide the rest yourself and say what you decided.

Leave out, whatever the docs contain: ticket and pull-request numbers, branch names,
commit hashes, class and file names in titles (they may appear in the small line under a
title), people's names unless the user wants them, and any score such as "10 out of 10"
unless the user confirms it.

## 2. Shape: two parts, each a sequence of single ideas

Default structure, 12 to 16 scenes, total between 4 and 5 minutes when narrated (the
player loads nothing over 300 seconds, so cap at 299 and trim tails, never middles):

Part 1, the solution
1. Title beside one drawing of the solution (not a pipeline, not a diagram: the thing
   itself drawn simply, with a little motion)
2. The task in one picture: input, live middle state, output, plus the framing sentence
3. Flow A, five numbered steps appearing one by one
4. Flow B, five numbered steps appearing one by one (only if the flow needs ten steps)
5. Three or four design rules, one card each
6. The product's screen in use, with explanatory callouts
7. Measured so far: the numbers from section 1, if there are any, as a short scene of
   their own or as the note card inside a flow scene

Part 2, how it was built (only when the project was built with agents or a method worth
showing; otherwise end part 1 with results and the end card)
8. Part-two title
9. The agents: one card per agent with the role and what it does well
10. Where the knowledge lives: the repo as memory
11. The loop of one work item
12. Commands and skills that carry the method
13. The enforcement ladder
14. The hooks, one card each
15. What held: lessons with evidence
16. End card

This list is the maximum, not a form to fill: show only the rungs, agents, hooks and
commands the project really has, and drop a scene when nothing true fills it (a project
with three controls gets a three-step ladder; a project with no commands has no commands
scene). Every scene makes one point. If a scene needs two, split it. If a point needs a
table, it is a document, not a film.

## 3. Pacing for a live voice

The presenter reads the screen a beat before speaking, so nothing can rush:

- a content scene runs 20 to 30 seconds; a title card 6 to 8; a transition 6
- the first element lands at about 0.5 s (an entrance that starts at 0 is invisible)
- then one new element every 2 to 5 seconds, never two at once
- hold the finished picture 3 to 6 seconds before the cut; if the last line is the
  takeaway, it lands at least 5 seconds before the end
- a traveling token (a dot on a rail, a signal between cards) crosses the screen in
  under a second per hop; it marks the beat, it does not fill time
- the camera moves only between readings: a push or pan of 1.2 to 1.6 seconds, with no
  text appearing while it moves, and callouts appear only once it has stopped and
  disappear before it moves again

No music when the user narrates live. Otherwise a quiet wordless score, dropped the moment
the user says so.

## 4. The visual system

One world for the whole film, so it looks made by one hand: paper cards on a faintly
tinted ground, thin rails between them, one accent-colored signal that travels the rails,
and a dark variant of the card for anything that is a screen or a terminal. Four colors in
role order (ground, main, second as ink, accent), taken from the user's brand or design
system; greys are mixes of those four, never pure black or white. Typeface from the brand
if Google Fonts has it; Helvetica or Arial map to Inter (say so once).

Scene archetypes, with the geometry that is known to work on a 1920 by 1080 stage, are in
`references/scenes.md`; the shared kit (cards, windows, rails, signal, tags, camera,
waveform, microphone) is in `references/world.md`. Read both before writing the first
scene. The archetypes:

- Numbered snake flow: five cards of 540 by 220 in three columns and two rows, read left
  to right then right to left, each card with an icon at the left that animates when the
  step arrives, a 27 px title and a 24 px body centered vertically, a number badge at the
  top right, a plain rail between consecutive cards. Cards appear one at a time, each
  preceded by the signal traveling the rail to it, each lit by an accent outline for a
  second on arrival. Nothing is visible before its turn. The free sixth slot holds a
  dashed note card (a measured number, a side fact).
- Cards in a row: up to four cards of 400 wide, each with a role chip, a name and three
  or four short lines with a thin left border that turns accent as each line lands.
  Below, one wide bar for the sentence that binds them; then a footer line.
- Ladder: five steps rising left to right, 340 wide, 240 tall, text centered; a token
  hops up one step every 2.6 seconds; the lowest step is the softest control, the top one
  the strongest.
- Loop: a rounded track with eight stations and a token that follows the track's own
  curve (sample the corner curves into the path; a token that cuts corners looks broken);
  station labels outside the track, one card in the middle for the rule the loop obeys.
- Product screen: the real interface, lifted from code or screenshots when available,
  otherwise drawn plainly from the user's description at 1440 by 900 inside a dark window;
  the camera pushes to the part in use; the interaction (typing, a button lighting, a
  state chip changing) is driven from `t`; explanatory callouts with a leader line.
- Lessons: numbered rows, a 44 px claim and a 30 px evidence line, one every 5 seconds.
- Title and end: words on the left, the solution drawing on the right, never overlapping.

What not to do, because each of these was rejected by a real audience: a tall diagram the
camera scrolls through while everything is already visible; text cards without a drawing
or icon in the flow scenes; a mix of connection styles (arrowheads on some rails, plain
lines on others; use plain lines everywhere); a token that leaves its path; music under a
live voice; a film that fits any project typed into the same prompt.

## 5. Proportions: every box sized by its text

Boxes too large for their text read as empty; boxes too small spill. Size from the text,
not the other way round. Estimate before writing: a character is about 0.55 of the font
size wide (0.6 in bold and in monospace), a line is 1.3 times the font size tall; count
the lines each string will take at the box's inner width, add the gaps, add 28 to 32 px of
padding on every side, and give the box that height. Where the content varies between
sibling cards, keep the boxes equal and center the text block vertically (a flex column
with a fixed height and `justify-content: center`), so the air above and below stays equal.
Body text in cards is 24 px, titles 27 to 30 px, chips 20 px; a reader on a phone-sized
preview must still read them.

A label never overflows its bar, a chip never meets a badge, a line of words never wraps
where it cannot grow. Keep words out of SVG (the page's retype tool needs HTML text), and
give every group of lines one flow container so that a wrapped line pushes the next one
down instead of overlapping it.

## 6. Callouts on a product screen

A callout is a card with a 6 px accent left border and a light translucent background,
24 px text, placed in an empty area of the screen it explains, never over text, with a
3 px accent leader line ending in a 7 px dot next to the thing it explains. Route the
leader through paddings and gutters (the margin inside a panel, the gap between two
panels), never across a label or a button. Compute positions in stage space for each
camera state (stage x = 960 + (sceneX - cameraX) * zoom, likewise for y) and check the
rectangle of every text block under that camera before placing. Callouts fade in after the
camera stops, stay at least 4 seconds at full opacity (fade-in and fade-out not counted),
fade out before the next camera move. When a callout is boxed in between a camera stop
and the next move, the honest lever is to delay the move and everything after it, even if
the scene then runs a second or two over the timing table; never shrink the text or the
visible time to fit.

## 7. Building the film with the Motion type

Follow the Motion type's own instructions: list the types, describe the Motion type, read
its questions page, then rough-cut, finalize, motion and film-api (and recreate-ui when
the film shows a real product). These pages are long, about 25k tokens together, and they
are the authority on how a scene is written; budget for them. Ask the style form once,
unless the request already settles style, colors and length (then the type's own rule
says no form: decide, say your picks in a line and go on). Create the film; first batch
with `scenes.json` at stage rough, `base.css` and the script; then `shared.js`, one `set`
per scene in film order, then `scenes.json` at stage final, with a score only if the film
is not narrated. The type's default length is 10 to 30 seconds; a narrated project film
is the "asked for more" case, so write the real durations (section 3) into the first
batch's `scenes.json` from the start and keep the total under 300. Beyond those
mechanics:

- put the four colors, the tones mixed from them and the type scale in `base.css`; put
  every drawing that recurs (cards, windows, rails, signal, tags, camera helper) in
  `shared.js` so that scenes stay short
- each scene is a pure function of `t`: entrances are `eo(seg(t, t0, t0 + 0.6))`, lights
  are a symmetric pulse around the arrival, the signal's position is `along(points, q)`
- sibling cards share one geometry constant; change the constant, not the cards
- keep SVG light (a few hundred elements per scene) and filters off large areas
- never render stills or video yourself; the film's page exports the MP4

## 8. The review loop

The user watches the film and leaves comments anchored at a time. Scenes are hard cuts
with no crossfade and each scene's own `t` starts at 0, so the anchor maps to a scene by
summing the durations in `scenes.json` in order (a moved or retimed scene shifts every
later anchor; say so in the reply when it happens). Locate the element from the comment's
x and y percentages of the frame, change only what the comment asks, keep every id
stable, and reply in the comment's thread, in the language of the comment, with what
changed in the user's words. Typical asks and their fixes: "too fast" means longer scene
and wider spacing of entrances, not faster motion; "too much empty space" means bigger
text and vertical centering, not a smaller box; "overlaps" means move the box to an empty
area and re-route the leader; "remove X" means remove it everywhere it appears and say
where else it still appears. After any retiming, re-sum the durations and keep the total
under the cap by trimming the holds at the ends of the longest scenes.

## 9. Delivery

Hand back the film's link. Say in one line that Export on the film's page saves the MP4,
and what you made up that the user's real material would replace (screenshots of the real
product, their logo, their font files). The user narrates; the film is the visual.
