# OPT Career Intelligence Agent

## Live Application

https://opt-career-intelligence-agent.streamlit.app/

## GitHub Repository

https://github.com/mutuac-bit/opt-career-intelligence-agent

---

# Author

Cynthia Mutua

GitHub: mutuac-bit

---

# Overview

OPT Career Intelligence Agent is an AI-powered career advisor built for international students on F-1 STEM OPT.

The system helps users:

* Discover relevant job opportunities
* Evaluate visa sponsorship likelihood
* Analyze uploaded resumes
* Receive personalized career recommendations
* Prioritize applications using AI reasoning

Unlike traditional job boards, this application combines live search, grounding, evaluation, and autonomous tool use.

---

# Problem Statement

International students often spend significant time applying for jobs without knowing whether employers are likely to sponsor work visas.

The goal of this project is to help students focus on opportunities that better align with their skills, location preferences, and sponsorship requirements.

Target Users:

* F-1 Students
* STEM OPT Students
* International Graduates
* Early Career Professionals

---

# System Architecture

The application uses GPT-4.1-mini as an autonomous career intelligence agent.

Architecture:

User

↓

GPT-4.1-mini

↓

Tool Calling Layer

↓

search_jobs()

analyze_resume()

check_sponsorship()

↓

Final Recommendation

---

# Models

## GPT-4.1-mini

Purpose:

* Tool selection
* Career reasoning
* Resume analysis
* Recommendation generation

Reason for selection:

GPT-4.1-mini provides reliable reasoning, tool calling capability, and lower operational cost compared to larger models.

---

# MCP Tool Definitions

## Tool 1: search_jobs()

Purpose:

Search live job postings using Tavily.

Inputs:

* role
* city

Returns:

* title
* url
* content snippet

---

## Tool 2: analyze_resume()

Purpose:

Read uploaded resume PDFs.

Inputs:

* PDF file

Returns:

* extracted resume text

---

## Tool 3: check_sponsorship()

Purpose:

Estimate sponsorship likelihood.

Inputs:

* company name

Returns:

* GREEN
* YELLOW
* explanation

---

# Agentic Behavior

This project implements true agentic behavior.

The model decides:

* Whether a tool is needed
* Which tool should be called
* When to call multiple tools
* When enough information exists
* When execution should stop

The application does not force a fixed sequence of actions.

Decision-making occurs inside the model.

---

# Evidence of Agentic Tool Use

Example execution:

User Request:

"Find sponsorship-friendly Data Analyst jobs in Atlanta."

GPT-4.1-mini decides to call:

search_jobs()

↓

Tool returns live search results.

↓

GPT-4.1-mini decides to call:

check_sponsorship()

↓

Tool returns sponsorship rating.

↓

GPT-4.1-mini combines:

* tool outputs
* user profile
* resume context

↓

Final recommendation generated.

This demonstrates autonomous tool selection and execution rather than hardcoded routing.

---

# Grounding

The application uses multiple grounding sources.

## User Profile

* Visa Status
* Experience
* Skills
* Target Role
* Target City

## Resume Grounding

Uploaded PDF resume content.

## Live Search Grounding

Real-time Tavily job search results.

The model receives information unavailable from pretraining alone.

---

# Prompt Engineering

## Prompt Version 1

Search for jobs matching the target role.

Issue:

Returned many irrelevant opportunities.

---

## Prompt Version 2

Search only for opportunities that:

* Match target role
* Match location
* Consider sponsorship
* Consider resume skills
* Use live evidence

Result:

Higher relevance and better recommendations.

---

# Evaluation

Evaluation was performed using 10 sponsorship classification test cases.

Files:

evaluation/test_cases.json

evaluation/eval.py

evaluation/results.json

Results:

Total Cases: 10

Correct Predictions: 10

Accuracy: 100%

Evaluation Output:

Microsoft → GREEN

Google → GREEN

Amazon → GREEN

Apple → GREEN

Meta → GREEN

Small Local Consulting → YELLOW

Neighborhood IT Services → YELLOW

Regional Accounting Group → YELLOW

Local Manufacturing Company → YELLOW

Startup XYZ → YELLOW

Final Accuracy:

100.00%

---

# Example Interaction

Input:

Role:
Data Analyst

City:
Atlanta

Visa:
F-1 STEM OPT

Skills:
Python, SQL, Power BI

Output:

* Job recommendations
* Sponsorship analysis
* Resume feedback
* Application strategy

---

# Iteration Based On Feedback

Draft Version:

* Limited documentation
* Weak evaluation evidence
* Sequential workflow

Instructor Feedback:

* Need stronger agentic behavior
* Need MCP tool implementation
* Need evaluation evidence
* Need clearer documentation

Changes Made:

* Added MCP tools
* Added tool execution loop
* Added evaluation framework
* Added build log
* Added grounding sources
* Added detailed architecture documentation

---

# Limitations

* Sponsorship analysis uses heuristics
* Not connected to USCIS sponsorship databases
* Search quality depends on Tavily results
* Large resumes may be truncated

---

# Future Improvements

* H-1B sponsor database integration
* Salary intelligence
* Resume tailoring agent
* Application tracking dashboard
* Multi-agent collaboration

---

# Deployment

Platform:

Streamlit Community Cloud

Requirements:

OPENAI_API_KEY

TAVILY_API_KEY

Run Locally:

streamlit run app.py

---

# Repository Structure

app.py

tools.py

requirements.txt

README.md

BUILD_LOG.md

evaluation/

* eval.py
* test_cases.json
* results.json

---

# Conclusion

This project combines prompt engineering, grounding, MCP tools, evaluation, and agentic decision making into a deployable AI application that solves a real problem for international students pursuing career opportunities in the United States.
