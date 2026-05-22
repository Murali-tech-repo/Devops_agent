
import os

from typing import Tuple, Any

from crewai import Task
from crewai.tasks.task_output import TaskOutput
from pydantic import BaseModel, Field

from agents.agents import (
    issue_investigator,
    log_analyzer,
    solution_specialist
)

os.makedirs("task_outputs", exist_ok=True)


# =========================
# Pydantic Output Model
# =========================

class LogAnalysisReport(BaseModel):
    primary_issue: str = Field(
        description="One-line description of the main issue"
    )

    root_cause: str = Field(
        description="Root cause analysis based on log evidence"
    )

    errors: list[str] = Field(
        description="All errors found in the log"
    )

    affected_components: list[str] = Field(
        description="System components affected"
    )

    timeline: list[str] = Field(
        description="Sequence of events leading to failure"
    )


# =========================
# Guardrail 1
# =========================

def validate_log_analysis(
    result: TaskOutput
) -> Tuple[bool, Any]:

    report = result.pydantic

    if not report or not report.errors:
        return (
            False,
            "Must identify at least one error"
        )

    return (True, report)


# =========================
# Guardrail 2
# =========================

def validate_solution(
    result: TaskOutput
) -> Tuple[bool, Any]:

    output = str(result)

    command_count = output.count("$")

    if command_count < 1:
        return (
            False,
            "Solution must contain at least 3 shell commands"
        )

    return (True, output)


# =========================
# Task 1
# =========================
analyze_logs_task = Task(
    description="""
You are a STRICT PRODUCTION LOG PARSER.

Your ONLY responsibility is to extract information
directly visible in the provided logs.

==================================================
LOG CONTENT:
{log_content}
==================================================

STRICT RULES:
- Use ONLY the provided logs
- Do NOT use external knowledge
- Do NOT infer missing information
- Do NOT explain errors
- Do NOT summarize logs
- Do NOT paraphrase
- Do NOT generate fake entries
- Do NOT modify original log lines
- Do NOT assume root causes
- Do NOT provide solutions
- Every extracted line MUST exist exactly in logs

EXTRACTION REQUIREMENTS:
1. Extract timestamps exactly as present
2. Extract ERROR lines exactly as present
3. Extract WARNING lines exactly as present
4. Extract stack traces exactly as present
5. Extract exception names exactly as present
6. Extract failed services/components exactly as present

If a section is unavailable, return:
NOT FOUND IN LOGS

OUTPUT MUST BE FACTUAL ONLY.
""",

    expected_output="""
# Extracted Log Report

## Timestamps
- Exact timestamps from logs

## Errors
- Exact ERROR lines

## Warnings
- Exact WARNING lines

## Exceptions
- Exact exception messages

## Stack Traces
- Original stack traces only

## Failed Services
- Exact service/component names

If unavailable:
NOT FOUND IN LOGS
""",

    agent=log_analyzer,
    output_file="task_outputs/log_analysis.md"
)
# =========================
# Task 2
# =========================
investigate_issue_task = Task( description=""" You are only allowed to use the given log analysis. DO NOT assume external knowledge. Only describe: - what is already present in logs - what dependencies are mentioned - what services failed in logs DO NOT search or guess solutions. """, expected_output=""" Facts strictly derived from logs only """, agent=issue_investigator, context=[analyze_logs_task], output_file="task_outputs/investigation_report.md", )

# =========================
# Task 3
# =========================

provide_solution_task = Task(
    description="""
    Provide a complete remediation plan.

    Include:

    1. Step-by-step fix
    2. Shell commands
    3. Verification steps
    4. Prevention measures
    """,

    expected_output="""
    Detailed remediation plan with commands
    """,

    guardrail=validate_solution,

    agent=solution_specialist,

    context=[
        analyze_logs_task,
        investigate_issue_task
    ],

    output_file="task_outputs/solution_plan.md",
)

