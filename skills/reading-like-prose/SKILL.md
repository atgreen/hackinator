---
name: reading-like-prose
description: Use when making code a joy to read — a function is hard to follow top to bottom, nesting is deep, the reader has to scroll up to understand, or high-level intent is buried under low-level detail
---

# Reading-Like-Prose

## Overview

**Core principle:** Code is read far more often than it's written, and mostly by someone with no
context — often you, months later. Structure it for that reader: top-down, one idea at a time, in
the order a person would want to learn it. Good code reads like a well-edited paragraph, not a
puzzle you assemble by jumping around.

## The Three Moves

### 1. One altitude per function

A function should operate at a single level of abstraction. High-level intent and low-level
mechanics in the same body forces the reader to change gears every line.

- The top-level function reads like a **table of contents**: named steps, each a call.
- Details live one level down, each in its own well-named function (see **naming-as-design**).
- If a function mixes "what we're doing" with "how a byte gets shifted," extract the *how*.

### 2. Read top-down, important-first

Order code the way a newspaper orders a story: headline first, details below.

- The thing the reader most wants to know goes **first** — the main path, the answer.
- Supporting detail comes **after**, so the reader never scrolls *up* to understand what they're reading.
- Define-before-use is a compiler's need, not a human's. Where the language allows, order for the human.

### 3. Flatten the happy path

Deep nesting hides the main story inside a staircase of conditions.

- **Return early** on the exceptional cases — guard clauses at the top — so the happy path runs down the left margin, unindented.
- Handle errors and edge cases *and get them out of the way*, rather than wrapping the real work inside them.
- Prefer a flat sequence of steps to a pyramid of `if/else`.

```
# staircase — the real work is buried three levels deep
if user:
    if user.active:
        if user.has_permission:
            do_the_thing()

# prose — exceptions handled and dismissed; the point runs down the margin
if not user:               return denied("no user")
if not user.active:        return denied("inactive")
if not user.has_permission: return denied("forbidden")
do_the_thing()
```

## Quick Reference

| Symptom | Move |
|---|---|
| Reader scrolls up to understand | Reorder important-first |
| Function changes altitude mid-body | Extract the low-level part |
| Three-deep `if` staircase | Guard clauses, return early |
| "What does this whole block do?" | Extract it and name it |
| Detail before the main point | Put the point first |

## Common Mistakes

- **Extracting into badly-named fragments.** Splitting a function into `helper1`/`helper2` moves
  the confusion, it doesn't cure it. Extraction only pays off with names that read (**naming-as-design**).
- **Flattening past clarity.** Ten early returns can be as hard to follow as deep nesting. The goal
  is a readable story, not a metric of zero indentation.
- **Reordering that fights the language.** Some languages need define-before-use. Order for the
  human *within* what the language allows; don't break the build for aesthetics.
- **Turning prose into golf.** Collapsing readable steps into one dense expression is the opposite
  of this skill. Elegance is *low effort to read*, not fewest lines.

## Relationship to Other Skills

This is the **whittler**'s third pass. It depends on **naming-as-design** (extraction is only
worthwhile with good names) and often follows **subtraction-first** (flattening removes structure
outright rather than reorganizing it).
