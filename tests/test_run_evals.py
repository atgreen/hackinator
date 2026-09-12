import json
import io
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts.run_evals import (
    AgentResult,
    ClaudeHarness,
    CodexHarness,
    EvalCase,
    TrialRecord,
    build_report,
    grade_trial,
    load_eval_cases,
    main,
    parse_claude_events,
    parse_codex_events,
    run_paired_trials,
)


_CHECK_EVALS_SPEC = importlib.util.spec_from_file_location(
    "check_evals", Path(__file__).parents[1] / "scripts/check-evals.py"
)
check_evals = importlib.util.module_from_spec(_CHECK_EVALS_SPEC)
assert _CHECK_EVALS_SPEC.loader is not None
_CHECK_EVALS_SPEC.loader.exec_module(check_evals)


class EvalCaseTests(unittest.TestCase):
    def test_case_rejects_non_object_json(self):
        with self.assertRaisesRegex(ValueError, "JSON object"):
            EvalCase.from_dict([], source="broken.json")

    def test_existing_case_shape_remains_valid(self):
        case = EvalCase.from_dict(
            {
                "skills": ["builder"],
                "query": "Build the smallest runnable thing.",
                "expected_behavior": ["Produces a runnable artifact"],
                "should_not_select": ["whittler"],
            },
            source="builder.json",
        )

        self.assertEqual(case.case_id, "builder")
        self.assertEqual(case.skills, ("builder",))
        self.assertEqual(case.should_not_select, ("whittler",))
        self.assertEqual(case.graders, ())
        self.assertFalse(case.workspace_write)

    def test_case_rejects_missing_expected_behavior(self):
        with self.assertRaisesRegex(ValueError, "expected_behavior"):
            EvalCase.from_dict(
                {"skills": ["builder"], "query": "Build it."},
                source="builder.json",
            )

    def test_case_accepts_deterministic_graders_and_workspace_write(self):
        case = EvalCase.from_dict(
            {
                **_case_dict("builder"),
                "workspace_write": True,
                "graders": [{"type": "file_exists", "path": "result.txt"}],
            },
            source="builder.json",
        )

        self.assertTrue(case.workspace_write)
        self.assertEqual(case.graders[0]["type"], "file_exists")

    def test_case_accepts_allowlist_that_contains_required_skills(self):
        case = EvalCase.from_dict(
            {
                **_case_dict("builder"),
                "allowed_skills": ["builder", "evidence-before-claims"],
            },
            source="builder.json",
        )

        self.assertEqual(
            case.allowed_skills, ("builder", "evidence-before-claims")
        )

    def test_case_rejects_allowlist_missing_a_required_skill(self):
        with self.assertRaisesRegex(ValueError, "must include required skills: builder"):
            EvalCase.from_dict(
                {**_case_dict("builder"), "allowed_skills": []},
                source="builder.json",
            )

    def test_case_rejects_skill_that_is_both_allowed_and_forbidden(self):
        with self.assertRaisesRegex(ValueError, "both allowed and forbidden"):
            EvalCase.from_dict(
                {
                    **_case_dict("builder"),
                    "allowed_skills": ["builder", "whittler"],
                    "should_not_select": ["whittler"],
                },
                source="builder.json",
            )

    def test_case_accepts_negative_routing_boundary(self):
        case = EvalCase.from_dict(
            {
                "skills": [],
                "query": "Explain this already-working function.",
                "expected_behavior": ["Answers without starting a workflow"],
                "should_not_select": ["builder", "whittler"],
            },
            source="negative.json",
        )

        self.assertEqual(case.skills, ())
        self.assertEqual(case.should_not_select, ("builder", "whittler"))


