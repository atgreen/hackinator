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

try:
    from scripts.run_evals import EvalCase
except ModuleNotFoundError:  # Direct execution puts scripts/ first on sys.path.
    from run_evals import EvalCase

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

    try:
        EvalCase.from_dict(data, source=str(path))
    except ValueError as e:
        errs.append(str(e))
        return errs

    skills = data.get("skills")
    for s in skills:
        if s not in known:
            bad(f"'skills' names unknown skill '{s}'")

    sns = data.get("should_not_select", [])
    for s in sns:
        if s not in known:
            bad(f"'should_not_select' names unknown skill '{s}'")
    allowed = data.get("allowed_skills", [])
    for s in allowed:
        if s not in known:
            bad(f"'allowed_skills' names unknown skill '{s}'")
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
