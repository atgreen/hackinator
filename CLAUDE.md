# hackinator

Personal skills for **hacking in the original sense** — building for the joy of it and making the
result beautiful. Not security; craft. A hack is a clever, playful, well-made solution that makes
another hacker smile.

## The workflow

For any non-trivial build, **hacking-workflow** is the front door — it runs the loop
`shape → isolate → plan → build → craft → verify → review → finish` with inviolable human-approval
gates, tracked in beads throughout. Process skills: `shaping`, `planning`, `test-first`,
`evidence-before-claims`, `reviewing-work`, `finishing`.

## The two moods

- **builder** — make an idea real, fast. Bias toward a running artifact over a finished argument.
- **whittler** — take working code and carve away everything that isn't the shape. Behavior-preserving craft.

Both lean on shared **techniques**: `walking-skeleton`, `spike-and-stabilize`, `subtraction-first`,
`naming-as-design`, `reading-like-prose`, `dispatching-subagents` (parallelize without overwhelming
the host), `using-worktrees` (isolate parallel edits), `using-beads` (track the work), and
`consulting-codex` (second opinion). Start at **using-hackinator** to route.

## Standing rules

- **Beads, always.** In any git-hosted activity, track work in `bd` — continuously, not at the end.
  Deferred TODOs, discovered bugs, and follow-ups are beads, not code comments or mental notes. See **using-beads**.
- **Ask a peer when it's hard.** Stuck or high-stakes? Consult an independent model via **consulting-codex**, then judge its answer.
- **Mind the host.** Parallelize via subagents, but treat host resources as a budget. See **dispatching-subagents**.

## Layout

```
skills/
  using-hackinator/   # ethos + router (entry point)
  hacking-workflow/   # the front-door loop: shape→…→finish, with gates
  shaping/            # process: understand + approval gate before code
  planning/           # process: design → right-sized tasks, filed as beads
  test-first/         # process: keeper code gets a failing test first (spikes exempt)
  evidence-before-claims/ # process: no "done" without fresh verification output
  reviewing-work/     # process: fresh reviewer subagent + receiving feedback well
  finishing/          # process: prove green → human picks how it lands → clean up
  builder/            # persona: make it work
  whittler/           # persona: make it beautiful
  walking-skeleton/   # technique
  spike-and-stabilize/# technique
  subtraction-first/  # technique
  naming-as-design/   # technique
  reading-like-prose/ # technique
  dispatching-subagents/ # technique: parallelize via subagents within a host budget
  using-worktrees/    # technique: isolate parallel edits so agents don't race
  using-beads/        # technique: track all git-hosted work in bd (always-on)
  consulting-codex/   # technique: second opinion / adversarial check from Codex
  writing-skills/     # meta: how to author skills in this suite
```

Flat namespace, one `SKILL.md` per skill.

## Authoring conventions

When adding or editing a skill, use the **writing-skills** skill. In short:

- **Descriptions state triggers only** — start with "Use when…", list symptoms and phrases, and
  **never summarize the workflow** (agents follow the description instead of reading the skill).
- **Active, verb-first names** (`subtraction-first`, not `code-reduction`).
- **Personas cross-reference techniques** via `**REQUIRED SUB-SKILL:** Use **name**` markers —
  never `@`-link (it force-loads and burns context).
- Prefer tables, guard-clause examples, and a "Common Mistakes" section. Keep it tight.
- Language-agnostic by default; use one good example, not five languages.
