---
name: subtraction-first
description: Use when improving existing code and the instinct is to add — a wrapper, a flag, a layer, a helper, a config option — before checking whether removing something is the better move; or when code feels bloated, over-engineered, or hard to hold in your head
---

# Subtraction-First

## Overview

**Core principle:** Before adding anything, try to remove something. The best improvement is
usually a deletion. Reach for subtraction *first* and adoption only when subtraction fails.

Humans — and models — have a documented bias toward solving problems by adding rather than
removing, even when removing is simpler and better. The bias is invisible from the inside, which
is exactly why it needs a rule: **make deletion the default hypothesis, not the last resort.**

## The Question to Ask First

Not "what should I add to make this better?" but:

> **What could I remove and have this be *just as good or better*?**

Run down the list before you write a single new line:

- **Dead code** — unreachable branches, unused functions, commented-out graveyards.
- **Unused parameters and options** — arguments nobody passes, flags nobody flips.
- **Speculative generality** — abstraction built for a second caller that never arrived.
- **Forwarding layers** — a wrapper whose whole job is to call one other thing.
- **Defensive checks that can't fire** — guards against states the type system or callers already forbid.
- **Comments that restate the code** — delete the comment or fix the name it's apologizing for.
- **Whole features** — the option nobody uses is a cost everyone pays. Removing it is a feature.

## The Discipline

```
NO ADDITION UNTIL SUBTRACTION HAS BEEN TRIED AND FAILED
```

When you catch yourself about to add:

1. **State what you're about to add and why.**
2. **Find the deletion that would solve the same problem.** There usually is one.
3. **Only if no deletion works, add — and add the smallest thing.**

| You're about to add... | Try removing instead... |
|---|---|
| A config option for two behaviors | One of the two behaviors |
| A wrapper to adapt an awkward interface | The awkwardness in the interface |
| A special case for weird input | The path that produces the weird input |
| A comment explaining a tricky line | The trickiness (rename, split, flatten) |
| A helper to reduce duplication | The duplication's cause — often one thing pretending to be two |
| A flag to make behavior optional | The reason anyone wanted it optional |

## When Subtraction Is Wrong

Subtraction is the *default*, not a mandate. Don't remove:

- Behavior something actually depends on. **Prove it's unused before deleting** — a grep, a test, a run — never assume.
- Clarity. Removing a well-named intermediate to save a line can *raise* the cost of understanding. Subtract effort-to-understand, not just tokens.
- Intentional roughness — a loud crash, a blunt escape hatch, a `TODO` left on purpose.

The goal is *less to understand and maintain*, not the smallest possible diff.

## Signs You're Adding When You Should Subtract

- The fix makes the file longer and you feel vaguely worse about it.
- You're writing a comment to explain why the new thing is necessary.
- The new abstraction has exactly one caller.
- You're adding a flag whose two branches barely differ.

**Any of these: stop. Ask what deletion solves the same problem.**

## Relationship to Other Skills

This is the **whittler**'s first pass. It pairs with **naming-as-design** (a better name often
deletes a comment or a helper) and **reading-like-prose** (flattening removes structure).
