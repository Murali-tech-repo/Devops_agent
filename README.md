# Devops_agent

# AI-Powered DevOps Incident Analyzer

## Overview

AI-Powered DevOps Incident Analyzer is an intelligent multi-agent system built using CrewAI and Ollama to automate log analysis, issue investigation, and solution generation for DevOps and SRE teams.

The system reads logs from sources like Loki or log files, identifies critical issues, investigates related solutions using LLM reasoning, and provides actionable remediation steps.

This project is designed to reduce manual debugging time and help DevOps engineers quickly resolve infrastructure and application issues.

---

# Features

* Automated log analysis
* Error categorization and extraction
* AI-powered issue investigation
* Root cause analysis
* Suggested remediation steps
* Step-by-step troubleshooting guidance
* Loki/log file integration
* Local LLM execution using Ollama
* Multi-agent orchestration using CrewAI

---

# Architecture

The system contains multiple AI agents working together.

## 1. Log Analyzer Agent

Responsible for:

* Reading logs from Loki or files
* Extracting important errors
* Identifying issue categories
* Detecting failure patterns

### Technologies

* CrewAI Agent
* Loki/File Reader Tool
* Ollama LLM

---

## 2. Issue Investigator Agent

Responsible for:

* Investigating identified issues
* Searching for related known problems
* Finding documentation references
* Understanding root causes

### Responsibilities

* Kubernetes issue investigation
* Container failure analysis
* CI/CD troubleshooting
* Infrastructure debugging

---

## 3. Solution Specialist Agent

Responsible for:

* Generating remediation plans
* Providing step-by-step fixes
* Suggesting preventive actions
* Recommending best practices

### Output Includes

* Solution steps
* Configuration fixes
* Deployment recommendations
* Preventive monitoring suggestions

---

# Tech Stack

* Python
* CrewAI
* Ollama
* Mistral / Qwen Models
* Loki
* Kubernetes
* Docker

---

# Recommended Models

For systems with 16GB RAM:

| Model            | Purpose                                 |
| ---------------- | --------------------------------------- |
| mistral          | Fast and lightweight                    |
| qwen2.5-coder:7b | Best for debugging and DevOps reasoning |
| phi3             | Lightweight alternative                 |

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd devop-begineer
```

---

## Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Install Ollama

Install Ollama from:

https://ollama.com

---

# Pull Required Models

```bash
ollama pull mistral
```

OR

```bash
ollama pull qwen2.5-coder:7b
```

---

# Environment Variables

Create a `.env` file:

```env
OLLAMA_BASE_URL=http://localhost:11434
EXA_API_KEY=your_api_key
```

---

# Running the Project

```bash
python main.py
```

---

# Sample Agent Configuration

```python
llm = LLM(
    model="ollama/mistral",
    base_url="http://localhost:11434"
)
```

---

# Example Workflow

1. Logs are fetched from Loki or files
2. Log Analyzer extracts critical issues
3. Issue Investigator searches for related solutions
4. Solution Specialist generates remediation steps
5. Final report is generated

---

# Future Improvements

* ChromaDB memory integration
* RAG-based incident history
* Slack/WhatsApp alerts
* Kubernetes auto-remediation
* Grafana integration
* Incident dashboard
* Multi-cluster support
* AI-powered preventive monitoring

---

# Use Cases

* Kubernetes incident analysis
* Production issue debugging
* CI/CD pipeline troubleshooting
* Application crash investigation
* Infrastructure monitoring
* Automated SRE assistance

---

# Advantages

* Reduces manual troubleshooting time
* Faster incident resolution
* Centralized AI-powered investigation
* Improved DevOps productivity
* Works completely locally using Ollama

---

# License

MIT License

---

# Author

Murali Yadav

AI-Powered DevOps & Automation Engineer

Output 

<img width="1920" height="1080" alt="Screenshot from 2026-05-19 12-02-59" src="https://github.com/user-attachments/assets/b1724af5-fb1a-4bc3-8cf2-30a23f0b1d14" />
<img width="1920" height="1080" alt="Screenshot from 2026-05-19 12-07-07" src="https://github.com/user-attachments/assets/1e0124b2-8589-44f1-a628-625a941fbd31" />
<img width="1920" height="1080" alt="Screenshot from 2026-05-19 12-07-16" src="https://github.com/user-attachments/assets/688f07d4-42be-4a41-b130-89ee1ee98243" />

