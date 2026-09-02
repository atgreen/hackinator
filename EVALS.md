# Skill evals

Evals are the **source of truth** for whether a skill works — not the prose in its `SKILL.md`.
Anthropic and LangChain both report that skill *invocation* is unreliable (~70%) and degrades to
**wrong-skill selection** once a suite passes ~20 skills. This suite has 21. So most of our evals
test the boundary: given a realistic prompt, does the *right* skill fire and the sibling stay quiet?

## Where they live

One `evals/` directory per skill, holding one or more `.json` cases:

```
skills/<name>/evals/<case>.json
```

`writing-skills` requires recording a case whenever you author or change a skill (step 4 of
"Write the Failing Case First").

## Case format

```json
{
  "skills": ["shaping"],
  "query": "the prompt a user would actually type",
  "expected_behavior": [
    "an observable thing the agent should do",
    "another observable thing"
  ],
  "should_not_select": ["planning", "builder"]
}
```

| Field | Required | Meaning |
|---|---|---|
| `skills` | yes | The skill(s) that should be selected for `query`. |
| `query` | yes | A realistic user prompt, ideally at a boundary with a sibling. |
| `expected_behavior` | yes | Observable outcomes — selection *and* what the skill should make the agent do. |
| `should_not_select` | no | Sibling skills that must **not** fire. This is the disambiguation assertion. |

Keep queries concrete and language-agnostic. Prefer a boundary case (where a sibling is plausible)
over an easy one — easy cases don't test the description.

## Running them

There is no built-in runner (Anthropic's guidance). Two ways to run:

- **Deterministic check** — `python3 scripts/check-evals.py` validates every case's schema and
  reports which skills still lack evals. Run it before committing skill changes.
- **Behavioral check (manual)** — give a *fresh* agent the `query` with the skill suite loaded and
  watch: did it select `skills`, avoid `should_not_select`, and produce `expected_behavior`? Compare
  against a baseline run with no skills loaded. Automating this with an LLM judge is a future bead.
