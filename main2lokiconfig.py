__import__('pysqlite3')

import sys
import os
from dotenv import load_dotenv

load_dotenv()
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

from tools.loki_tool import LokiLogTool


# =========================================
# CONFIG
# =========================================

MAX_CHARS = 20000

print("\n" + "=" * 60)
print("LOKI ACCESS VALIDATION")
print("=" * 60)

# =========================================
# FETCH FROM LOKI (NOT FILE)
# =========================================

loki = LokiLogTool(
    base_url=os.getenv("LOKI_URL"),
    token=os.getenv("LOKI_TOKEN")
)

log_content = loki.get_last_15min_logs(
    query='{app="api/report-service"}'
)

print("\n===== LOKI LOG PREVIEW =====\n")
print(log_content[:1000])

# =========================================
# SAFETY CHECK
# =========================================

if not log_content:
    print("\n❌ No logs received from Loki. Exiting.")
    exit(1)

if len(log_content) > MAX_CHARS:
    print("\n⚠️ Logs truncated for LLM safety")
    log_content = log_content[-MAX_CHARS:]

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
    print("DevOps AI Analysis (LOKI MODE)")
    print("=" * 60)

    result = devops_crew.kickoff(
        inputs={
            "log_content": log_content
        }
    )

    print("\n\n========== FINAL RESULT ==========\n")
    print(result)