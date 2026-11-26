# movie-my-code

Make a movie of your code. A Claude skill that turns any software project into a narrated movie: part one shows the solution and its workflow, part two shows how it was built (agents, rules, hooks, commands, review loop) when the project was built with AI agents. The film is made with Claude's Motion artifact type (a film written as code), so it can be revised from comments anchored on the artifact and exported as MP4 from the film's page.

![movie-my-code: from a repo or its docs to a narrated film, one scene at a time](docs/demo.gif)

It works from project documents or straight from a code repository in any language or stack. The output is meant to be talked over live by the presenter: one idea per scene, management-level wording, boxes sized to their text, nothing on screen that is not true of the project.

## What you get

- a 1920 x 1080 film of 12 to 16 scenes, 4 to 5 minutes when narrated (hard cap 299 s)
- one visual world for the whole film: paper cards on a tinted ground, thin rails, one accent signal that travels them, a dark window for anything that is a screen
- scene archetypes that are known to work: numbered flow with animated icons, cards in a row, ladder, loop, product screen with callouts, lessons, title and end card
- a review loop: leave a comment on the film at a time, Claude maps it to the scene and element and changes only that

## Requirements

Claude with the Motion artifact type available (the Claude app on web or desktop). Claude Code can read the skill, but the film itself is built where artifacts are.

## Install

Pick one:

- **Claude app**: add `SKILL.md` (or the packaged `movie-my-code.skill`) as a skill in your account's skills settings.
- **Claude Code, personal**: copy this folder to `~/.claude/skills/movie-my-code/`.
- **Claude Code, one repo**: copy it to `<repo>/.claude/skills/movie-my-code/`.

## Use

Ask Claude for a movie of a project and give it the material (docs, a repo, or both). There is no configuration file: the parameters are the sentences of your request. Below is an example request for an invented project called "Inbox Triage"; every line stands for one parameter, and you replace each with your own.

```text
Make a video presenting our project "Inbox Triage" to the leadership team.          (1) project and audience
I will talk over it live, in English, no music, under five minutes.                 (2) pacing, language, music, length
Brand colors: #F2F4F7 (ground), #1B2A49 (main), #10141C (ink), #F2A900 (accent).    (3) colors
Material: README.md, docs/ARCHITECTURE.md, AGENTS.md, and the repo itself.          (4) material
Numbers measured so far: 120 real emails, 4 s each, about 0.004 USD each.           (5) numbers
Connections: plain lines with a traveling dot.                                      (6) connections, optional
```

What each line does, and where it ends up in the film:

| Line | Parameter | What it changes | Where it lands in the film's code | If you leave it out |
|---|---|---|---|---|
| (1) | project and audience | the framing sentence, the words on every card, the language | the text of each scene module; `lang` in `scenes.json` | Claude asks; when nobody can answer, it uses the language the request is written in and says so |
| (2) | pacing, language, music, length | "live" means 20 to 30 s per scene and no score; "plays on its own" means shorter scenes and a quiet score; the limit sets the total | `dur` of each scene in `scenes.json` (the film is their sum), the arrival times `S = [...]` at the top of each scene module, the score module present or absent | live, no music, 4 to 5 minutes |
| (3) | colors | the four brand colors, in role order: ground, main, ink, accent; every other tone is mixed from them | the first line of `base.css`; `palettes` and `background` in `scenes.json` | Claude asks once in the Motion style form |
| (4) | material | what the film is allowed to say; from a repo, Claude reads README and docs, agent rules files, entry points, interfaces, config, tests and the agent tooling, in that order | the content of every scene | Claude asks for it |
| (5) | numbers | the only figures the film may show, marked "measured so far" | the dashed note card in a flow scene, or a short scene of their own | no numbers in the film |
| (6) | connections | the one style of every link between cards: plain lines (default), dashed, arrowheads; and what travels them: an accent dot (default), a comet, a pulse along the rail, or nothing | `W.rail` and `W.signal` in `shared.js`, defined once for the whole film | plain lines and the traveling dot |

A blank version to fill in:

