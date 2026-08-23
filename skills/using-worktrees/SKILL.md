---
name: using-worktrees
description: Use when parallel agents or experiments need to edit files without racing each other, when you want a throwaway branch you can build in and discard, or when the words "worktree", "isolation", or "keep main clean" come up
---

# Using Worktrees

## Overview

**Core principle:** A git **worktree** is a second working directory backed by the *same* repository,
checked out to its own branch. Two worktrees are two real folders that share history but have
completely separate files — so two agents can edit at once without stepping on each other, and a
risky experiment lives somewhere you can delete without touching your main checkout.

This is the isolation that makes **parallel *writing*** safe. Parallel *reading* never needs it —
see **dispatching-subagents**.

## When to Reach for One

- **Concurrent edits.** Two or more agents that will *write* files in parallel. Without isolation they race and corrupt each other's changes.
- **Throwaway experiments.** A spike you want to run for real but keep off your main branch.
- **Keeping main clean.** Work in progress stays on its own branch in its own directory; your primary checkout is untouched.

**Not worth it for:** read-only fan-out, or a single sequential edit. Worktrees cost disk and setup —
spend them only when writes actually collide. (Same host-budget instinct as everywhere else.)

## Step 0 — Are You Already Isolated?

**Before creating anything, check whether you're already in a worktree.** Harness-created isolation
fools the eye — don't stack a second worktree on top of one.

```bash
# In a linked worktree, the git-dir and the common git-dir differ
[ "$(git rev-parse --git-dir)" != "$(git rev-parse --git-common-dir)" ] && echo "linked worktree" || echo "main checkout"
# ...but a submodule also trips that test. If this prints a path, you're in a submodule, not a worktree:
git rev-parse --show-superproject-working-tree 2>/dev/null
```

Already in a linked worktree (and not a submodule)? **Skip creation — work where you are.**

## Prefer the Harness's Built-In Isolation

If you're dispatching a subagent that will edit files, let the runtime make and clean up the
worktree for you — no git commands, no orphans:

- **Agent tool:** pass `isolation: "worktree"`. The agent runs in a fresh worktree, auto-removed if unchanged.
- **Workflow steps:** pass `isolation: 'worktree'` on the agent call — exactly when parallel stages mutate files.

**Why prefer it:** the native tool owns placement, branch creation, and cleanup. Running `git
worktree add` when a native tool exists creates phantom state the harness can't see or manage —
the single most common worktree mistake. Reach for the flag first; drive git by hand only when you
need a worktree *yourself* (outside an agent) or the runtime offers no isolation.

## Driving It by Hand

```bash
# Pick a location the repo ignores, so worktree contents never get committed.
# Default to .worktrees/ at the project root; verify it's ignored first:
git check-ignore -q .worktrees || { echo ".worktrees/" >> .gitignore; git add .gitignore && git commit -m "ignore worktrees"; }

# Create a worktree on a NEW branch
git worktree add .worktrees/spike-idea -b spike/idea
cd .worktrees/spike-idea

# ...or check out an EXISTING branch into its own directory
git worktree add .worktrees/review review-branch

git worktree list                      # see what exists
git worktree remove .worktrees/spike-idea   # cleanup (NOT rm -rf)
git worktree prune                     # tidy metadata after any manual deletion
```

**If `git worktree add` fails with a permission/sandbox error:** don't fight it. Say the sandbox
blocked worktree creation and work in the current directory instead — serialize the writes rather
than isolating them.

To **keep** the work: commit on its branch, then merge or cherry-pick back into main. To **discard**
it: `git worktree remove` and the unmerged branch simply evaporates.

## Start From a Clean Baseline

A fresh worktree should build and pass tests *before* you change anything — otherwise every later
failure is ambiguous. Install deps (`npm install` / `cargo build` / `pip install` / as the project
needs) and run the test suite once. If the baseline is already red, report it before proceeding.

## Cleanup Is Not Optional

```
EVERY WORKTREE YOU CREATE, YOU REMOVE
```

Orphaned worktrees pile up disk and clutter `git worktree list`. Remove each when its work lands or
is abandoned. The built-in isolation flag does this for you — one more reason to prefer it.

## Rationalizations

| Excuse | Reality |
|---|---|
| "Obviously not in a worktree, no need to check" | Run Step 0. Harness isolation and submodules both fool eyeballing. |
| "`git worktree add` is quicker than finding the native tool" | The native flag owns placement, branching, and cleanup. Bypassing it leaves phantom state. |
| "The worktree dir is surely ignored" | Run `git check-ignore`. An unignored worktree commits the whole tree into the repo. |
| "Baseline tests can wait" | A dirty baseline makes every later failure ambiguous. Run them first. |
| "I'll `rm -rf` the folder when done" | Use `git worktree remove` — a hand-deleted folder leaves stale metadata. |

## Gotchas

- **One branch, one worktree.** Git won't check out the same branch in two worktrees at once.
- **Uncommitted work is lost on remove.** Commit first if you want to keep it.
- **Disk cost is real** on large repos — another reason worktrees are for genuine write-conflicts, not read-only fan-out.

## Relationship to Other Skills

**dispatching-subagents** decides *whether* to parallelize and how wide; this skill is *how* the
writing agents stay isolated when it does. **whittler** uses it when carving many files at once;
**builder** uses it for throwaway spikes it wants to run for real.
