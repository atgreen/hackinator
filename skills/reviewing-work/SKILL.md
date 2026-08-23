---
name: reviewing-work
description: Use after finishing a task or feature and before it lands — getting an independent review, and handling the feedback well. "review this", "code review", "check my work", or when receiving review comments (from a person, a subagent, or Codex)
---

# Reviewing-Work

## Overview

**Core principle:** Fresh eyes catch what yours can't — you're too close to code you just wrote.
Review **early and often** (per meaningful chunk, not just at the end), get it from a context that
*doesn't share your assumptions*, and engage the feedback as a technical evaluation, not a social
one. Two halves: **getting** the review, and **receiving** it well.

## Getting a Review — Use Fresh Context

The reviewer must not inherit your session's history and rationalizations. Give it exactly what it
needs, constructed on purpose:

- **A fresh reviewer subagent** (**dispatching-subagents**) with a crafted brief: the diff range
  (base…head), what the change is meant to do, the requirements/constraints it must meet, and "return
  severity-ranked findings." It keeps the diff in *its* context; only the findings come back to you.
- **Or an independent model** — **consulting-codex** in review or challenge mode for a second opinion.

Mandatory after each task in a fan-out, after a major feature, and before anything merges. "It's
simple" is not a reason to skip — simple changes carry the bugs you stopped looking for.

## Receiving a Review — Technical, Not Emotional

Review is evaluation of the *code*, not of you. Respond to the substance.

**Forbidden reflexes:** "You're absolutely right!", "Great catch!", "Thanks so much!" — performative
agreement and gratitude. They add nothing and often precede applying a *wrong* fix to please the
reviewer. **State the fix (or the disagreement) instead.**

**The response pattern for each item:** READ → UNDERSTAND → VERIFY (is it actually true for *this*
code?) → EVALUATE (does the fix fit, or does it break something / violate YAGNI?) → RESPOND → IMPLEMENT.

- **If any item is unclear, STOP and clarify all items before implementing any** — items can be
  related, and fixing one blind can undo another.
- **Verify before implementing.** A reviewer (especially an external model) can be wrong for *this*
  codebase. Check the claim: does it reproduce? does the fix break a caller? `grep` for real usage.
- **Push back with reasoning** when the feedback is wrong, YAGNI, or wrong-for-this-stack. A reasoned
  "no" is a valid review outcome. Agreement is not the goal; correctness is.

## Act by Severity

| Severity | Action |
|---|---|
| **Critical** (breaks, unsafe, wrong) | Fix immediately, before anything else. |
| **Important** (real problem, not breaking) | Fix before proceeding past this chunk. |
| **Minor** (style, nit, maybe-later) | Note it — file a **bead** if deferring — don't let it block. |

Order the fixes blocking → simple → complex. **Verify each fix** (**evidence-before-claims**) and
confirm no regressions before moving on. Then, if the reviewer raised anything load-bearing, one
scoped re-review of just those changes.

## Common Mistakes

- **Reviewing with your own warm context.** You'll rubber-stamp your own reasoning. Use a fresh reviewer.
- **Performative agreement.** "You're so right!" then a wrong fix. Verify, then state what you're doing.
- **Applying external feedback blindly.** Wrong-for-this-codebase advice sounds authoritative. Check it against reality.
- **Batch-implementing unclear items.** Clarify everything first; related items fixed in isolation collide.
- **Letting minor nits block the merge.** File them as beads and move; don't gold-plate under review.
