# hackinator

> Skills for hacking in the *original* sense — building for the joy of it, and making the result beautiful.

Not breaking into things. **Making** things. A hack is a clever, playful, well-crafted solution —
the kind that makes another hacker smile. This is a personal, language-agnostic skills library in
the portable `SKILL.md` (Agent Skills) format — it works with
[Claude Code](https://claude.com/claude-code) and [Codex CLI](https://github.com/openai/codex) alike.

## The workflow

For any non-trivial build, **hacking-workflow** is the front door. Say *"let's build X"* or
*"start a hacking session"* and it runs the loop, right-sizing the ceremony to the work:

```
shape → isolate → plan → build → craft → verify → review → finish
```

…with inviolable human-approval gates (what you build, and how it lands) and everything tracked in
beads. The process skills behind it: **shaping** (understand + approve before code), **planning**
(design → tasks → beads), **test-first** (keeper code gets a failing test first; spikes exempt),
**evidence-before-claims** (no "done" without fresh output), **reviewing-work** (fresh reviewer +
receiving feedback well), **finishing** (prove green → human picks merge/PR/keep → clean up).

## Two moods, shared craft

**Personas** are your entry points:

| Persona | Mood | Invoke when |
|---|---|---|
| **builder** | Make it work | Turning an idea into something that runs — prototype, spike, scratch an itch |
| **whittler** | Make it beautiful | Carving working-but-ugly code into its simple, elegant shape (behavior-preserving) |

**Techniques** are neutral and reusable; the personas pull them in, or you invoke them directly:

- **walking-skeleton** — get a thin end-to-end slice running before fleshing out any part
- **spike-and-stabilize** — throwaway probe to retire an unknown, then rebuild for keeps
- **subtraction-first** — try to remove before you add; deletion is the highest-leverage edit
- **naming-as-design** — a name you can't find is a design you haven't made
- **reading-like-prose** — structure code top-down for the human who reads it next
- **dispatching-subagents** — parallelize via subagents to cut wall-clock and keep context clean, while treating the host as a budget (cheap reads wide, heavy builds narrow)
- **using-worktrees** — isolate parallel *edits* so agents don't race, preferring the harness's built-in isolation over hand-rolled `git worktree`
- **using-beads** — track all git-hosted work in `bd` (beads): tasks, deferred TODOs, discovered bugs, and dependencies — always, and frequently
- **consulting-codex** — get an independent second opinion, adversarial gut-check, or outside diff review from the Codex CLI when stuck or the stakes are high

Start at **using-hackinator** — it carries the ethic and routes you to the right skill.

## Install

Each skill is a plain `SKILL.md` with `name`/`description` frontmatter, so any harness that reads
the Agent Skills format can load it. `install.sh` symlinks every skill into the personal skill
trees of both runtimes — symlinks, so edits in this repo take effect immediately:

```
./install.sh              # Claude Code (~/.claude/skills) and Codex (~/.codex/skills)
./install.sh --claude     # just one runtime
./install.sh --codex
./install.sh --uninstall  # remove hackinator's symlinks
```

Claude Code can alternatively install it as a plugin:

```
/plugin marketplace add atgreen/hackinator
/plugin install hackinator@hackinator-dev
```

### Running under Codex (or another harness)

The skills are written harness-neutral and degrade gracefully where runtimes differ:

- **Subagents and worktree isolation** — `dispatching-subagents` and `using-worktrees` prefer the
  harness's native isolation when it exists (Claude Code's `isolation: "worktree"` flag); on a
  runtime without one, the same skills' manual `git worktree` path applies.
- **Second opinions** — `consulting-codex` is symmetric: the point is an *independent* model, not a
  specific CLI. From Claude Code, consult `codex`; from Codex, consult `claude -p`.
- **Beads everywhere** — `bd` is an external CLI, so `using-beads` and the workflow's tracking work
  identically in any harness. Repo-level agent instructions live in both `CLAUDE.md` and `AGENTS.md`.

## The ethic

- Hands-on: you understand a system by building with it.
- Beauty is functional — elegant code is easier to trust and change.
- Subtraction is progress.
- Ship something that runs.
- If it isn't a little bit fun, you're doing it wrong.

## Acknowledgements

hackinator is inspired by two excellent skill libraries, both MIT-licensed:

- [**superpowers**](https://github.com/obra/superpowers) by Jesse Vincent — the disciplined
  development loop (shape → plan → build → verify → review → finish), the test-first and
  evidence-before-claims rigor, and the skill-authoring philosophy.
- **gstack** by Garry Tan — the persona-driven skill model and the idea of a personal,
  opinionated suite that encodes how *you* like to work.

The skills here are original writing that adapts their ideas to a personal, language-agnostic
suite; no text was copied. Gratitude to both projects for showing the way.

## License

MIT © Anthony Green
