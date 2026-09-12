---
name: hacking-workflow
description: Coordinates a non-trivial git-hosted change from intent through verified integration. Use at the START when the user says "let's build X", "hack on X", "start a hacking session", "run the loop", "new project", or "implement this". Not for a quick direct artifact — that's builder
---

# Hacking Workflow

## Overview

**Core principle:** Real work runs a loop with **decision and evidence gates**. Resolve choices that
materially affect the result, then keep moving until fresh evidence supports the outcome. This
skill is the spine; each phase is its own skill it hands off to.

**This is the front door.** When a build starts, run the loop. Right-size the ceremony to the work
(a spike skips most of it), the host's capabilities, and the active authority boundaries.

Skills guide technique; they do not grant permission. System, user, host, and repository policy
decide which actions and capabilities are available.

## Classify First (right-size the loop)

Classify the path and state it briefly when that helps the user follow the work. Complexity can only
*upgrade* the path, never downgrade it.

| Path | What it is | Loop |
|---|---|---|
| **Spike** | "Can this even be done?" throwaway probe | `spike-and-stabilize` only, report back. Skip the rest. |
| **Bounded** | A clear, contained change | Shape briefly → build → verify → finish. Skip the plan doc. |
| **Architectural** | New system, many parts, real design choices | The full loop below. |

## The Loop

Track the whole thing in **beads** from the first phase (**using-beads**) — file the work, close as you go.

```
Phase 0 — SHAPE       resolve unclear intent and consequential design choices
   → shaping when needed. GATE: no unresolved choice that materially changes the result.

Phase 1 — ISOLATE     protect concurrent or risky edits when the host permits it
   → using-worktrees when useful. Otherwise work serially in the current workspace.
     GATE: understand the baseline and preserve unrelated changes.

Phase 2 — PLAN        (architectural only) map files + right-sized tasks, file as beads
   → planning. GATE: plan filed; pick a permitted execution mode.

Phase 3 — BUILD       make it work, thinnest slice first
   → builder (walking-skeleton, spike-and-stabilize). Keeper code is test-first → test-first.

Phase 4 — CRAFT       make it elegant, behavior-preserving
   → whittler.

Phase 5 — VERIFY       prove it actually works, with fresh evidence
   → evidence-before-claims.  GATE: no "done" without fresh command output.

Phase 6 — REVIEW       an independent pass before it lands
   → reviewing-work via the best available independent mechanism; use an adversarial self-review
     when none exists. GATE: findings resolved by severity.

Phase 7 — FINISH       follow the authorized integration choice; clean up
   → finishing. GATE: fresh relevant suite green; request a choice only when none was supplied.
```

Build and craft interleave per slice; verify and review gate each meaningful chunk, not just the end.

## Checkpoint Green Slices When Authorized

```
GREEN EVIDENCE = SAFE CHECKPOINT OPPORTUNITY
```

The moment a slice verifies — fresh output in hand (**evidence-before-claims**) — checkpoint it if
the active profile or user authorizes commits. A commit is not a publication, but this workflow is
not standing authority to create one. Without commit authority, preserve the working tree and
report the verified boundary clearly.

| The excuse | The answer |
|---|---|
| "I'll commit when it's all done" | If commits are authorized, a green checkpoint is safer and easier to review. |
| "It's not clean enough to commit" | Clean is Phase 4's job. An authorized working checkpoint can still be the block whittling carves from. |
| "It'll get squashed anyway" | Fine — squashing later is trivial. Recovering lost uncommitted work isn't. |

## Decision Boundaries

Proceed autonomously on reversible, in-scope work when the result is clear. An explicit request to
implement a clear, bounded change supplies intent; do not ask the user to approve it again.

Pause when:

- A missing product or design choice would materially change the result.
- An action is destructive, irreversible, security-sensitive, externally visible, or incurs real
  spend and has not already been authorized.
- The next requested integration, commit, sync, or push action lacks authority or conflicts with
  active policy.

Everywhere else, **decide and record the ruling** (in a bead) rather than stalling — momentum over paralysis.

## Common Mistakes

- **Re-asking after a clear implementation request.** Resolve real ambiguity; don't manufacture it.
- **Forcing isolation the host forbids.** Preserve unrelated changes and work serially in place.
- **Claiming done from Phase 3.** "It compiles" is not "it works." Phase 5 exists for a reason.
- **Treating the workflow as commit authority.** Checkpoint green slices only when active policy or
  the user permits commits.
- **Running the full loop for a spike.** Ceremony must match the work. Classify first.
