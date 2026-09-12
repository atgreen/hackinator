---
name: shaping
description: Use at the very start of any non-trivial build, BEFORE writing code or scaffolding — turning a rough idea into an understood, agreed direction. "let's build X", "I want to make Y", "how should I approach Z", or any request where the goal isn't yet pinned down. Not for turning an already-agreed design into ordered tasks — that's planning
---

# Shaping

## Overview

**Core principle:** Resolve unclear intent and consequential design choices *before* building. The
cheapest place to fix a design is in conversation; the most expensive is in code you've already
written. Shaping is where you subtract features, choose an approach, and establish a shared
direction.

## The Decision Gate

```
NO CODE WHILE A MISSING CHOICE WOULD MATERIALLY CHANGE THE RESULT
```

Do not guess through material ambiguity. But do not invent ambiguity either: an explicit request to
implement a clear, bounded change supplies intent, and a previously approved design stays approved.
In those cases, skip shaping and continue with planning or implementation.

## Classify, and Announce It

State the path out loud so the human can correct you. Complexity only *upgrades* the path.

- **Spike** — "can this even be done?" → shaping is one line: state the question, then go probe (**spike-and-stabilize**).
- **Bounded but unclear** — a contained change with one material uncertainty → resolve it briefly,
  record the result, then build.
- **Bounded and explicit** — the request already pins down the result → shaping is unnecessary.
- **Architectural** — new system, real choices → the full dialogue below, ending in a written design and the **planning** skill.

## How to Shape

1. **Ask only questions whose answers change the result.** Ask one at a time. A wall of ten
   questions gets skimmed and half-answered. Prefer multiple-choice when the options are genuinely
   discrete; wait for the answer before the next consequential decision.
2. **Propose alternatives when a real trade-off exists.** Usually offer 2–3 approaches with a
   recommendation. Do not manufacture options for a bounded request with one obvious implementation.
3. **Subtract ruthlessly (YAGNI).** For every feature, ask "does the first real version need this?"
   Default to no. The smallest thing that delivers the core is the thing to build.
4. **Present architectural designs in sections.** Don't dump a monolith. Goal → approach → the
   shape of the pieces, checking in at consequential decisions. Course-correction is cheap here.

## What Shaping Produces

- **Spike/unclear bounded work:** a short, agreed description of what you're about to build —
  captured as a **bead** in a Git repository.
- **Architectural:** a written design (goal, chosen approach, the pieces and how they fit, what's
  explicitly out of scope), self-reviewed for gaps/placeholders/scope-creep, then **approved by the
  human**. The only next step is **planning**.

File the work as beads (**using-beads**) as it firms up — the shape *is* the initial backlog.

## When Stuck on the Idea Itself

If the design has real, hard trade-offs you can't resolve, this is a good moment for an outside
voice — **consulting-codex** for a second opinion — *before* committing to a direction.

## Common Mistakes

- **Building through a material unknown.** Resolve the choice that changes the result first.
- **Re-approving explicit work.** A clear implementation request is already a direction; proceed.
- **Ten questions in one message.** One at a time, multiple-choice where you can.
- **Presenting one approach as fait accompli.** Give options and a recommendation; let the human choose.
- **Gold-plating the design.** Every "wouldn't it be nice if…" is scope you'll pay for. Cut it now.
- **Treating a vague nod as approval of unresolved architecture.** Confirm the choices that actually
  affect scope or structure, not every sentence.
