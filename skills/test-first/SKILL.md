---
name: test-first
description: Use when implementing keeper code — any behavior meant to last, and especially when fixing a bug. Triggers on writing a function/feature you intend to keep, "add a test", "TDD", or the urge to write the code first and test it "after"
---

# Test-First

## Overview

**Core principle:** For code you intend to keep, write the test **before** the code, and **watch it
fail** before you make it pass. A test written after the code asks "what does this do?"; a test
written first asks "what should this do?" — and only the second one can catch the code being wrong.

If you didn't watch the test fail, you don't know it tests the right thing. It might pass because of
a typo, a stubbed return, or nothing at all.

## The Iron Law

```
NO KEEPER CODE WITHOUT A FAILING TEST FIRST
```

Wrote the code before the test? Delete it and start over. Not "keep it as reference," not "adapt it
while I write the test" — **delete**. The value was the *watched failure*, and you can't get it back
by testing code that already works.

## Scope: What Counts as "Keeper"

This law governs **code meant to last**. It does **not** govern:

- **Spikes and throwaway probes** — exploration is exempt *by design*. That's the whole point of
  **spike-and-stabilize**: learn in the ugly spike, then rebuild the answer test-first in the
  stabilize phase. The spike is where you're allowed to skip tests; the keeper version is not.
- **Generated code, config, and trivial declarations** with no behavior to test.

When in doubt about whether something is a keeper, it's a keeper.

## RED → GREEN → REFACTOR

1. **RED** — write one small test for one real behavior. Real behavior, not a mock of it.
2. **Watch it fail (mandatory).** Run it. Confirm it fails *for the right reason* — the behavior is
   missing, not the test is misspelled. A test that fails because of a typo has told you nothing.
3. **GREEN** — write the *simplest* code that passes. No extra generality, no features the test
   didn't ask for. Then run it: this test passes, and every other test still passes.
4. **REFACTOR** — clean it up while staying green. No new behavior in this step (that needs its own
   RED). This is also where **whittler** naturally takes over for the craft pass.

## Bugs Get a Failing Test First

A bug fix starts with a test that *reproduces* the bug — and fails. Watch it fail (red), fix it
(green). That failing-then-passing test is your proof the bug is real and your guard against its
return. A "fix" with no reproducing test is a guess.

## Rationalizations — All Mean "Start Over"

| Excuse | Reality |
|---|---|
| "I'll write tests after" | Tests-after pass immediately and prove nothing. You skipped the watched failure. |
| "It's too simple to test" | Simple code breaks too, and a simple test costs seconds. |
| "I already tested it by hand" | Manual checks aren't repeatable and don't guard against regressions. |
| "I'll lose the code I wrote" | You keep the understanding, which is the part that mattered. Rebuild it green. |
| "This is basically a spike" | Then say so and treat it as one — throwaway. If you're keeping it, it's keeper code. |

## Common Mistakes

- **Skipping the watched failure.** GREEN that was never RED is a test you can't trust.
- **Over-building in GREEN.** Write only what the test demands; save generality for a test that needs it.
- **Adding behavior in REFACTOR.** New behavior needs a new failing test first.
- **Testing the mock instead of the behavior.** If the test would pass with the real logic deleted, it's testing nothing.
