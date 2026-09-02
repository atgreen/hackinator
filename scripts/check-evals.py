#!/usr/bin/env python3
"""Validate skill eval cases and report coverage.

Every skills/<name>/evals/*.json must have: skills (list), query (str),
expected_behavior (non-empty list). should_not_select (list) is optional.
Selected/should-not-select skills must name real skill directories.

Exit non-zero if any case is malformed. Coverage gaps (skills with no evals)
are reported but do not fail the check.
"""
import json
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


def skill_names():
    return {p.name for p in SKILLS_DIR.iterdir() if (p / "SKILL.md").exists()}


def check_case(path, known):
    errs = []

    def bad(msg):
        errs.append(f"{path}: {msg}")

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        bad(f"invalid JSON ({e})")
        return errs

    skills = data.get("skills")
    if not isinstance(skills, list) or not skills:
        bad("'skills' must be a non-empty list")
    else:
        for s in skills:
            if s not in known:
                bad(f"'skills' names unknown skill '{s}'")

    if not isinstance(data.get("query"), str) or not data.get("query", "").strip():
        bad("'query' must be a non-empty string")

    beh = data.get("expected_behavior")
    if not isinstance(beh, list) or not beh:
        bad("'expected_behavior' must be a non-empty list")

    sns = data.get("should_not_select", [])
    if not isinstance(sns, list):
        bad("'should_not_select' must be a list")
    else:
        for s in sns:
            if s not in known:
                bad(f"'should_not_select' names unknown skill '{s}'")
    return errs


def main():
    known = skill_names()
    cases, errs, covered = 0, [], set()
    for eval_dir in sorted(SKILLS_DIR.glob("*/evals")):
        for case in sorted(eval_dir.glob("*.json")):
            cases += 1
            case_errs = check_case(case, known)
            errs.extend(case_errs)
            if not case_errs:
                covered.update(json.loads(case.read_text()).get("skills", []))

    print(f"Checked {cases} eval case(s) across {len(known)} skills.")
    if errs:
        print(f"\n{len(errs)} error(s):")
        for e in errs:
            print(f"  - {e}")

    gaps = sorted(known - covered)
    if gaps:
        print(f"\nNo evals yet ({len(gaps)}): {', '.join(gaps)}")

    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
