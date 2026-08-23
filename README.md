# hackinator

> Skills for hacking in the *original* sense — building for the joy of it, and making the result beautiful.

Not breaking into things. **Making** things. A hack is a clever, playful, well-crafted solution —
the kind that makes another hacker smile. This is a personal, language-agnostic skills library for
[Claude Code](https://claude.com/claude-code).

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

Once pushed to GitHub:

```
/plugin marketplace add atgreen/hackinator
/plugin install hackinator@hackinator-dev
```

Or drop the contents of `skills/` into `~/.claude/skills/` for a purely personal setup.

## The ethic

- Hands-on: you understand a system by building with it.
- Beauty is functional — elegant code is easier to trust and change.
- Subtraction is progress.
- Ship something that runs.
- If it isn't a little bit fun, you're doing it wrong.

## License

MIT © Anthony Green
