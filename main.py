__import__('pysqlite3')

import sys
import os

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crewai import Crew, Process

from agents.agents import (
    issue_investigator,
    log_analyzer,
    solution_specialist
)

from tasks.tasks import (
    analyze_logs_task,
    investigate_issue_task,
    provide_solution_task
)

# =========================================
# CONFIG
# =========================================

log_file = "error.log"
MAX_CHARS = 20000

print("\n" + "=" * 60)
print("FILE ACCESS VALIDATION")
print("=" * 60)

print("File Exists :", os.path.exists(log_file))
print("Readable    :", os.access(log_file, os.R_OK))
print("Absolute Path:", os.path.abspath(log_file))

# =========================================
# READ LOGS
# =========================================

log_content = ""

try:
    with open(log_file, "r") as f:
        log_content = f.read()

    print("\n===== LOG PREVIEW =====\n")
    print(log_content[:1000])

except Exception as e:
    print("\nFILE READ ERROR:", str(e))

# =========================================
# SAFETY CHECK
# =========================================

if not log_content:
    print("\n❌ No log content found. Exiting.")
    exit(1)

# truncate for safety
if len(log_content) > MAX_CHARS:
    print("\n⚠️ Log truncated for analysis")
    log_content = log_content[-MAX_CHARS:]

print("\n" + "=" * 60)

# =========================================
# CREW SETUP
# =========================================

devops_crew = Crew(
    agents=[
        log_analyzer,
        issue_investigator,
        solution_specialist
    ],
    tasks=[
        analyze_logs_task,
        investigate_issue_task,
        provide_solution_task
    ],
    verbose=True,
    process=Process.sequential,
)

# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("DevOps Issue Analysis v2")
    print("=" * 60)

    result = devops_crew.kickoff(
        inputs={
            "log_content": log_content
        }
    )

    print("\n\n========== FINAL RESULT ==========\n")
    print(result)