#!/usr/bin/env python3
"""Run Hackinator skill evaluations against supported coding-agent CLIs."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, Callable, Iterable


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    source: str
    skills: tuple[str, ...]
    query: str
    expected_behavior: tuple[str, ...]
    should_not_select: tuple[str, ...] = ()
    allowed_skills: tuple[str, ...] | None = None
    graders: tuple[dict[str, Any], ...] = ()
    workspace_write: bool = False

    @classmethod
    def from_dict(cls, data: Any, *, source: str) -> "EvalCase":
        if not isinstance(data, dict):
            raise ValueError(f"{source}: case must be a JSON object")
        skills = _strings(data.get("skills"), "skills", source)
        query = data.get("query")
        if not isinstance(query, str) or not query.strip():
            raise ValueError(f"{source}: query must be a non-empty string")
        expected = _nonempty_strings(
            data.get("expected_behavior"), "expected_behavior", source
        )
        excluded = _strings(data.get("should_not_select", []), "should_not_select", source)
        if not skills and not excluded:
            raise ValueError(
                f"{source}: skills or should_not_select must name at least one skill"
            )
        allowed = None
        if "allowed_skills" in data:
            allowed = _strings(data["allowed_skills"], "allowed_skills", source)
            missing_allowed = sorted(set(skills) - set(allowed))
            if missing_allowed:
                raise ValueError(
                    f"{source}: allowed_skills must include required skills: "
                    f"{', '.join(missing_allowed)}"
                )
            contradictory = sorted(set(allowed) & set(excluded))
            if contradictory:
                raise ValueError(
                    f"{source}: skills cannot be both allowed and forbidden: "
                    f"{', '.join(contradictory)}"
                )
        graders = data.get("graders", [])
        if not isinstance(graders, list) or not all(isinstance(item, dict) for item in graders):
            raise ValueError(f"{source}: graders must be a list of objects")
        for index, grader in enumerate(graders, 1):
            _validate_grader(grader, source, index)
        workspace_write = data.get("workspace_write", False)
        if not isinstance(workspace_write, bool):
            raise ValueError(f"{source}: workspace_write must be a boolean")

        return cls(
            case_id=Path(source).stem,
            source=source,
            skills=tuple(skills),
            query=query.strip(),
            expected_behavior=tuple(expected),
            should_not_select=tuple(excluded),
            allowed_skills=tuple(allowed) if allowed is not None else None,
            graders=tuple(graders),
            workspace_write=workspace_write,
        )


@dataclass(frozen=True)
class AgentResult:
    selected_skills: tuple[str, ...] = ()
    output: str = ""
    model: str | None = None
    input_tokens: int = 0
    cached_input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float | None = None
    duration_ms: int | None = None
    error: str | None = None
    events: tuple[dict[str, Any], ...] = ()


@dataclass(frozen=True)
class Grade:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class TrialRecord:
    case_id: str
    condition: str
    trial: int
    result: AgentResult
    grades: tuple[Grade, ...] = ()


class ClaudeHarness:
    name = "claude"

    def prepare_workspace(
        self, condition: str, workspace: Path, repo_root: Path
    ) -> None:
        _validate_condition(condition)

    def command(
        self,
        case: EvalCase,
        condition: str,
        workspace: Path,
        repo_root: Path,
        *,
        model: str | None = None,
    ) -> list[str]:
        _validate_condition(condition)
        command = [
            "claude",
            "-p",
            "--bare",
            "--output-format",
            "stream-json",
            "--verbose",
            "--no-session-persistence",
            "--permission-mode",
            "dontAsk",
        ]
        if condition == "baseline":
            command.append("--disable-slash-commands")
        else:
            command.extend(("--plugin-dir", str(repo_root)))
        if model:
            command.extend(("--model", model))
        command.append(case.query)
        return command

    def parse(self, stream: str) -> AgentResult:
        return parse_claude_events(stream)

    def environment(self, workspace: Path) -> dict[str, str]:
        return os.environ.copy()


class CodexHarness:
    name = "codex"

    def __init__(
        self,
        *,
        auth_source: Path | None = None,
        external_skill_paths: Iterable[Path] | None = None,
    ) -> None:
        configured_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        self.auth_source = auth_source or configured_home / "auth.json"
        self.external_skill_paths = tuple(
            external_skill_paths
            if external_skill_paths is not None
            else _discover_external_skill_paths()
        )

    def prepare_workspace(
        self, condition: str, workspace: Path, repo_root: Path
    ) -> None:
        _validate_condition(condition)
        isolated_home = workspace / ".codex-home"
        isolated_home.mkdir()
        if self.auth_source.is_file():
            (isolated_home / "auth.json").symlink_to(self.auth_source.resolve())
        if condition == "skills":
            shutil.copytree(repo_root / "skills", workspace / ".agents/skills")

    def command(
        self,
        case: EvalCase,
        condition: str,
        workspace: Path,
        repo_root: Path,
        *,
        model: str | None = None,
    ) -> list[str]:
        _validate_condition(condition)
        command = [
            "codex",
            "exec",
            "--ephemeral",
            "--json",
            "--skip-git-repo-check",
            "--ignore-user-config",
            "--ignore-rules",
            "--disable",
            "plugins",
            "--sandbox",
            "workspace-write" if case.workspace_write else "read-only",
            "--cd",
            str(workspace),
        ]
        if self.external_skill_paths:
            entries = ", ".join(
                f"{{ path = {json.dumps(str(path))}, enabled = false }}"
                for path in self.external_skill_paths
            )
            command.extend(("--config", f"skills.config=[{entries}]"))
        if condition == "baseline":
            command.extend(("--config", "skills.include_instructions=false"))
        if model:
            command.extend(("--model", model))
        command.append(case.query)
        return command

    def parse(self, stream: str) -> AgentResult:
        return parse_codex_events(stream)

    def environment(self, workspace: Path) -> dict[str, str]:
        environment = os.environ.copy()
        environment["CODEX_HOME"] = str(workspace / ".codex-home")
        return environment


Harness = ClaudeHarness | CodexHarness
RunCommand = Callable[..., subprocess.CompletedProcess[str]]


def load_eval_cases(
    skills_root: Path, *, case_ids: set[str] | None = None
) -> list[EvalCase]:
    cases = []
    seen_ids: set[str] = set()
    for path in sorted(skills_root.glob("*/evals/*.json")):
        with path.open(encoding="utf-8") as source_file:
            data = json.load(source_file)
        case = EvalCase.from_dict(data, source=str(path))
        if case.case_id in seen_ids:
            raise ValueError(f"duplicate evaluation case id: {case.case_id}")
        seen_ids.add(case.case_id)
        if case_ids is None or case.case_id in case_ids:
            cases.append(case)

    if case_ids is not None:
        missing = case_ids - seen_ids
        if missing:
            raise ValueError(f"unknown evaluation case ids: {', '.join(sorted(missing))}")
    return cases


def run_paired_trials(
    cases: Iterable[EvalCase],
    harness: Harness,
    *,
    repo_root: Path,
    trials: int,
    timeout: int,
    model: str | None = None,
    run_command: RunCommand = subprocess.run,
) -> list[TrialRecord]:
    if trials < 1:
        raise ValueError("trials must be at least 1")
    if timeout < 1:
        raise ValueError("timeout must be at least 1 second")

    records = []
    for case in cases:
        for trial in range(1, trials + 1):
            for condition in ("baseline", "skills"):
                with tempfile.TemporaryDirectory(prefix="hackinator-eval-") as directory:
                    workspace = Path(directory)
                    harness.prepare_workspace(condition, workspace, repo_root)
                    command = harness.command(
                        case,
                        condition,
                        workspace,
                        repo_root,
                        model=model,
                    )
                    result = _run_trial(
                        command,
                        workspace,
                        harness,
                        timeout=timeout,
                        model=model,
                        run_command=run_command,
                    )
                    grades = grade_trial(
                        case,
                        condition,
                        result,
                        workspace,
                        run_command=run_command,
                    )
                records.append(
                    TrialRecord(
                        case_id=case.case_id,
                        condition=condition,
                        trial=trial,
                        result=result,
                        grades=grades,
                    )
                )
    return records


def grade_trial(
    case: EvalCase,
    condition: str,
    result: AgentResult,
    workspace: Path,
    *,
    run_command: RunCommand = subprocess.run,
) -> tuple[Grade, ...]:
    _validate_condition(condition)
    grades = [
        Grade(
            "agent_success",
            result.error is None,
            result.error or "agent completed without a harness error",
        )
    ]
    selected = set(result.selected_skills)
    if condition == "skills" and case.skills:
        missing = sorted(set(case.skills) - selected)
        grades.append(
            Grade(
                "expected_skills",
                not missing,
                "all expected skills selected"
                if not missing
                else f"missing expected skills: {', '.join(missing)}",
            )
        )
    if case.should_not_select:
        unexpected = sorted(set(case.should_not_select) & selected)
        grades.append(
            Grade(
                "excluded_skills",
                not unexpected,
                "no excluded skills selected"
                if not unexpected
                else f"selected excluded skills: {', '.join(unexpected)}",
            )
        )
    if condition == "skills" and case.allowed_skills is not None:
        unexpected = sorted(selected - set(case.allowed_skills))
        grades.append(
            Grade(
                "unexpected_skills",
                not unexpected,
                "all selected skills are allowed"
                if not unexpected
                else f"unexpected skills selected: {', '.join(unexpected)}",
            )
        )

    for index, grader in enumerate(case.graders, 1):
        grades.append(
            _run_grader(
                grader,
                index,
                result,
                workspace,
                run_command=run_command,
            )
        )
    return tuple(grades)


def build_report(
    cases: Iterable[EvalCase],
    records: Iterable[TrialRecord],
    *,
    harness_name: str,
    harness_version: str | None,
    requested_model: str | None = None,
    git_metadata: dict[str, Any],
    generated_at: str | None = None,
    include_events: bool = False,
) -> dict[str, Any]:
    case_list = list(cases)
    record_list = list(records)
    generated_at = generated_at or datetime.now(timezone.utc).isoformat().replace(
        "+00:00", "Z"
    )
    models = sorted(
        {record.result.model for record in record_list if record.result.model}
    )
    return {
        "schema_version": 1,
        "generated_at": generated_at,
        "harness": {
            "name": harness_name,
            "version": harness_version,
            "requested_model": requested_model,
            "observed_models": models,
        },
        "git": git_metadata,
        "cases": [
            {
                "id": case.case_id,
                "source": case.source,
                "skills": list(case.skills),
                "query": case.query,
                "expected_behavior": list(case.expected_behavior),
                "should_not_select": list(case.should_not_select),
                "allowed_skills": (
                    list(case.allowed_skills)
                    if case.allowed_skills is not None
                    else None
                ),
                "graders": list(case.graders),
                "workspace_write": case.workspace_write,
            }
            for case in case_list
        ],
        "summary": _summarize(record_list),
        "trials": [
            _record_as_dict(record, include_events=include_events)
            for record in record_list
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run paired baseline-vs-Hackinator skill evaluations."
    )
    parser.add_argument("--harness", choices=("codex", "claude"), default="codex")
    parser.add_argument("--case", action="append", dest="case_ids", metavar="ID")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=300, metavar="SECONDS")
    parser.add_argument("--model")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--include-events", action="store_true")
    parser.add_argument("--list", action="store_true", dest="list_cases")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args(argv)

    try:
        cases = load_eval_cases(
            args.repo_root / "skills",
            case_ids=set(args.case_ids) if args.case_ids else None,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if not cases:
        print("error: no evaluation cases found", file=sys.stderr)
        return 2
    if args.list_cases:
        for case in cases:
            print(f"{case.case_id}\t{', '.join(case.skills)}")
        return 0
    if args.trials < 1 or args.timeout < 1:
        print("error: --trials and --timeout must be positive", file=sys.stderr)
        return 2

    harness: Harness = CodexHarness() if args.harness == "codex" else ClaudeHarness()
    turn_count = len(cases) * args.trials * 2
    print(
        f"Running {len(cases)} case(s) x {args.trials} trial(s) x "
        f"2 conditions = {turn_count} model turns."
    )
    records = run_paired_trials(
        cases,
        harness,
        repo_root=args.repo_root,
        trials=args.trials,
        timeout=args.timeout,
        model=args.model,
    )
    report = build_report(
        cases,
        records,
        harness_name=harness.name,
        harness_version=_command_version(harness.name),
        requested_model=args.model,
        git_metadata=_git_metadata(args.repo_root),
        include_events=args.include_events,
    )
    output_path = args.output or _default_report_path(args.repo_root, harness.name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")

    failed = any(record.result.error for record in records) or any(
        not grade.passed
        for record in records
        if record.condition == "skills"
        for grade in record.grades
    )
    return 1 if failed else 0


def _command_version(command: str) -> str | None:
    try:
        completed = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    version = completed.stdout.strip() or completed.stderr.strip()
    return version or None


def _git_metadata(repo_root: Path) -> dict[str, Any]:
    def git(*arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(repo_root), *arguments],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

    try:
        revision = git("rev-parse", "HEAD")
        status = git("status", "--porcelain")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return {"commit": None, "dirty": None}
    return {
        "commit": revision.stdout.strip() if revision.returncode == 0 else None,
        "dirty": bool(status.stdout.strip()) if status.returncode == 0 else None,
    }


def _default_report_path(repo_root: Path, harness_name: str) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return repo_root / "eval-results" / f"{timestamp}-{harness_name}.json"


def _run_trial(
    command: list[str],
    workspace: Path,
    harness: Harness,
    *,
    timeout: int,
    model: str | None,
    run_command: RunCommand,
) -> AgentResult:
    started = time.monotonic()
    try:
        completed = run_command(
            command,
            cwd=workspace,
            env=harness.environment(workspace),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        return AgentResult(
            model=model,
            duration_ms=round((time.monotonic() - started) * 1000),
            error=str(error),
        )

    result = harness.parse(completed.stdout)
    elapsed_ms = round((time.monotonic() - started) * 1000)
    errors = [result.error]
    if completed.returncode:
        detail = completed.stderr.strip() or f"process exited {completed.returncode}"
        errors.append(detail)
    return replace(
        result,
        model=result.model or model,
        duration_ms=result.duration_ms if result.duration_ms is not None else elapsed_ms,
        error="; ".join(error for error in errors if error) or None,
    )


def _run_grader(
    grader: dict[str, Any],
    index: int,
    result: AgentResult,
    workspace: Path,
    *,
    run_command: RunCommand,
) -> Grade:
    grader_type = grader["type"]
    name = f"grader_{index}:{grader_type}"
    if grader_type == "output_contains":
        value = grader["value"]
        passed = value.casefold() in result.output.casefold()
        verb = "contains" if passed else "does not contain"
        return Grade(name, passed, f"output {verb} {value!r}")
    if grader_type == "output_regex":
        pattern = grader["pattern"]
        passed = re.search(pattern, result.output, re.IGNORECASE) is not None
        verb = "matches" if passed else "does not match"
        return Grade(name, passed, f"output {verb} /{pattern}/")
    if grader_type == "file_exists":
        path = workspace / grader["path"]
        passed = path.exists()
        verb = "exists" if passed else "does not exist"
        return Grade(name, passed, f"{grader['path']} {verb}")

    expected_exit = grader.get("expected_exit", 0)
    try:
        completed = run_command(
            list(grader["argv"]),
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=grader.get("timeout", 60),
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        return Grade(name, False, str(error))
    passed = completed.returncode == expected_exit
    detail = f"command exited {completed.returncode}; expected {expected_exit}"
    if not passed and completed.stderr.strip():
        detail += f": {completed.stderr.strip()}"
    return Grade(name, passed, detail)


def _summarize(records: list[TrialRecord]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for condition in ("baseline", "skills"):
        selected = [record for record in records if record.condition == condition]
        grades: dict[str, dict[str, int]] = {}
        for record in selected:
            for grade in record.grades:
                tally = grades.setdefault(grade.name, {"passed": 0, "total": 0})
                tally["total"] += 1
                tally["passed"] += int(grade.passed)
        costs = [
            record.result.cost_usd
            for record in selected
            if record.result.cost_usd is not None
        ]
        skill_selections = sum(
            len(record.result.selected_skills) for record in selected
        )
        unexpected_runs = sum(
            any(
                grade.name == "unexpected_skills" and not grade.passed
                for grade in record.grades
            )
            for record in selected
        )
        summary[condition] = {
            "runs": len(selected),
            "errors": sum(record.result.error is not None for record in selected),
            "input_tokens": sum(record.result.input_tokens for record in selected),
            "cached_input_tokens": sum(record.result.cached_input_tokens for record in selected),
            "output_tokens": sum(record.result.output_tokens for record in selected),
            "cost_usd": round(sum(costs), 8) if costs else None,
            "duration_ms": sum(record.result.duration_ms or 0 for record in selected),
            "selection": {
                "total": skill_selections,
                "mean_per_run": round(skill_selections / len(selected), 3)
                if selected
                else 0.0,
                "multi_skill_runs": sum(
                    len(record.result.selected_skills) > 1 for record in selected
                ),
                "unexpected_runs": unexpected_runs,
            },
            "grades": grades,
        }
    return summary


def _record_as_dict(record: TrialRecord, *, include_events: bool) -> dict[str, Any]:
    result = asdict(record.result)
    result["selected_skills"] = list(record.result.selected_skills)
    if not include_events:
        result.pop("events")
    return {
        "case_id": record.case_id,
        "condition": record.condition,
        "trial": record.trial,
        "result": result,
        "grades": [asdict(grade) for grade in record.grades],
    }


def parse_claude_events(stream: str) -> AgentResult:
    events, parse_errors = _parse_jsonl(stream)
    selected: list[str] = []
    output = ""
    model = None
    usage: dict[str, Any] = {}
    cost = None
    duration = None
    result_error = None

    for event in events:
        if event.get("type") == "assistant":
            message = event.get("message", {})
            for block in message.get("content", []):
                if block.get("type") == "tool_use" and block.get("name") == "Skill":
                    skill = block.get("input", {}).get("skill")
                    if isinstance(skill, str):
                        selected.append(_unqualify_skill(skill))
        if event.get("type") == "result":
            output = str(event.get("result", output))
            usage = event.get("usage") or usage
            cost = event.get("total_cost_usd")
            duration = event.get("duration_ms")
            model_usage = event.get("modelUsage", {})
            if model_usage:
                model = next(iter(model_usage))
            if event.get("subtype") not in (None, "success"):
                result_error = output or str(event.get("subtype"))

    error = "; ".join((*parse_errors, *((result_error,) if result_error else ()))) or None
    return AgentResult(
        selected_skills=_deduplicate(selected),
        output=output,
        model=model,
        input_tokens=_integer(usage.get("input_tokens")),
        cached_input_tokens=_integer(usage.get("cache_read_input_tokens")),
        output_tokens=_integer(usage.get("output_tokens")),
        cost_usd=float(cost) if isinstance(cost, (int, float)) else None,
        duration_ms=_optional_integer(duration),
        error=error,
        events=tuple(events),
    )


_SKILL_PATH = re.compile(
    r"(?:^|[\\/])skills[\\/](?P<name>[a-z0-9][a-z0-9-]*)[\\/]SKILL\.md"
)


def parse_codex_events(stream: str) -> AgentResult:
    events, parse_errors = _parse_jsonl(stream)
    selected: list[str] = []
    output = ""
    usage: dict[str, Any] = {}
    result_error = None

    for event in events:
        event_type = event.get("type")
        item = event.get("item", {})
        if event_type in ("item.started", "item.completed"):
            if item.get("type") == "command_execution":
                for match in _SKILL_PATH.finditer(str(item.get("command", ""))):
                    selected.append(match.group("name"))
            elif event_type == "item.completed" and item.get("type") == "agent_message":
                output = str(item.get("text", output))
        elif event_type == "turn.completed":
            usage = event.get("usage") or usage
        elif event_type in ("turn.failed", "error"):
            result_error = str(event.get("error") or event.get("message") or event_type)

    error = "; ".join((*parse_errors, *((result_error,) if result_error else ()))) or None
    return AgentResult(
        selected_skills=_deduplicate(selected),
        output=output,
        input_tokens=_integer(usage.get("input_tokens")),
        cached_input_tokens=_integer(usage.get("cached_input_tokens")),
        output_tokens=_integer(usage.get("output_tokens")),
        error=error,
        events=tuple(events),
    )


def _parse_jsonl(stream: str) -> tuple[list[dict[str, Any]], list[str]]:
    events = []
    errors = []
    for line_number, line in enumerate(stream.splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"malformed JSONL at line {line_number}")
            continue
        if isinstance(event, dict):
            events.append(event)
        else:
            errors.append(f"non-object JSONL at line {line_number}")
    return events, errors


def _unqualify_skill(name: str) -> str:
    return name.rsplit(":", 1)[-1]


def _deduplicate(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def _strings(value: Any, field: str, source: str) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise ValueError(f"{source}: {field} must be a list of non-empty strings")
    return [item.strip() for item in value]


def _nonempty_strings(value: Any, field: str, source: str) -> list[str]:
    result = _strings(value, field, source)
    if not result:
        raise ValueError(f"{source}: {field} must not be empty")
    return result


def _integer(value: Any) -> int:
    return int(value) if isinstance(value, (int, float)) else 0


def _optional_integer(value: Any) -> int | None:
    return int(value) if isinstance(value, (int, float)) else None


def _validate_condition(condition: str) -> None:
    if condition not in ("baseline", "skills"):
        raise ValueError(f"unknown evaluation condition: {condition}")


def _validate_grader(grader: dict[str, Any], source: str, index: int) -> None:
    prefix = f"{source}: graders[{index - 1}]"
    grader_type = grader.get("type")
    if grader_type not in ("output_contains", "output_regex", "file_exists", "command"):
        raise ValueError(f"{prefix}: unknown grader type {grader_type!r}")
    if grader_type == "output_contains":
        if not isinstance(grader.get("value"), str) or not grader["value"]:
            raise ValueError(f"{prefix}: value must be a non-empty string")
    elif grader_type == "output_regex":
        pattern = grader.get("pattern")
        if not isinstance(pattern, str) or not pattern:
            raise ValueError(f"{prefix}: pattern must be a non-empty string")
        try:
            re.compile(pattern)
        except re.error as error:
            raise ValueError(f"{prefix}: invalid pattern ({error})") from error
    elif grader_type == "file_exists":
        path = grader.get("path")
        if not isinstance(path, str) or not _is_safe_relative_path(path):
            raise ValueError(f"{prefix}: path must stay within the trial workspace")
    else:
        argv = grader.get("argv")
        if not isinstance(argv, list) or not argv or not all(
            isinstance(item, str) and item for item in argv
        ):
            raise ValueError(f"{prefix}: argv must be a non-empty list of strings")
        expected_exit = grader.get("expected_exit", 0)
        if not isinstance(expected_exit, int):
            raise ValueError(f"{prefix}: expected_exit must be an integer")
        timeout = grader.get("timeout", 60)
        if not isinstance(timeout, int) or timeout < 1:
            raise ValueError(f"{prefix}: timeout must be a positive integer")


def _is_safe_relative_path(value: str) -> bool:
    path = Path(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts


def _discover_external_skill_paths() -> tuple[Path, ...]:
    roots = (Path.home() / ".agents/skills", Path("/etc/codex/skills"))
    return tuple(
        sorted(path for root in roots for path in root.glob("*/SKILL.md"))
    )


if __name__ == "__main__":
    sys.exit(main())
