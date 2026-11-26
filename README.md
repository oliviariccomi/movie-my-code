# movie-my-code

Make a movie of your code. A Claude skill that turns any software project into a narrated movie: part one shows the solution and its workflow, part two shows how it was built (agents, rules, hooks, commands, review loop) when the project was built with AI agents. The film is made with Claude's Motion artifact type (a film written as code), so it can be revised from comments anchored on the artifact and exported as MP4 from the film's page.

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

Ask for a video of a project and give Claude the material (docs, a repo, or both). The request is where the parameters go; everything you leave out is asked once in the Motion style form or decided with a stated default.

```
Make a video presenting our project "Inbox Triage" to the leadership team.
I will talk over it live, in English, no music, under five minutes.
Brand colors: light grey #F2F4F7 (ground), navy #1B2A49 (main), near-black #10141C (ink), amber #F2A900 (accent).
Material: README.md, docs/ARCHITECTURE.md, AGENTS.md, and the repo itself.
Numbers measured so far: 120 real emails, 4 s each, about 0.004 USD each.
```

| Parameter | How to set it | Where it lands in the film |
|---|---|---|
| Colors | four hex values in role order: ground, main, ink, accent | first line of `base.css`; `palettes` and `background` in `scenes.json` |
| Typeface | the brand family | `fonts` in `scenes.json` |
| Total length | "under N minutes" | `dur` of each scene in `scenes.json`; the film is their sum |
| Pacing | "I will talk over it live" or "it plays on its own" | arrival times at the top of each scene module (`S = [...]`) and each scene's `dur` |
| Music | "no music" / "with music" | the score module, present or absent |
| Audience, language | "for management, in English" | the words on every card |

To change something later, comment on the film at the moment you mean ("this scene is too fast", "this box covers text") or ask in chat; the skill changes the one place that parameter lives and keeps everything else stable.

## Layout

```
movie-my-code/
├── SKILL.md              the method: material, shape, pacing, visual system, proportions, callouts, Motion mechanics, review loop
├── references/
│   ├── world.md          base.css and shared.js: the kit every scene uses
│   └── scenes.md         the scene archetypes as code, with their timing tables
└── evals/                two test cases with graders (a film from a description; a revision from an anchored comment)
```

## Testing

The two cases under `evals/` were run with fresh agents that had only the skill: one built a complete film for an unrelated project from a short description, the other applied a revision from a comment anchored at a time on the artifact. Both passed all graders. With Claude Code, `claude plugin eval` runs the same cases.

## License

MIT, see `LICENSE`.
