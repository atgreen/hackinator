---
name: walking-skeleton
description: Use when starting anything new and unsure where to begin, tempted to build the interesting component first, or when a prototype has many parts that don't yet connect end to end. Not for a throwaway probe to answer an unknown you'll then delete — that's spike-and-stabilize
---

# Walking Skeleton

## Overview

**Core principle:** Get the thinnest possible slice running end to end *first* — input to visible
output, all the way through — before you flesh out any single part.

A walking skeleton is a system that does almost nothing but does it *completely*: every layer is
present, wired together, and runs, even if each layer is a stub returning a hard-coded value. It
walks. Then you grow muscle onto a skeleton that already stands, instead of assembling a pile of
perfect bones that have never held weight together.

## Why It Wins

The risk in anything new is rarely a single component — it's the **connections**: the layers that
must talk, the assumptions that don't survive contact, the "obvious" integration that isn't. A
walking skeleton pays down that risk on day one. A pile of polished-but-unconnected parts defers it
to the worst possible moment: the end.

## The Recipe

1. **Trace the thinnest line** from a real input to a visible output. List every layer it must
   pass through. Keep the line as short as you can while still touching every layer.
2. **Stub every layer to the minimum that lets the line run.** Hard-code returns. Fake the data.
   Print instead of persist. The goal is a pulse, not a feature.
3. **Wire it together and run it.** Watch the input travel all the way to output. This is the
   moment that matters — the system *walks*.
4. **Only now, grow one layer at a time.** Replace a stub with the real thing, run again, confirm
   it still walks. Repeat. The skeleton stays alive through every step.

## Quick Reference

| Do | Don't |
|---|---|
| Touch every layer, shallowly | Perfect one layer, deeply |
| Hard-code, stub, fake — to get a pulse | Build real data models up front |
| Run end to end before anything is "real" | Wait until parts are done to connect them |
| Grow one stub into real code at a time | Replace many stubs in one leap |

## Signs You Skipped This

- You have three "done" components and nothing runs.
- You're deep in the interesting module and haven't proven the boring integration works.
- The first end-to-end run is scheduled for "once the pieces are ready" — i.e., never, until crunch.
- You can describe how it *will* work but can't show it doing anything.

**Any of these: stop adding. Wire what exists into a slice that runs, however fake.**

## Relationship to Other Skills

The **builder** persona starts here by default. When a layer hides a genuine unknown ("can this
even be done?"), retire it with **spike-and-stabilize** before growing it for real.
