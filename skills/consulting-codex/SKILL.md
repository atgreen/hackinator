---
name: consulting-codex
description: Use when stuck on a tricky problem, second-guessing a design decision, or wanting an independent model to cross-check or try to break your work — "ask codex", "second opinion", "am I missing something", "another set of eyes", "is this right"
---

# Consulting Codex

## Overview

**Core principle:** When a problem is genuinely hard, a second, independent model is worth more than
another lap of your own reasoning. Codex (OpenAI's CLI) is a peer you can consult — for a fresh
answer, an adversarial gut-check, or an outside diff review. Consult it, weigh what it says, and
decide for yourself. **You are asking a colleague, not obeying an oracle.**

This runs both ways: a Codex session stuck on something can consult *you* the same way, by shelling
out to `claude -p "<prompt>"`. The pattern is symmetric; the mechanics below are the Claude→Codex direction.

## When to Consult (and When Not To)

**Consult when:**
- You're genuinely **stuck** — the root cause eludes you after an honest attempt, not on first friction.
- A **design decision** has real trade-offs and you want an independent voice before committing.
- You're about to ship something **risky** and want an adversary to try to break it first.
- You suspect you're **missing something** — a second reading catches what your first one rationalized past.

**Don't consult when:**
- You can look it up or read the code yourself — that's faster and doesn't burn an external call.
- It's routine work — consulting on every step is latency and noise, not diligence.
- You're using it to **avoid thinking**. Consult *after* forming your own view, so you can judge the answer.

Codex calls are **slow and external** — treat each like a heavy job on the host budget: timeboxed,
one focused question at a time, not a loop you spam. (See **dispatching-subagents** for the budget mindset.)

## First: Is It Available?

```bash
command -v codex || echo "codex CLI not installed"
```

Auth is via `codex login` (or `$CODEX_API_KEY` / `$OPENAI_API_KEY`). If it's missing or unauthenticated,
tell the user how to enable it rather than silently skipping the consult.

## Craft the Prompt — Codex Starts Blank

Codex does **not** see your session. Same discipline as briefing a subagent (see **dispatching-subagents**):
paste the code, the diff, the error, the constraints — everything needed to understand the problem —
then ask a sharp question and **name the output you want** (a verdict, the flaw, a recommendation with reasoning).

## The Three Modes

Run read-only, high reasoning, under a timeout. `-s read-only` keeps Codex from editing your tree.

### Consult — get an outside answer

```bash
timeout 330 codex exec -s read-only -c 'model_reasoning_effort="high"' \
  "Here is the problem. <paste context: code, error, what you've tried>.
   Question: <the sharp question>. Give your reasoning, then a clear recommendation." < /dev/null
```

### Challenge — adversarial gut-check

```bash
timeout 330 codex exec -s read-only -c 'model_reasoning_effort="high"' \
  "Try to BREAK this. <paste the code/design>. Find the strongest failure case,
   the edge that isn't handled, or the assumption that doesn't hold. Be specific." < /dev/null
```

### Review — independent diff review

```bash
timeout 330 codex review                 # reviews the current repo diff
timeout 330 codex review "<focus>"       # e.g. "focus on the concurrency in the writer"
```

Add `--json` to `codex exec` to stream reasoning traces if you want to see how it got there. Use
`-C <dir>` to point it at a specific repo root.

## After It Answers

1. **Show the user Codex's answer** — don't bury or silently absorb it. The outside voice has value *as* an outside voice.
2. **Judge it against your own understanding.** Codex is confidently wrong sometimes. Agreement is evidence; it isn't proof. Where you and Codex disagree, that gap is the interesting part — dig into it.
3. **Decide and say why.** "Codex flagged X; I checked and it's real, fixing it" or "Codex suggested Y; I'm not taking it because Z." You own the call.

## Common Mistakes

- **Consulting instead of thinking.** Form your own view first, or you can't evaluate the reply.
- **Under-briefing.** A vague prompt to a blank-slate model gets a vague answer. Paste the real context.
- **Obeying the oracle.** Blindly applying Codex's suggestion is how a confident wrong answer becomes your bug.
- **Spamming it.** One focused consult beats ten reflexive ones — and respects the runtime/host budget.
