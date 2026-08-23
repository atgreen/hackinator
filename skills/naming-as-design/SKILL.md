---
name: naming-as-design
description: Use when code feels tangled or needs a comment to explain what something is, when reaching for a name and nothing fits, or when a name is vague (data, tmp, handle, process, manager, util, doStuff) and the fuzziness hides a fuzzy design
---

# Naming-as-Design

## Overview

**Core principle:** Naming is not decoration applied after the design — naming *is* the design.
A thing you can't name cleanly is usually a thing that isn't cleanly *one thing*. Use the struggle
to name as a signal about the structure, and renaming as a tool to fix it.

When the right name is obvious, the design underneath is sound. When no name fits, the name isn't
the problem — the shape is.

## The Diagnostic

A hard-to-name thing is telling you something. Read the signal:

| Naming symptom | What it usually means | The fix |
|---|---|---|
| The name needs "and" (`parseAndValidate`) | It does two things | Split it into two named things |
| Only a vague name fits (`data`, `manager`, `process`) | Its responsibility is vague | Sharpen the responsibility, then name it |
| The name lies about what it does now | Behavior drifted from intent | Rename to the truth, or restore the intent |
| You reach for a comment to say what it *is* | The name is underperforming | Move the comment's content *into* the name |
| Same concept, three different names across the file | You haven't decided what it is | Pick one true name, use it everywhere |

## The Practice

1. **Name for the reader, from the outside.** A name describes what a thing *is* or *returns*,
   in the caller's vocabulary — not how it's implemented inside. `activeUsers`, not `filteredList`.
2. **Make the name carry the weight a comment would.** `secondsUntilExpiry` needs no comment;
   `t` plus a comment does the same job worse. Every comment explaining a name is a naming bug.
3. **Let a failure to name change the code, not just the label.** If nothing fits, don't force a
   bad name — split, merge, or reshape until a good name becomes available. The name comes *last*
   because it's the design's signature.
4. **One concept, one name; one name, one concept.** Synonyms drifting across a codebase
   (`fetch`/`get`/`load`/`retrieve` for the same act) make readers hunt for distinctions that
   aren't there. Consistency is kindness.

## Quick Reference

| Weak name | Why it's weak | Stronger |
|---|---|---|
| `data`, `info`, `obj` | Says nothing | `invoice`, `userProfile` |
| `tmp`, `x`, `result` | No meaning | `remainder`, `parsedDate` |
| `handle`, `process`, `doIt` | Verb without object | `retryFailedJobs`, `renderInvoice` |
| `manager`, `helper`, `util` | Junk-drawer | Name the actual job it does |
| `flag`, `check`, `isValid` | Which flag? valid how? | `hasUnsavedChanges`, `isPastDue` |
| `getData()` returning a filtered subset | Hides the filter | `getActiveUsers()` |

## Common Mistakes

- **Naming by implementation, not by meaning.** `sortedList` breaks the day you switch to a set;
  `rankedCandidates` survives. Name the *what*, not the *how*.
- **Renaming the label without re-reading the passage.** A name is only better if the code around
  it reads better. Names live in sentences; read the sentence.
- **Encoding types into names** (`strName`, `listUsers`) when the language already tracks types.
  The name should add meaning the type can't.
- **Accepting a bad name because "it's just a local."** Locals are where the reader spends the
  most time. They deserve the most care, not the least.

## Relationship to Other Skills

This is the **whittler**'s second pass, after **subtraction-first** (a good name often deletes a
comment or a helper). Renaming for the reader flows directly into **reading-like-prose**.
