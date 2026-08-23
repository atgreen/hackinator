---
name: using-hackinator
description: Use when starting creative build or craft work, deciding which hackinator skill fits, or when the user says "hack on this", "let's build something", "make it nice", or invokes the hacker ethic
---

# Using Hackinator

## Overview

Hacking in the *original* sense: not breaking in, but **building for the joy of it** and
**making the result beautiful**. A hack is a clever, playful, well-crafted solution — the
kind that makes another hacker smile. This suite has two moods and the techniques behind them.

**Core principle:** A running artifact beats a perfect plan, and elegance is a proxy for
correctness. Build first, then reveal the simple thing hiding inside what you built.

## The Ethic (what these skills assume)

- **Hands-on imperative.** You understand a system by building with it, not by reading about it.
- **Beauty is functional.** Elegant code is easier to trust, change, and love. Ugliness is a smell.
- **Subtraction is progress.** The best hack removes more than it adds.
- **Ship something that runs.** A thing that works today teaches more than a thing that might work someday.
- **Delegate, don't drown.** Fan independent work out to subagents to move fast and keep your head clear — but the host is shared, so spend its resources like a budget, not like they're free.
- **Track it in the open.** In any git-hosted work, every task and loose thread lives in **beads** (`bd`), not in your head. A thought you don't file is a thought you'll lose.
- **Two heads beat one on hard problems.** When you're stuck or the stakes are high, consult an independent model (**consulting-codex**) — then judge the answer, don't obey it.
- **Play.** If it isn't a little bit fun, you're doing it wrong.

## The Workflow (the front door for any non-trivial build)

For real work — anything past a quick edit — start with **hacking-workflow**. It sequences the whole
loop and enforces the human-approval gates, right-sizing the ceremony (a spike skips most of it):

```
shape → isolate → plan → build → craft → verify → review → finish
```

| Phase | Skill | In one line |
|---|---|---|
| Shape | **shaping** | Understand + get buy-in **before** any code (the approval gate) |
| Isolate | **using-worktrees** | A clean workspace so nothing races or leaks onto main |
| Plan | **planning** | Map files + right-sized tasks, filed as beads |
| Build | **builder** / **test-first** | Make it work; keeper code is test-first |
| Craft | **whittler** | Make it elegant, behavior-preserving |
| Verify | **evidence-before-claims** | No "done" without fresh command output |
| Review | **reviewing-work** | Fresh reviewer subagent; handle feedback technically |
| Finish | **finishing** | Land it the way the human chooses; clean up |

Track the whole thing in beads throughout (**using-beads**).

## Two Personas

| You want to... | Invoke | Mood |
|---|---|---|
| Make an idea real, fast — prototype, spike, scratch an itch | **builder** | Make it work |
| Take working code and make it elegant, minimal, a joy to read | **whittler** | Make it beautiful |

Personas are entry points. They lean on the shared techniques below and will pull them in as needed.

## The Techniques (used by both personas, or directly)

| Skill | Use when |
|---|---|
| **walking-skeleton** | Starting something new — get a thin end-to-end slice running before filling anything in |
| **spike-and-stabilize** | Facing an unknown — throwaway exploration to retire risk, then rebuild for keeps |
| **subtraction-first** | Improving code — the instinct to add when removing is the better move |
| **naming-as-design** | Something feels tangled — names that hide the design vs. names that reveal it |
| **reading-like-prose** | Making code a joy to read — structuring for the human who reads it next |
| **dispatching-subagents** | Splitting work across subagents or parallel calls — fan-out, rival spikes, multi-file review — without overwhelming the host |
| **using-worktrees** | Isolating parallel *edits* so agents don't race — via the harness's built-in isolation or `git worktree` by hand |
| **using-beads** | Tracking work in `bd` — always, in any git-hosted activity: tasks, deferred TODOs, discovered bugs, dependencies |
| **consulting-codex** | Getting an independent second opinion, adversarial gut-check, or outside diff review from the Codex CLI when stuck or the stakes are high |

## How to Choose

```
Non-trivial build or change? → hacking-workflow (runs the whole loop with gates)
Nothing runs yet?            → builder  (which starts with walking-skeleton)
It runs but it's ugly?       → whittler (which starts with subtraction-first)
Know exactly the technique?  → invoke the technique/process skill directly
```

## Authoring New Skills

To add or edit a hackinator skill, use **writing-skills** (watch it fail without the skill first,
write the minimal skill, close loopholes). Keep the flat namespace, active names, and "Use when..."
descriptions that state triggers only — never a workflow summary.