```text
Make a video presenting <project> to <audience>.
<I will talk over it live | It plays on its own>, in <language>, <no music | with music>, under <N> minutes.
Brand colors: <ground> (ground), <main> (main), <ink> (ink), <accent> (accent).   or: use our design system
Material: <files, folders, or the repository>.
Numbers measured so far: <only what was actually measured, or nothing>.
Connections: <plain lines | dashed | arrows>, <traveling dot | comet | pulse | nothing>.   optional
```

## Fixing the film

The first cut is rarely the last. Two ways to ask for a change:

- **Comment on the artifact.** Open the film, pause at the moment you mean, click the thing and write the comment in your own words ("this scene is too fast", "why does the dot stop here", "this box covers text", "remove the name"). The comment carries the time and the position in the frame; the skill maps the time to a scene by summing the `dur` values in `scenes.json`, finds the element from the position, changes only that, keeps every id stable, and replies in the comment's thread in the language you wrote it in. If a change moves or retimes a scene, every later comment anchor shifts, and the reply says so.
- **Ask in chat.** Same effect, useful for changes that span the whole film ("plain lines everywhere", "shorter by thirty seconds", "switch to our new palette").

What typical asks turn into: "too fast" is a longer scene and wider spacing of entrances, never faster motion; "too much empty space" is bigger text and vertical centering, never a smaller box; "overlaps" or "covers text" is the box moved to an empty area and the leader re-routed; "remove X" is X removed everywhere it appears, with a note of where else it still shows; "the dot stops" is the loop kept turning until the cut. After any retiming the skill re-sums the durations and keeps the total under 299 s by trimming holds at the ends of the longest scenes, never the middles.

Before handing a revision back, the skill renders the changed scene outside the player (`scripts/preview.py`) and checks two things a reading of the code misses: a drawing left at the stage origin and text blocks that overlap. If you prefer to edit yourself, the table above says where each parameter lives: `dur` and `desc` per scene in `scenes.json`, arrival times in the `S = [...]` array at the top of each scene module, the four colors in the first line of `base.css`, every rail and signal in `W.rail` and `W.signal` in `shared.js`.

## What it costs

Measured on the test runs, each by a fresh agent with only the skill, in a Claude session with the Motion type (your figures will differ with the model, the repo and the number of scenes):

| Run | Result | Tokens | Time |
|---|---|---|---|
| Complete film from a one-paragraph description (invented project) | 14 scenes, 4:28 | about 320k | about 25 min |
| Complete film from a real repository (12 Python modules, 230 KB of code and docs) | 10 scenes, 3:56 | about 355k | about 23 min, 42 tool calls |
| One revision from a comment anchored on the film | one scene retimed and one box moved | about 100k | about 6 min |

Of each full run about 35k tokens are the Motion type's own pages, read once per film, and 10 to 20k go to each scene written; a product-screen scene costs about twice a flow scene, because the real interface is rebuilt from its code. A revision costs 30 to 60k when only `scenes.json` and the one scene are re-read, which is what the skill now says to do; listing the whole `modules` collection returns every scene at once (about 25k) and is for a missing scene only. The cheapest film is the one asked for in a single request with all the parameters above: every open question is a round trip.

## Layout

```
movie-my-code/
├── SKILL.md              the method: inputs, material, shape, pacing, visual system, proportions, callouts, Motion mechanics, review loop
├── references/
│   ├── world.md          base.css and shared.js: the kit every scene uses
│   └── scenes.md         the scene archetypes as code, with their timing tables
├── scripts/preview.py    screenshots one scene outside the player with a stub kit, and warns when a drawing sits at the origin
├── evals/                two test cases with graders (a film from a description; a revision from an anchored comment)
└── docs/demo.gif         the animation above
```

## Testing

The two cases under `evals/` were run with fresh agents that had only the skill: one built a complete film for an invented project from a short description, the other applied a revision from a comment anchored at a time on the artifact. Both passed all graders. A third run took a real Python repository (a personal job-search agent with no agent tooling and no measured numbers) and a request in Italian for a non-technical audience: the agent read the repo in the skill's order, dropped part two and the numbers scene on its own, rebuilt the product's control panel from its page code, and labelled the example data on screen. Its 24 remarks on unclear or contradictory passages are folded into this version. With Claude Code, `claude plugin eval` runs the two cases.

## License

MIT, see `LICENSE`.