class ClaudeEventParserTests(unittest.TestCase):
    def test_extracts_skill_result_and_usage(self):
        events = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Skill",
                            "input": {"skill": "hackinator:builder"},
                        }
                    ]
                },
            },
            {
                "type": "result",
                "subtype": "success",
                "result": "Built the thin slice.",
                "duration_ms": 1234,
                "total_cost_usd": 0.25,
                "usage": {
                    "input_tokens": 10,
                    "cache_read_input_tokens": 20,
                    "output_tokens": 30,
                },
                "modelUsage": {"claude-fable-5": {}},
            },
        ]

        result = parse_claude_events(_jsonl(events))

        self.assertEqual(result.selected_skills, ("builder",))
        self.assertEqual(result.output, "Built the thin slice.")
        self.assertEqual(result.model, "claude-fable-5")
        self.assertEqual(result.input_tokens, 10)
        self.assertEqual(result.cached_input_tokens, 20)
        self.assertEqual(result.output_tokens, 30)
        self.assertEqual(result.cost_usd, 0.25)
        self.assertEqual(result.duration_ms, 1234)
        self.assertIsNone(result.error)

    def test_reports_malformed_json_without_losing_valid_events(self):
        stream = "not-json\n" + _jsonl(
            [{"type": "result", "subtype": "error", "result": "failed"}]
        )

        result = parse_claude_events(stream)

        self.assertEqual(result.output, "failed")
        self.assertIn("malformed JSONL", result.error)


class CodexEventParserTests(unittest.TestCase):
    def test_extracts_skill_read_result_and_usage(self):
        events = [
            {
                "type": "item.completed",
                "item": {
                    "type": "command_execution",
                    "command": (
                        "/bin/bash -lc \"sed -n '1,240p' "
                        "/tmp/eval/.agents/skills/builder/SKILL.md\""
                    ),
                    "exit_code": 0,
                },
            },
            {
                "type": "item.completed",
                "item": {"type": "agent_message", "text": "Built the thin slice."},
            },
            {
                "type": "turn.completed",
                "usage": {
                    "input_tokens": 10,
                    "cached_input_tokens": 20,
                    "output_tokens": 30,
                },
            },
        ]

        result = parse_codex_events(_jsonl(events))

        self.assertEqual(result.selected_skills, ("builder",))
        self.assertEqual(result.output, "Built the thin slice.")
        self.assertEqual(result.input_tokens, 10)
        self.assertEqual(result.cached_input_tokens, 20)
        self.assertEqual(result.output_tokens, 30)
        self.assertIsNone(result.error)


