---
name: hacking-workflow
description: Use at the START of any non-trivial build or change in a git repo — "let's build X", "hack on X", "start a hacking session", "run the loop", "new project", "implement this". The spine that sequences shaping → planning → build → craft → verify → review → finish, with human-approval gates
---

# Hacking Workflow

## Overview

**Core principle:** Real work runs a loop with **gates** — points where a human decides and where
you must *prove* progress before advancing. The loop keeps momentum honest: you never drift from a
vague idea straight into code, and you never call something done without evidence. This skill is the
spine; each phase is its own skill it hands off to.

**This is the front door.** When a build starts, run the loop. Right-size the ceremony to the work
(a spike skips most of it) but **never skip a human-approval gate.**

## Classify First (right-size the loop)

Announce which path you're on. Complexity can only *upgrade* the path, never downgrade it.

| Path | What it is | Loop |
|---|---|---|
| **Spike** | "Can this even be done?" throwaway probe | `spike-and-stabilize` only, report back. Skip the rest. |
| **Bounded** | A clear, contained change | Shape briefly → build → verify → finish. Skip the plan doc. |
| **Architectural** | New system, many parts, real design choices | The full loop below. |

## The Loop

Track the whole thing in **beads** from the first phase (**using-beads**) — file the work, close as you go.

```
Phase 0 — SHAPE       understand the goal, weigh approaches, get buy-in
   → shaping.  GATE: the human approves the intent/design before ANY code.

Phase 1 — ISOLATE     a clean workspace so nothing races or leaks onto main
   → using-worktrees.  GATE: clean baseline (builds/tests green, or human OKs).

Phase 2 — PLAN        (architectural only) map files + right-sized tasks, file as beads
   → planning.  GATE: plan filed; pick execution mode (subagents vs inline).

Phase 3 — BUILD       make it work, thinnest slice first
   → builder (walking-skeleton, spike-and-stabilize). Keeper code is test-first → test-first.

Phase 4 — CRAFT       make it elegant, behavior-preserving
   → whittler.

Phase 5 — VERIFY       prove it actually works, with fresh evidence
   → evidence-before-claims.  GATE: no "done" without fresh command output.

Phase 6 — REVIEW       an independent pass before it lands
   → reviewing-work (fresh reviewer subagent) and/or consulting-codex.  GATE: findings resolved by severity.

Phase 7 — FINISH       land it the way the human chooses; clean up
   → finishing.  GATE: full suite green; human picks merge / PR / keep.
```

Build and craft interleave per slice; verify and review gate each meaningful chunk, not just the end.

## Commit at Every Green Slice

```
GREEN EVIDENCE = COMMIT POINT
```

The moment a slice verifies — fresh output in hand (**evidence-before-claims**) — commit it on the
isolated branch, with the slice as the message. Uncommitted work must never outlive the slice that
produced it. A commit is a **checkpoint, not a publication**: this loop is your standing authority
to commit on the work branch; *pushing* and *landing* stay human gates (Phase 7).

| The excuse | The answer |
|---|---|
| "I'll commit when it's all done" | Then one bad edit can cost the session. Checkpoint the green. |
| "It's not clean enough to commit" | Clean is Phase 4's job. Commit the working ugly version — that's the block whittling carves from. |
| "It'll get squashed anyway" | Fine — squashing later is trivial. Recovering lost uncommitted work isn't. |

## The Gates Are Inviolable

Three things are the human's call, never yours, no matter the time pressure:
- **Phase 0** — approval of *what* you're building, before any code.
- **Phase 7** — *how* it lands (merge / PR / keep). Discarding work needs an explicit, typed confirmation.
- Anything **irreversible, security-sensitive, or externally visible** (push, publish, delete, spend).

Everywhere else, **decide and record the ruling** (in a bead) rather than stalling — momentum over paralysis.

## Common Mistakes

- **Skipping Phase 0 because the idea "is obvious."** Obvious ideas are where scope creep hides. Get buy-in.
- **Coding on `main`.** Isolate first (Phase 1), or you can't cleanly abandon a bad path.
- **Claiming done from Phase 3.** "It compiles" is not "it works." Phase 5 exists for a reason.
- **Hoarding changes until Phase 7.** A wall of uncommitted work is unreviewable and one mistake from gone. Green slice → commit, every time.
- **Running the full loop for a spike.** Ceremony must match the work. Classify first.
