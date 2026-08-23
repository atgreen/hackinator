---
name: using-beads
description: Use at the start of and throughout ANY git-hosted work — tracking tasks, deferred TODOs, discovered bugs, follow-ups, dependencies, or "while I'm here" ideas. Triggers include "beads", "bd", "track this", "backlog", "file an issue", "what's ready to work on", or noticing work you're about to only keep in your head
---

# Using Beads

## Overview

**Core principle:** In any git-hosted work, track it in **beads** — continuously, not as an
afterthought. `bd` is a git-native, dependency-aware issue tracker. Every task, deferred TODO,
discovered bug, and follow-up becomes a bead, so nothing is lost between sessions, ready-vs-blocked
work is always visible, and parallel agents (you, Codex, a future session) share one work-list.

**The rule here is: always, and frequently.** If you catch yourself holding a work item only in your
head or buried in a `// TODO` comment, that is the signal — **make it a bead now.**

**Beads vs. the harness todo list:** the in-session todo list is ephemeral scratch for *this* turn;
beads is the **durable, git-shared, cross-session** record. Use beads for anything that outlives the
current train of thought or that another agent might pick up.

## The Habit

### At the start of any git-hosted activity

```bash
bd ready            # what's unblocked and claimable right now?
bd status           # database overview, if you want the lay of the land
```

If the repo has no beads yet: `bd init` (fresh repo) or `bd bootstrap` (fresh clone of a repo that
already uses beads). Run `bd prime` any time you want the full, up-to-date agent workflow.

### Capture the moment work appears

Don't defer capture. The builder's "write it down, don't do it" and the whittler's "that's
out of scope" **are bead-creating moments**:

```bash
bd create "Handle the empty-input edge case" -t task -p 2
bd q "Flaky test in writer_test — investigate"     # quick capture, prints only the ID
bd create "Refactor parser" --deps discovered-from:hackinator-12   # link where it came from
```

### Model what blocks what

The whole payoff of beads is that ready work surfaces itself once dependencies are recorded:

```bash
bd dep add hackinator-5 hackinator-3    # 5 is blocked by 3 (3 must finish first)
bd dep tree hackinator-5                # visualize
```

### Move work through its states

```bash
bd update hackinator-5 --status in_progress   # claim it
bd comment hackinator-5 "Root cause was X"    # progress notes live on the bead
bd close hackinator-5                          # done
```

### Share it — it's git-hosted, so sync

```bash
bd sync             # pull, reconcile, push the federation loop
# or, minimally:
bd dolt push        # push beads to the remote so other sessions/agents see them
```

## With Parallel Agents

Beads is how a fan-out shares work without racing (see **dispatching-subagents**). Each agent can
atomically claim the next ready item instead of you hand-partitioning:

```bash
bd ready --claim --json    # atomically claim the first ready issue; returns it as JSON
```

File the work as beads with dependencies, then let agents pull ready issues. Blocked work stays
hidden until its blocker closes.

## Quick Reference

| Do | Command |
|---|---|
| See claimable work | `bd ready` |
| Create an issue | `bd create "Title" -t task -p 2` |
| Quick capture (ID only) | `bd q "Title"` |
| Record a blocker | `bd dep add <blocked> <blocker>` |
| Claim / progress / finish | `bd update <id> --status in_progress` · `bd comment <id> "…"` · `bd close <id>` |
| Push to remote | `bd sync` (or `bd dolt push`) |
| Full agent workflow | `bd prime` |

## When It's Overkill

Genuinely one-shot work in no repo, or throwaway scratch — skip it. Everywhere else in a git repo,
the default is **on**. When unsure, file the bead; a cheap bead beats a lost thought.

## Common Mistakes

- **Keeping work in your head or in code comments.** That's the exact failure beads exists to prevent. File it.
- **Batch-filing at the end.** Capture *as work appears* — end-of-session recall drops the small stuff, which is most of it.
- **Recording no dependencies.** Beads without deps is just a list; the ready/blocked view is the point. Link blockers.
- **Never syncing.** Unpushed beads don't help the next session or another agent. Sync so the shared memory is actually shared.
