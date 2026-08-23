---
name: planning
description: Use after a design is approved and before implementing anything architectural — turning an agreed direction into an ordered, testable set of tasks. "write a plan", "break this down", "what are the steps", "plan the implementation"
---

# Planning

## Overview

**Core principle:** Write the plan for someone with **zero context, questionable taste, and no
instinct to test** — because that someone is a fresh subagent, or you after compaction, or you at
2am. Everything the implementer needs is *in the plan*; nothing lives only in your head or the chat.

A good plan turns a design into a sequence of tasks that each end in something you can *run and
check*. It is the bridge between **shaping** (what & why) and the build (how).

## Map the Structure First

Before tasks, lay out the pieces: what files/modules exist, each with **one responsibility**. A
clear structure makes the tasks fall out naturally. If you can't name a piece cleanly, the design
isn't settled — go back to **shaping** (and see **naming-as-design**).

## Right-Size the Tasks

- A task is the **smallest chunk worth a reviewer's gate** — it ends in an independently testable,
  runnable deliverable. Not "build the parser" (too big); not "add a semicolon" (too small).
- Inside a task, steps are **bite-sized** (a couple of minutes each), test-first where it's keeper code.
- Each task names its **interfaces**: what it consumes and what it produces, with the *actual*
  signatures — not "a function that parses input" but the real name, args, and return shape.

## No Placeholders

```
IF THE PLAN SAYS "TBD" OR "SIMILAR TO ABOVE", IT ISN'T A PLAN YET
```

Ban "add error handling", "etc.", "TBD", "like task 2". Write the real thing. A placeholder is a
decision you're pushing onto someone with less context than you have right now. Repeat real code
rather than referencing it vaguely.

## File It As Beads

The plan is not a document that rots in a folder — it's **beads** (**using-beads**):

```bash
bd create "Parser: tokenize input" -t task -p 1
bd create "Parser: build AST"      -t task -p 1 --deps blocked-by:<tokenize-id>
```

Record dependencies so `bd ready` surfaces exactly what's buildable next. This is what lets a
fan-out of implementers (**dispatching-subagents**) each claim ready work without colliding. For a
larger effort, also keep a short plan note in the repo; for most work, the beads *are* the plan.

## Self-Review Before Handing Off

Check the plan against the approved design:
- **Coverage** — every part of the design maps to a task; nothing designed is unplanned.
- **No placeholders** — every task is concrete enough to implement blind.
- **Interfaces line up** — what one task produces is what the next consumes, names and shapes matching.

Then pick the execution mode: fan out fresh implementers per ready task (**dispatching-subagents**,
default for independent tasks) or work them inline.

## Common Mistakes

- **Tasks too big to review.** If a task can't be checked in one sitting, split it.
- **Vague interfaces.** "Passes the data along" hides the exact mismatch that will bite in integration. Write signatures.
- **Planning what won't be built.** YAGNI applies here too — don't plan the speculative feature shaping already cut.
- **A plan nobody can act on without you.** If the implementer would have to ask you a question, answer it *in the plan* first.
