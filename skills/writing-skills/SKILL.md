---
name: writing-skills
description: Use when adding a new hackinator skill, editing an existing one, or reviewing whether a skill is well-formed — before writing the SKILL.md, and before considering it done
---

# Writing Skills

## Overview

**Core principle:** A skill earns its place by changing what a future agent *does*, not by
describing what you already know. If an agent would behave correctly without the skill, the skill
is noise. So the test comes first: watch the wrong behavior happen, then write the smallest skill
that fixes it.

A skill is a **reusable technique, persona, or reference** — not a story about the one time you
solved something. If it reads like a diary entry, it's not a skill yet.

## Write the Failing Case First

```
NO SKILL WITHOUT FIRST SEEING THE BEHAVIOR IT FIXES
```

1. **Run the scenario without the skill.** Give a fresh agent the task that should trigger it.
   Watch what it actually does. Write down the exact wrong move and the exact rationalization it used.
2. **Write the minimal skill** that addresses *that* failure — not every hypothetical cousin of it.
3. **Run the scenario again with the skill.** Confirm the behavior changed. If it didn't, the
   wording is too soft or too abstract — tighten it against the real rationalization, not an imagined one.
4. **Record the scenario** in the skill's `evals/` — the triggering prompt plus the expected-behavior
   bullets. That baseline is what proves the *next* edit still works. A skill with no recorded failing
   case is a claim no one can re-check; evals are the source of truth, not the prose.

Skipping this is the cardinal sin. "It's obviously clear" is how unused skills get written.

## Anatomy of a SKILL.md

```
---
name: active-verb-first-name
description: <one capability clause> — Use when <triggers/symptoms/phrases>. Not for <neighbour> — that's <other-skill>
---

# Name
## Overview  — core principle in 1–2 sentences
## <the meat> — recipe, passes, or reference; tables over prose
## Common Mistakes — what goes wrong and the fix
```

## The Rules That Matter Most

- **Description = one capability clause + triggers + one exclusion clause; never the procedure.**
  Name *what the skill does* in a phrase, then the triggers ("Use when…" — symptoms and the phrases a
  user would actually type). When a near-neighbour skill exists, end with a "Not for X — that's
  **other-skill**" clause: with ~20 skills in the suite, invocation is unreliable and the wrong one
  gets picked without it. **Never summarize the workflow** — agents follow a described workflow
  *instead of* reading the skill, and act on the summary's gaps. State *what* and *when*, never *how*.
- **Name for what you do.** Active, verb-first: `subtraction-first`, not `code-reduction`;
  `naming-as-design`, not `naming-utilities`. Gerunds work well for processes.
- **Keywords an agent would search for** — real phrases, error strings, symptoms — scattered
  through the description and body, so the skill is *found* when it's needed.
- **Cross-reference by name, never by `@`.** Write `**REQUIRED SUB-SKILL:** Use **naming-as-design**`.
  An `@`-link force-loads the file and burns context before it's wanted.
- **One good example beats five languages.** Port later if you must. Contrived templates teach nothing.
- **Tables and guard-clause snippets over paragraphs.** Skills are scanned, not read.

## Match the Form to the Failure

| The baseline failure is… | Write… |
|---|---|
| Knows the rule, breaks it under pressure | A hard rule + a rationalization table that names each excuse and answers it |
| Does the right thing but the output is misshapen | A positive recipe: state what the output *is*, in order |
| Leaves out a required piece | A structural slot they must fill, not a prose reminder |
| Behavior should depend on a condition | A conditional keyed to something observable |

Prohibitions ("don't do X") backfire on shaping problems — under a competing incentive the agent
negotiates with them. A recipe leaves nothing to negotiate.

## Common Mistakes

- **Narrative instead of technique.** "In this project we found…" — strip the story, keep the move.
- **Description that leaks the workflow.** The most common and most damaging error. Capability +
  triggers + exclusion — never the how.
- **No exclusion clause when a sibling exists.** Two skills with overlapping triggers both fire, or
  the wrong one wins. Name the boundary: "Not for X — that's **sibling**".
- **Rewriting the rule on one surprise.** A single odd case is an anecdote. Change a skill (or this
  rubric) when the *same* friction recurs, not on the first exception — otherwise the process churns
  faster than it learns.
- **Skill for something a regex could enforce.** If it's mechanically checkable, automate it; save
  skills for judgment calls.
- **Shipping untested.** A skill you didn't watch change behavior is a guess, not a skill.
