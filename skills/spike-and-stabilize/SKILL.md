---
name: spike-and-stabilize
description: Use when a genuine unknown blocks progress — "can this even be done?", an unfamiliar API or library, an uncertain approach — and you're tempted to either research forever or build production code around something you don't yet understand
---

# Spike and Stabilize

## Overview

**Core principle:** When you don't know whether something is possible or how it behaves, write a
**throwaway probe** to find out — fast, ugly, deliberately disposable — then throw it away and
rebuild the answer cleanly. Learn in the spike; keep only in the stabilize.

A *spike* is an experiment, not a foundation. Its only product is knowledge. You are allowed to
write terrible code in a spike precisely because none of it survives.

## Why Two Phases

Trying to *learn* and *build well* at the same time does neither well: you write careful,
defensive, abstracted code around behavior you don't understand yet — and half of it is wrong
because your understanding was wrong. Separating the phases lets each be honest. The spike is
cheap because it's disposable. The rebuild is clean because you finally know the answer.

## The Two Phases

### Phase 1 — Spike (learn)

- **Timebox it.** Pick a limit up front (30 min, an afternoon). The clock forces the question to be sharp.
- **Answer one question.** "Can I get X from this API?" "Does this approach handle Y?" Write the ugliest code that answers it. No tests, no structure, no error handling.
- **Optimize for learning, not keeping.** Hard-code, `print`, copy-paste, comment out. It's scaffolding.
- **Write down what you learned** the moment you know it — the answer outlives the code.

### Phase 2 — Stabilize (keep)

- **Throw the spike away.** Delete it, or move it aside where it can't be mistaken for real code.
- **Rebuild for keeps** with everything you now know: clean structure, real error handling, tests.
- The rebuild is fast — the hard part (understanding) is already done.

## The Iron Rule

```
THE SPIKE DOES NOT GET PROMOTED
```

The single most common failure is the spike quietly becoming the product. It works, so why rewrite
it? Because it was written by someone who didn't understand the problem — you, an hour ago. Spike
code carries every wrong assumption you've since corrected, in code you stopped reading critically
the moment it worked.

| Rationalization | Reality |
|---|---|
| "It already works, rewriting is wasteful" | It works by luck around assumptions you've since disproven. |
| "I'll clean it up in place" | In-place cleanup keeps the wrong bones. Deletion forces the right ones. |
| "I'll lose the working version" | You keep the *knowledge*, which is the part that mattered. |
| "There's no time to rebuild" | The rebuild is the cheap phase. You already paid for the expensive one. |

**Genuine exception:** if the spike was trivial *and* you'd write it identically now, keeping it is
fine — but say so out loud ("keeping the spike; it's already what I'd write") rather than sliding
into it by default.

## Quick Reference

| Phase | Goal | Code quality | Fate |
|---|---|---|---|
| Spike | Answer one question | As ugly as it takes | Deleted |
| Stabilize | Ship the answer | Clean, tested | Kept |

## Relationship to Other Skills

The **builder** persona reaches for this when an unknown blocks the **walking-skeleton**. Once the
answer is stabilized, hand the clean result to **whittler** if it wants a final craft pass.
