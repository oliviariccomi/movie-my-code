# movie-my-code

This is a Claude skill that turns a software project into a short narrated film. The first half shows what the thing does and how the work flows through it; the second half shows how it was built (which agents, which rules and hooks, how changes get reviewed). The film is a Motion artifact, so it can be commented on like a document and Claude fixes the exact scene you point at. The Export button on the film gives you an MP4.

![movie-my-code: from a repo or its docs to a narrated film, one scene at a time](docs/demo.gif)

It works from documents, from a repo, or both, in any language or stack. The result is meant to be talked over live.

## What comes out

A 1920 x 1080 film, usually 12 to 16 scenes and 4 to 5 minutes (the type caps it at 299 seconds). All the scenes share one look: paper cards on a tinted background, thin rails between them, one accent-coloured dot that travels the rails, and a dark window whenever something is a screen. But this can be personalized. The scenes are built from a handful of layouts that are known to work at this size: a numbered flow with small animated icons, cards in a row, a ladder, a loop, the real product screen with callouts, a list of lessons, a title card and an end card.

## What you need

Claude with the Motion artifact type, which means the Claude app on web or desktop. Claude Code can read the skill, but the film itself gets built where artifacts live.

## Install

- Claude app: add `SKILL.md` (or `movie-my-code.skill`, same thing zipped) as a skill in your account's skills settings.
- Claude Code, for yourself: copy this folder to `~/.claude/skills/movie-my-code/`.
- Claude Code, for one repo: copy it to `<repo>/.claude/skills/movie-my-code/`.

## How to ask for a film

In this Project there's no config file. The settings are the sentences in your prompt. Here's the request used for testing, with example project called Inbox Triage. Each line sets one thing that you can swap in your own.

```text
Make a video presenting our project "Inbox Triage" to the leadership team.          (1) project and audience
I will talk over it live, in English, no music, under five minutes.                 (2) pacing, language, music, length
Brand colors: #F2F4F7 (ground), #1B2A49 (main), #10141C (ink), #F2A900 (accent).    (3) colors
Material: README.md, docs/ARCHITECTURE.md, AGENTS.md, and the repo itself.          (4) material
Numbers measured so far: 120 real emails, 4 s each, about 0.004 USD each.           (5) numbers
Connections: plain lines with a traveling dot.                                      (6) connections, optional
```

What each line does, and where it ends up if you ever want to edit the film by hand:

| Line | Sets | What it changes | Where it lives in the film's code | If you leave it out |
|---|---|---|---|---|
| (1) | project and audience | the framing, the words on every card, the language | the text of each scene module; `lang` in `scenes.json` | Claude asks. If nobody's there to answer, it uses the language you wrote in and tells you |
| (2) | pacing, language, music, length | "live" means 20 to 30 s per scene and no music; "plays on its own" means shorter scenes and a quiet score; the limit caps the total | `dur` per scene in `scenes.json` (the film is their sum), the arrival times `S = [...]` at the top of each scene, the score module present or not | live, no music, 4 to 5 minutes |
| (3) | colors | the four brand colours in this order: background, main, ink, accent. Everything else is mixed from those | the first line of `base.css`; `palettes` and `background` in `scenes.json` | Claude asks once, in the Motion style form |
| (4) | material | what the film is allowed to say. From a repo, Claude reads README and docs first, then agent rules files, entry points, interfaces, config, tests, and the agent tooling | the content of every scene | Claude asks for it |
| (5) | numbers | the only figures that may appear, always marked "measured so far" | the dashed note card in a flow scene, or a short scene of their own | no numbers at all |
| (6) | connections | one style for every link: plain lines, dashed, or arrowheads; and what travels them: a dot, a comet, a pulse along the rail, or nothing | `W.rail` and `W.signal` in `shared.js`, defined once | plain lines and the dot |

A blank example for you to fill in:

