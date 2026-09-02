---
name: shaping
description: Use at the very start of any non-trivial build, BEFORE writing code or scaffolding — turning a rough idea into an understood, agreed direction. "let's build X", "I want to make Y", "how should I approach Z", or any request where the goal isn't yet pinned down. Not for turning an already-agreed design into ordered tasks — that's planning
---

# Shaping

## Overview

**Core principle:** Understand the work and get the human's buy-in *before* building anything. The
cheapest place to fix a design is in conversation; the most expensive is in code you've already
written. Shaping is where you subtract features, choose an approach, and earn a "yes."

## The Iron Gate

```
NO CODE, NO SCAFFOLDING, NO IMPLEMENTATION SKILL UNTIL THE HUMAN HAS APPROVED THE INTENT
```

This gate is not negotiable and it does not shrink under time pressure. "It's obviously what they
want" is exactly the assumption that builds the wrong thing fast. Say what you intend to build; wait
for an explicit yes.

## Classify, and Announce It

State the path out loud so the human can correct you. Complexity only *upgrades* the path.

- **Spike** — "can this even be done?" → shaping is one line: state the question, then go probe (**spike-and-stabilize**).
- **Bounded** — a clear, contained change → a short in-chat design, one approval, then build.
- **Architectural** — new system, real choices → the full dialogue below, ending in a written design and the **planning** skill.

## How to Shape

1. **Ask one question at a time.** A wall of ten questions gets skimmed and half-answered. One
   sharp question per message, and **prefer multiple-choice** — it's faster for the human and
   surfaces options they hadn't named. Wait for the answer before the next.
2. **Propose 2–3 approaches with a recommendation.** Not one (looks like you didn't think) and not
   five (offloads the decision). Name the trade-offs; say which you'd pick and why.
3. **Subtract ruthlessly (YAGNI).** For every feature, ask "does the first real version need this?"
   Default to no. The smallest thing that delivers the core is the thing to build.
4. **Present the design in sections, approve as you go.** Don't dump a monolith. Goal → approach →
   the shape of the pieces, checking in at each. Course-correction is cheap here.

## What Shaping Produces

- **Spike/Bounded:** a short, agreed description of what you're about to build — captured as a **bead**.
- **Architectural:** a written design (goal, chosen approach, the pieces and how they fit, what's
  explicitly out of scope), self-reviewed for gaps/placeholders/scope-creep, then **approved by the
  human**. The only next step is **planning**.

File the work as beads (**using-beads**) as it firms up — the shape *is* the initial backlog.

## When Stuck on the Idea Itself

If the design has real, hard trade-offs you can't resolve, this is a good moment for an outside
voice — **consulting-codex** for a second opinion — *before* committing to a direction.

## Common Mistakes

- **Building during the conversation.** "I'll just scaffold while we talk" breaks the gate. Talk first.
- **Ten questions in one message.** One at a time, multiple-choice where you can.
- **Presenting one approach as fait accompli.** Give options and a recommendation; let the human choose.
- **Gold-plating the design.** Every "wouldn't it be nice if…" is scope you'll pay for. Cut it now.
- **Treating a nod as approval of everything.** Approve section by section; a vague "sounds good" isn't a yes to specifics.
