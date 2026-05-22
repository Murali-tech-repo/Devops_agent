import os

from crewai import Agent
from crewai.llm import LLM
from dotenv import load_dotenv

load_dotenv()


from tools.tools import  log_reader_tool

llm = LLM(
    model="ollama/mistral",
    base_url="http://localhost:11434"
)



# log_analyzer = Agent(
#     role="DevOps Log Analyzer",
#     goal="Fetch and strictly extract log issues from Loki",
#     backstory="Expert SRE specialized in Kubernetes & observability",
#     tools=[log_reader_tool],  # IMPORTANT: tool not used directly in agent
#     llm=llm,
#     verbose=True,
#     respect_context_window=True,
#     max_iter=5,
#     max_execution_time=600,
#     max_rpm=15,
# )

log_analyzer = Agent(
    role="DevOps Log Analyzer",

    goal="""
    Analyze only the provided log content and extract
    actual errors, warnings, failures, and incident details
    strictly from the given logs without assumptions,
    external knowledge, or fabricated information.
    """,

    backstory="""
    You are a highly precise Site Reliability Engineer (SRE)
    specializing in log analysis and observability.

    Your responsibility is to:
    - Analyze only the provided log content
    - Extract exact issues from logs
    - Identify error patterns
    - Categorize incidents based strictly on evidence present in logs
    - Avoid assumptions or imaginary root causes

    Rules:
    - Do not use external knowledge
    - Do not guess missing information
    - Do not generate issues not present in logs
    - Do not provide fixes unless explicitly visible in logs
    - Only report findings directly supported by log evidence
    """,

    llm=llm,
    verbose=True,
    respect_context_window=True,
    max_iter=5,
    max_execution_time=600,
    max_rpm=15,
)

issue_investigator = Agent(
    role="DevOps Issue Investigator",
    goal="Investigate identified issues by searching documentation, forums, and known solutions online",
    llm=llm,
    backstory="""You are a DevOps troubleshooting specialist who excels at quickly 
    finding solutions to technical problems. You know how to search effectively for 
    similar issues, identify reliable sources, and gather comprehensive information 
    about error patterns and their solutions.""",
    tools=[log_reader_tool],
    verbose=True,
    respect_context_window=True,
    max_iter=5,
    max_execution_time=600,
    max_rpm=15,
)

solution_specialist = Agent(
    role="DevOps Solution Specialist",
    goal="Provide clear, actionable solutions with step-by-step instructions based on investigation findings",
    llm=llm,
    backstory="""You are a DevOps solutions architect who specializes in creating 
    reliable, step-by-step remediation plans for infrastructure and deployment issues. 
    You always provide official documentation references, tested solutions, and 
    preventive measures to avoid future occurrences.""",
    verbose=True,
    respect_context_window=True,
    max_iter=4,
    max_execution_time=450,
    max_rpm=8,
)