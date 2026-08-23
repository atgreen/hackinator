---
name: finishing
description: Use when an implementation is complete and ready to land — deciding how it integrates and cleaning up. "finish this", "land it", "wrap up", "ship it", "merge", "make a PR", "I'm done — now what"
---

# Finishing

## Overview

**Core principle:** Landing work is a sequence with a human decision in the middle: **prove it's
green → figure out where you are → let the human choose how it integrates → execute that → clean up.**
How work integrates — and especially whether it's ever discarded — is the human's call, not yours.

## Step 1 — Prove It's Green (on the tree you'll integrate)

Run the **full** test/build suite on the actual code about to land, right now. A green run from
before your last change does not count (**evidence-before-claims**). Red suite → stop and fix, or
surface it; don't land red.

## Step 2 — Detect Where You Are

You can't present the right options until you know the git situation:

```bash
[ "$(git rev-parse --git-dir)" != "$(git rev-parse --git-common-dir)" ] && echo "linked worktree" || echo "main checkout"
git branch --show-current   # empty output = detached HEAD (needs a branch before it can land)
```

## Step 3 — Confirm the Base Branch

Which branch does this integrate into (`main`, `develop`, …)? Confirm it before offering to merge —
don't assume.

## Step 4 — Present the Menu, Then Wait

Offer exactly these, and **stop for the human to choose** — do not pick for them:

1. **Merge locally** into the base branch.
2. **Push and open a PR.**
3. **Keep the branch as-is** (integrate later).

(Detached HEAD: first create a branch, or offer only "keep" until one exists.)

**Discarding work is not on this menu by default.** Only discard on an explicit request, and only
after the human confirms by typing the literal word **`discard`** — losing work must be deliberate,
never a default or a misread.

## Step 5 — Execute, Then Close the Loop

- Do the chosen action. Pushing or opening a PR is an **external side effect** — a gate; confirm intent first.
- **Close the beads** this work completed (`bd close <id>`), comment any follow-ups discovered, and
  **`bd sync`** so the shared record is current (**using-beads**).
- **Clean up the worktree** if you made one: `git worktree remove <path>` (never a hand `rm -rf`;
  never `--force` past a refusal — if it refuses, show the human the uncommitted files and ask).

## Common Mistakes

- **Landing on a stale green.** Re-run the full suite on the final tree; earlier passes don't certify it.
- **Merging without asking.** Integration is the human's decision. Present the menu; wait.
- **Discarding on a vague "scrap it."** Require the typed `discard`. Work is expensive; deletion is forever.
- **Force-removing a worktree with uncommitted changes.** That's silent data loss. Surface the files and ask.
- **Leaving beads open.** Unclosed beads rot the backlog; unsynced ones don't reach the next session. Close and sync.
