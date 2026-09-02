---
name: evidence-before-claims
description: Use before claiming ANYTHING works, passes, is fixed, or is done — before every commit, PR, task hand-off, or "it should work now". Triggers on the urge to say done, or words like "should", "probably", "that fixes it", "all green". Not for writing the failing test that drives new code — that's test-first
---

# Evidence-Before-Claims

## Overview

**Core principle:** You may not claim something works until you have run the proving command **in
this message** and read its output. Evidence first, claim second — always. "Should work" is not a
status; it's a hope.

## The Iron Law

```
NO COMPLETION CLAIM WITHOUT FRESH VERIFICATION EVIDENCE
```

Fresh means *now*, in this turn — not "I ran it earlier," not "it passed last time." Code changed
since then, or you wouldn't be claiming anything. A prior green run does not certify the current tree.

## The Gate

Before any success claim, run this gate:

1. **IDENTIFY** the command that would *prove* the claim (the build, the test, the actual run that
   exercises the change — not a proxy).
2. **RUN it fresh and in full.** Not a subset, not `--fast`, not the one test you think matters.
3. **READ the whole output and the exit code.** Errors hide in the middle; exit code is the verdict.
4. **VERIFY** it actually shows what you're about to claim — the *right* thing passed, not just *something*.
5. **THEN claim** — and show the evidence.

If you can't run the proving command, you don't claim success; you say what you verified and what you didn't.

## This Applies to Paraphrases Too

The law covers the *meaning*, not just the exact word "done." "That should fix it," "all green,"
"ready to merge," "the tests are passing," "🎉 Perfect!" — every one is a completion claim and needs
fresh evidence behind it.

## Don't Trust Reports — Verify Them

When a subagent or tool reports success, that is a *claim*, not evidence. Verify it against reality —
the VCS diff, the actual output, the running artifact. Agents can be confidently wrong; "the
implementer said it's done" is not the same as "it's done."

## Red Flags — STOP, You're About to Claim Without Evidence

| Signal | What to do |
|---|---|
| "It should work now" | Run it. "Should" means you haven't. |
| "Perfect! / Done! / All set!" | Where's the command output? Run it first. |
| "The linter passed, so we're good" | A linter is not a build is not a test. Run the real proving command. |
| "The subagent reported success" | Verify via diff/output. Reports aren't evidence. |
| "I only changed one line" | One line breaks builds. Run it. |
| "I'm pretty sure the other tests still pass" | Sure isn't verified. Run the full suite. |

## Common Mistakes

- **Partial verification.** Running the one new test but not the suite — you've proven you didn't fix it *and* break three others… by not checking.
- **Reading the exit code but not the output** (or vice versa). You need both: green exit *and* the right thing in the log.
- **Stale evidence.** Output from before your last edit certifies nothing about the current tree.
- **Claiming for the human what you'd never claim for yourself.** The bar is the same whether it's a status update or a merge.
