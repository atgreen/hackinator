# hackinator

Personal skills for **hacking in the original sense** — building for the joy of it and making the
result beautiful. Not security; craft. A hack is a clever, playful, well-made solution.

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

- **Descriptions = capability clause + triggers + exclusion clause** — name what the skill does, then
  "Use when…" symptoms/phrases, then "Not for X — that's **sibling**" when a near-neighbour exists
  (with ~20 skills, the wrong one gets picked without it). **Never summarize the workflow** (agents
  follow the description instead of reading the skill).
- **Active, verb-first names** (`subtraction-first`, not `code-reduction`).
- **Personas cross-reference techniques** via `**REQUIRED SUB-SKILL:** Use **name**` markers —
  never `@`-link (it force-loads and burns context).
- Prefer tables, guard-clause examples, and a "Common Mistakes" section. Keep it tight.
- Language-agnostic by default; use one good example, not five languages.


<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:1105d646 -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/core-concepts/sync-concepts.md for details and anti-patterns.

## Agent Context Profiles

The managed Beads block is task-tracking guidance, not permission to override repository, user, or orchestrator instructions.

- **Conservative (default)**: Use `bd` for task tracking. Do not run git commits, git pushes, or Dolt remote sync unless explicitly asked. At handoff, report changed files, validation, and suggested next commands.
- **Minimal**: Keep tool instruction files as pointers to `bd prime`; use the same conservative git policy unless active instructions say otherwise.
- **Team-maintainer**: Only when the repository explicitly opts in, agents may close beads, run quality gates, commit, and push as part of session close. A current "do not commit" or "do not push" instruction still wins.

## Session Completion

This protocol applies when ending a Beads implementation workflow. It is subordinate to explicit user, repository, and orchestrator instructions.

1. **File issues for remaining work** - Create beads for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **Handle git/sync by active profile**:
   ```bash
   # Conservative/minimal/default: report status and proposed commands; wait for approval.
   git status

   # Team-maintainer opt-in only, unless current instructions forbid it:
   git pull --rebase
   git push
   git status
   ```
5. **Hand off** - Summarize changes, validation, issue status, and any blocked sync/commit/push step

**Critical rules:**
- Explicit user or orchestrator instructions override this Beads block.
- Do not commit or push without clear authority from the active profile or the current user request.
- If a required sync or push is blocked, stop and report the exact command and error.
<!-- END BEADS INTEGRATION -->
