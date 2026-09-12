# Skill evals

Evals are the source of truth for whether a skill routes and behaves as intended. Hackinator
currently has 10 cases covering 10 of its 20 skills; `scripts/check-evals.py` reports the gaps.

Each behavioral run compares two fresh workspaces:

- `baseline`: the agent answers with skill instructions disabled.
- `skills`: the same agent and query run with this repository's skills available.

Repeated pairs expose routing variance. The report preserves the prompt, expected-behavior rubric,
selection results, deterministic grades, requested/observed model identifiers, CLI version, git
revision, tokens, timing, and any cost reported by the harness.

## Where cases live

Put JSON cases under the skill they primarily exercise:

```text
skills/<name>/evals/<case>.json
```

`writing-skills` requires a case whenever a skill is authored or changed. Prefer realistic boundary
prompts where a sibling skill is plausible; easy prompts reveal little about routing quality.

## Case format

```json
{
  "skills": ["builder"],
  "query": "Hack together a scraper that prints page titles.",
  "expected_behavior": [
    "Produces a runnable thin slice",
    "Does not polish code that does not exist yet"
  ],
  "should_not_select": ["whittler", "shaping"],
  "workspace_write": true,
  "graders": [
    {"type": "file_exists", "path": "scraper.py"},
    {"type": "command", "argv": ["python3", "scraper.py"], "expected_exit": 0},
    {"type": "output_contains", "value": "title"},
    {"type": "output_regex", "pattern": "tests? pass"}
  ]
}
```

| Field | Required | Meaning |
|---|---:|---|
| `skills` | yes | Skills the candidate run must select. May be empty for a negative-routing case whose `should_not_select` is non-empty. |
| `query` | yes | The user prompt sent unchanged to both conditions. |
| `expected_behavior` | yes | Human-review rubric included in the report; it is not automatically LLM-judged. |
| `should_not_select` | no | Skills that both conditions must avoid. |
| `workspace_write` | no | Requests a writable Codex sandbox; defaults to `false`. |
| `graders` | no | Deterministic assertions evaluated inside the temporary trial workspace. |

Output checks are case-insensitive. Regular expressions use Python syntax and case-insensitive
matching. File paths must be relative and cannot escape the trial workspace. Command graders take
an argument vector, never a shell string; `expected_exit` defaults to `0` and `timeout` to 60
seconds.

## Validate cases

Schema validation is local, deterministic, and free:

```bash
python3 scripts/check-evals.py
python3 scripts/run_evals.py --list
```

## Run paired evaluations

Both harnesses require an installed, authenticated CLI. Start with one case and one trial:

```bash
python3 scripts/run_evals.py \
  --harness codex \
  --case quick-prototype \
  --trials 1 \
  --output eval-results/quick-prototype-codex.json
```

Use `--harness claude` for Claude Code and `--model` to pin a model. Omitting `--case` runs every
case; the default is three trials. The runner prints the model-turn count before starting:

```text
cases x trials x 2 conditions = model turns
```

Those turns may incur API charges. A full run of the current 10 cases at the default trial count is
60 model turns. Each condition gets a new temporary workspace. Claude runs in `--bare` mode and
loads this repository as a plugin only for the candidate. Codex ignores user config and rules,
disables plugins, disables skill instructions for the baseline, and stages this repository's skills
under the candidate workspace.

Reports default to `eval-results/<UTC timestamp>-<harness>.json`. Raw client events can be large and
may contain incidental environment details, so they are omitted unless `--include-events` is set.
The command exits nonzero for harness errors or failed candidate grades. Baseline behavior graders
are still recorded but do not make the experiment fail—the comparison is their purpose.

Commit deliberately chosen result artifacts when they support a skill change or release. Treat
model, CLI, repository revision, and trial count as part of the result; scores without that context
are not comparable.