```text
Make a video presenting <project> to <audience>.
<I will talk over it live | It plays on its own>, in <language>, <no music | with music>, under <N> minutes.
Brand colors: <ground> (ground), <main> (main), <ink> (ink), <accent> (accent).   or: use our design system
Material: <files, folders, or the repository>.
Numbers measured so far: <only what was actually measured, or nothing>.
Connections: <plain lines | dashed | arrows>, <traveling dot | comet | pulse | nothing>.   optional
```

## When something's wrong

And for sure something will be :) Two ways to get it fixed.

The quickest: open the film, pause where the problem is, click on it and write a comment the way you'd write it to a colleague. "This scene is too fast." "Why does the dot stop here?" "This box covers text." "Remove the name." The comment carries the time and the spot in the frame. Claude works out which scene that is (by adding up the `dur` values), finds the element, changes that and nothing else, and answers in the thread in whatever language you wrote. If the fix moves or retimes a scene, the anchors of any later comments shift too; the reply will say so.

Or just ask in chat. Better for changes that touch the whole film: "plain lines everywhere", "thirty seconds shorter", "switch to the new palette".

The skill has its own ideas about what a fix should be, learned the hard way. "Too fast" means a longer scene with more room between entrances, not faster motion. "Too much empty space" means bigger text, not a smaller box. "Overlapping" means the box moves to an empty area and its leader line gets re-routed. "Remove X" means X goes everywhere, and you get told where else it still shows up. "The dot stops" means the loop should keep turning until the cut. After any retiming the durations get re-added and the total trimmed back under 299 s by cutting the holds at the ends of the longest scenes, never the middles.

Before handing a fix back, the skill renders the changed scene outside the player (`scripts/preview.py`) and checks two things you can't see by reading code: a drawing that ended up at the top-left corner of the stage, and text sitting on top of other text. Both happened in testing. If you'd rather edit the film yourself, the table above says where each thing lives.

## What it costs

Each was a fresh agent with nothing but the skill in a Claude session with the Motion type. Yours will differ with the model, the repo and how many scenes you end up with.

| Run | Result | Tokens | Time |
|---|---|---|---|
| Full film from a one-paragraph description (made-up project) | 14 scenes, 4:28 | about 320k | about 25 min |
| Full film from a real repo (12 Python modules, 230 KB of code and docs) | 10 scenes, 3:56 | about 355k | about 23 min, 42 tool calls |
| One fix from a comment on the film | one scene retimed, one box moved | about 100k | about 6 min |

Where it goes: roughly 35k per film on the Motion type's own instruction pages, read once; 10 to 20k per scene written; a product-screen scene costs about double a flow scene because the real interface gets rebuilt from its code. A fix should cost 30 to 60k if only `scenes.json` and the one scene get re-read, which is what the skill now says to do. Listing the whole `modules` collection dumps every scene at once (about 25k) and is only worth it when a scene is missing. The cheapest film is the one asked for in a single message with all six lines filled in.

## What's in here

```
movie-my-code/
├── SKILL.md              the method: inputs, material, shape, pacing, visual system, proportions, callouts, Motion mechanics, review loop
├── references/
│   ├── world.md          base.css and shared.js, the kit every scene uses
│   └── scenes.md         the scene layouts as code, with their timings
├── scripts/preview.py    screenshots one scene outside the player with a stub kit, and warns about drawings at the origin or overlapping text
├── evals/                two test cases with graders (a film from a description; a fix from a comment)
└── docs/demo.gif         the animation at the top
```

## How it was tested

The two cases under `evals/` were run by fresh agents that only had the skill. One built a whole film for a made-up project from a short description, the other applied a fix from a comment anchored at a time on the film. Both passed their graders. A third run pointed the skill at a real repo, a small Python job-search agent with no agent tooling and no measured numbers, and asked for a film in Italian for people who aren't engineers. The agent read the repo in the order the skill gives, dropped the second half and the numbers scene on its own, rebuilt the project's control panel from its page code, and labelled the example data on screen. It also came back with 24 notes on things in the skill that were unclear or contradicted the Motion type's own pages. Those are all folded into this version with Claude Code, `claude plugin eval` runs the two cases.

## License

MIT, see `LICENSE`.