class HarnessCommandTests(unittest.TestCase):
    def test_claude_uses_plugin_only_for_skill_condition(self):
        harness = ClaudeHarness()
        case = _case()
        workspace = Path("/tmp/eval")
        repo = Path("/repo")

        baseline = harness.command(case, "baseline", workspace, repo, model="sonnet")
        candidate = harness.command(case, "skills", workspace, repo, model="sonnet")

        self.assertIn("--bare", baseline)
        self.assertIn("--disable-slash-commands", baseline)
        self.assertNotIn("--plugin-dir", baseline)
        self.assertEqual(candidate[candidate.index("--plugin-dir") + 1], "/repo")
        self.assertNotIn("--disable-slash-commands", candidate)
        self.assertEqual(candidate[candidate.index("--model") + 1], "sonnet")

    def test_codex_disables_skill_catalog_only_for_baseline(self):
        harness = CodexHarness()
        case = _case()
        workspace = Path("/tmp/eval")
        repo = Path("/repo")

        baseline = harness.command(case, "baseline", workspace, repo, model="gpt-test")
        candidate = harness.command(case, "skills", workspace, repo, model="gpt-test")

        self.assertIn("skills.include_instructions=false", baseline)
        self.assertNotIn("skills.include_instructions=false", candidate)
        self.assertEqual(candidate[candidate.index("--model") + 1], "gpt-test")
        self.assertIn("read-only", candidate)

    def test_codex_enables_workspace_writes_when_case_requests_them(self):
        harness = CodexHarness()
        case = EvalCase.from_dict(
            {**_case_dict("builder"), "workspace_write": True},
            source="builder.json",
        )

        command = harness.command(
            case, "skills", Path("/tmp/eval"), Path("/repo")
        )

        self.assertIn("workspace-write", command)

    def test_codex_isolates_global_instructions_but_preserves_auth(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            auth_source = root / "real-codex-home/auth.json"
            auth_source.parent.mkdir()
            auth_source.write_text("{}")
            workspace = root / "workspace"
            workspace.mkdir()
            harness = CodexHarness(auth_source=auth_source)

            harness.prepare_workspace("baseline", workspace, root)
            environment = harness.environment(workspace)

            isolated_home = workspace / ".codex-home"
            self.assertEqual(environment["CODEX_HOME"], str(isolated_home))
            self.assertEqual(
                (isolated_home / "auth.json").resolve(), auth_source.resolve()
            )
            self.assertFalse((isolated_home / "AGENTS.md").exists())

    def test_codex_disables_discovered_user_skills(self):
        external_skill = Path("/home/test/.agents/skills/unrelated/SKILL.md")
        harness = CodexHarness(external_skill_paths=(external_skill,))

        command = harness.command(
            _case(), "skills", Path("/tmp/eval"), Path("/repo")
        )

        override = next(
            argument
            for argument in command
            if argument.startswith("skills.config=[{")
        )
        self.assertIn(str(external_skill), override)
        self.assertIn("enabled = false", override)


class TrialExecutionTests(unittest.TestCase):
    def test_runs_repeated_pairs_and_stages_skills_for_codex(self):
        calls = []

        def fake_run(command, **kwargs):
            workspace = Path(kwargs["cwd"])
            calls.append((command, workspace))
            if "skills.include_instructions=false" not in command:
                self.assertTrue(
                    (workspace / ".agents/skills/builder/SKILL.md").is_file()
                )
            output = _jsonl(
                [
                    {
                        "type": "item.completed",
                        "item": {"type": "agent_message", "text": "answer"},
                    },
                    {"type": "turn.completed", "usage": {"output_tokens": 4}},
                ]
            )
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            skill = repo / "skills/builder"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: builder\ndescription: Build.\n---\n")

            records = run_paired_trials(
                [_case()],
                CodexHarness(),
                repo_root=repo,
                trials=2,
                timeout=10,
                run_command=fake_run,
            )

        self.assertEqual(len(calls), 4)
        self.assertEqual(
            [(record.condition, record.trial) for record in records],
            [("baseline", 1), ("skills", 1), ("baseline", 2), ("skills", 2)],
        )
        self.assertTrue(all(record.result.output == "answer" for record in records))

    def test_load_eval_cases_can_filter_by_case_id(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "one/evals/first.json"
            second = root / "two/evals/second.json"
            first.parent.mkdir(parents=True)
            second.parent.mkdir(parents=True)
            first.write_text(json.dumps(_case_dict("one")))
            second.write_text(json.dumps(_case_dict("two")))

            cases = load_eval_cases(root, case_ids={"second"})

        self.assertEqual([case.case_id for case in cases], ["second"])


class GradingTests(unittest.TestCase):
    def test_candidate_grades_expected_and_excluded_skill_selection(self):
        case = EvalCase.from_dict(
            {**_case_dict("builder"), "should_not_select": ["whittler"]},
            source="builder.json",
        )

        grades = grade_trial(
            case,
            "skills",
            AgentResult(selected_skills=("builder",), output="done"),
            Path("/tmp"),
        )

        by_name = {grade.name: grade for grade in grades}
        self.assertTrue(by_name["expected_skills"].passed)
        self.assertTrue(by_name["excluded_skills"].passed)

    def test_candidate_grades_selections_outside_an_explicit_allowlist(self):
        case = EvalCase.from_dict(
            {**_case_dict("builder"), "allowed_skills": ["builder"]},
            source="builder.json",
        )

        grades = grade_trial(
            case,
            "skills",
            AgentResult(selected_skills=("builder", "walking-skeleton")),
            Path("/tmp"),
        )

        grade = next(grade for grade in grades if grade.name == "unexpected_skills")
        self.assertFalse(grade.passed)
        self.assertIn("walking-skeleton", grade.detail)

    def test_baseline_does_not_require_candidate_skill_selection(self):
        grades = grade_trial(
            _case(), "baseline", AgentResult(output="done"), Path("/tmp")
        )

        self.assertNotIn("expected_skills", {grade.name for grade in grades})

    def test_deterministic_output_and_filesystem_graders(self):
        case = EvalCase.from_dict(
            {
                **_case_dict("builder"),
                "graders": [
                    {"type": "output_contains", "value": "runnable"},
                    {"type": "output_regex", "pattern": "tests? pass"},
                    {"type": "file_exists", "path": "result.txt"},
                ],
            },
            source="builder.json",
        )
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "result.txt").write_text("ok")

            grades = grade_trial(
                case,
                "skills",
                AgentResult(output="Runnable artifact; tests pass."),
                workspace,
            )

        grader_results = [grade.passed for grade in grades if grade.name.startswith("grader_")]
        self.assertEqual(grader_results, [True, True, True])

    def test_command_grader_uses_argv_without_a_shell(self):
        calls = []

        def fake_run(command, **kwargs):
            calls.append((command, kwargs))
            return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

        case = EvalCase.from_dict(
            {
                **_case_dict("builder"),
                "graders": [{"type": "command", "argv": ["make", "test"]}],
            },
            source="builder.json",
        )

        grades = grade_trial(
            case, "skills", AgentResult(), Path("/tmp"), run_command=fake_run
        )

        self.assertTrue(grades[-1].passed)
        self.assertEqual(calls[0][0], ["make", "test"])
        self.assertNotIn("shell", calls[0][1])


class ReportTests(unittest.TestCase):
    def test_report_contains_reproducibility_metadata_and_aggregates(self):
        result = AgentResult(
            selected_skills=("builder",),
            output="done",
            model="gpt-test",
            input_tokens=10,
            output_tokens=5,
            duration_ms=100,
        )
        grades = grade_trial(_case(), "skills", result, Path("/tmp"))
        records = [TrialRecord("builder", "skills", 1, result, grades)]

        report = build_report(
            [_case()],
            records,
            harness_name="codex",
            harness_version="codex-cli 1.2.3",
            requested_model="gpt-test",
            git_metadata={"commit": "abc123", "dirty": False},
            generated_at="2026-09-12T12:00:00Z",
        )

        self.assertEqual(report["schema_version"], 1)
        self.assertEqual(report["harness"]["name"], "codex")
        self.assertEqual(report["harness"]["requested_model"], "gpt-test")
        self.assertEqual(report["git"]["commit"], "abc123")
        self.assertEqual(report["summary"]["skills"]["runs"], 1)
        self.assertEqual(
            report["summary"]["skills"]["grades"]["expected_skills"],
            {"passed": 1, "total": 1},
        )
        self.assertEqual(report["cases"][0]["expected_behavior"], ["Produces a runnable artifact"])

    def test_report_summarizes_selectivity_and_cascades(self):
        case = EvalCase.from_dict(
            {**_case_dict("builder"), "allowed_skills": ["builder"]},
            source="builder.json",
        )
        result = AgentResult(selected_skills=("builder", "walking-skeleton"))
        records = [
            TrialRecord(
                "builder",
                "skills",
                1,
                result,
                grade_trial(case, "skills", result, Path("/tmp")),
            )
        ]

        report = build_report(
            [case],
            records,
            harness_name="codex",
            harness_version="codex-cli 1.2.3",
            git_metadata={"commit": "abc123", "dirty": False},
        )

        summary = report["summary"]["skills"]["selection"]
        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["mean_per_run"], 2.0)
        self.assertEqual(summary["multi_skill_runs"], 1)
        self.assertEqual(summary["unexpected_runs"], 1)


