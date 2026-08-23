---
name: dispatching-subagents
description: Use when work can be split across subagents or parallel tool calls — fan-out search, independent build/spike/review tasks, adversarial verification — or when deciding how many things to run at once without overwhelming the host or ballooning total runtime
---

# Dispatching Subagents

## Overview

**Core principle:** Delegate to go faster and to keep your own context clean — but treat the host
as a **budget**, not an infinite pool. The goal is *lower wall-clock*, not *maximum concurrency*.
Ten agents that make the machine swap are slower than three that don't.

Two wins from delegating, and they're different:

- **Parallelism** — independent work runs at once, so wall-clock ≈ the slowest chain, not the sum.
- **Context hygiene** — a subagent reads the haystack and hands you the needle; the file dumps
  never enter your context. Reach for this even when you *don't* need speed.

## Reach for a Subagent When

- **Fan-out search / exploration** — "where is X handled", sweeping many files or naming conventions. Delegate; keep the conclusion, not the excerpts.
- **Independent tasks** — spikes of two rival approaches, reviewing N files, building M targets — anything with no ordering dependency between the pieces.
- **Adversarial verification** — spawn independent skeptics to try to *refute* a claim (behavior unchanged? bug real?). Diverse lenses catch what one pass misses.
- **Anything that would flood your context** with output you won't keep.

## Don't When

- **Steps depend on each other** — B needs A's output. Delegating then blocking on it buys nothing but overhead.
- **It's one known lookup** — you know the file and symbol. Just read it.
- **The work is smaller than the dispatch cost** — spawning an agent to save five seconds loses.

## Free Parallelism First

Independent **tool calls in a single message run concurrently** — no subagent needed. Before
spawning anything, batch the handful of independent reads/greps into one message. Use subagents
when you need context isolation or genuine fan-out beyond a few calls.

## The Host Budget

Classify every unit of work before deciding how wide to go:

| Class | Examples | How wide |
|---|---|---|
| **Cheap / read-only** | Read, Grep, Glob, search agents, analysis | Fan out — but cap ~5–8. More adds coordination churn, not speed. |
| **Heavy / compute** | build, compile, full test suite, install, render, containers, DB | Serialize, or cap to **≤ (cores − 2)**. Never run N full builds at once. |

**Heuristic:** heavy jobs concurrent ≤ `nproc − 2`; cheap agents a flat ~5–8. When mixing, the
heavy class sets the limit — a single build can saturate the machine on its own.

## Before a Wide Fan-Out

1. **Scout first.** Send *one* agent (or one check) to confirm the approach before launching
   twelve down the same dead end. Cheap insurance against expensive mistakes.
2. **Know the machine.** `nproc` for cores; check current load. On a busy laptop, dial it down —
   your fan-out shares the host with the user's editor, browser, and running app.
3. **Pipeline over barrier.** Don't make fast agents idle waiting for the slowest before *any*
   result moves on. Let each result flow to its next stage as it lands; wall-clock drops and
   fewer agents sit live at once.
4. **Chunk huge lists.** 200 files is not 200 agents (a thundering herd). Batch into a handful of
   agents each handling a slice.

## Craft Each Agent's Task

A subagent starts blank — it does **not** inherit your context, so hand it exactly what it needs
and nothing it doesn't:

- **Focused scope.** One domain per agent ("fix the abort tests in X"), not "fix everything." Broad scope loses the agent.
- **Self-contained.** Paste the error text, the file path, the relevant facts. Don't assume it saw your session.
- **Constraints.** Say what *not* to touch — "tests only", "don't refactor production code" — or it may reshape the world.
- **Named output.** Tell it what to return (a summary, a verdict, the patch). Its final text *is* the result you get back — vague ask, vague result.

Dispatch all independent tasks **in one message** so they run at once. When they return: read each
summary, check the changes don't conflict, and run the full suite once to confirm they compose.

## Parallel *Edits* Need Isolation

Read-only fan-out is safe. **Concurrent edits are not** — two agents writing the same tree race and
corrupt each other. If parallel tasks mutate files, give each its own worktree, or partition so no
two touch the same file. When in doubt, parallelize the *reading/analysis* and serialize the *writing*.

→ **REQUIRED SUB-SKILL:** Use **using-worktrees** for the isolation mechanics — including the
harness's built-in `isolation: "worktree"` flag, which creates and cleans up the worktree for you.

## Common Mistakes

- **One agent per item for hundreds of items.** Thundering herd. Chunk it.
- **8 parallel test suites on a 4-core laptop.** Swap death; slower than running them in twos.
- **Fanning out before the approach is proven.** Scout with one, then widen.
- **Delegating a dependent step, then blocking on it.** No parallelism gained — just dispatch overhead.
- **Maximizing agent count.** Wall-clock is set by the slowest chain and the host's limits, not by how many agents you launched.