class CommandLineTests(unittest.TestCase):
    def test_list_prints_cases_without_running_a_harness(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            case_path = repo / "skills/builder/evals/quick.json"
            case_path.parent.mkdir(parents=True)
            case_path.write_text(json.dumps(_case_dict("builder")))
            output = io.StringIO()

            with patch("sys.stdout", output):
                status = main(["--repo-root", str(repo), "--list"])

        self.assertEqual(status, 0)
        self.assertIn("quick", output.getvalue())
        self.assertIn("builder", output.getvalue())


class SchemaCheckerTests(unittest.TestCase):
    def test_checker_rejects_unknown_allowed_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            path.write_text(
                json.dumps(
                    {
                        **_case_dict("builder"),
                        "allowed_skills": ["builder", "invented-skill"],
                    }
                )
            )

            errors = check_evals.check_case(path, {"builder"})

        self.assertTrue(any("invented-skill" in error for error in errors))


def _jsonl(events):
    return "".join(json.dumps(event) + "\n" for event in events)


def _case():
    return EvalCase.from_dict(_case_dict("builder"), source="builder.json")


def _case_dict(skill):
    return {
        "skills": [skill],
        "query": "Build the smallest runnable thing.",
        "expected_behavior": ["Produces a runnable artifact"],
    }


if __name__ == "__main__":
    unittest.main()
