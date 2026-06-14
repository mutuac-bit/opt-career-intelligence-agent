# OPT Career Intelligence Agent

## Overview

OPT Career Intelligence Agent is an AI-powered career advisor for international students on F-1 STEM OPT.

The system helps students:

* Find relevant jobs
* Identify sponsorship-friendly employers
* Analyze resumes
* Prioritize applications
* Make career decisions using live job market data

Unlike traditional job boards, this application combines live search, resume grounding, sponsorship analysis, and autonomous tool use.

---

# Problem Statement

International students often spend hundreds of hours applying for jobs without knowing whether employers are likely to sponsor work visas.

This project helps students focus their efforts on jobs that better match their skills, location preferences, and sponsorship needs.

Target Users:

* F-1 Students
* STEM OPT Students
* International Graduates
* Early Career Professionals

---

# System Architecture

The system uses GPT-4.1-mini as an autonomous orchestration agent.

Architecture:

User

↓

GPT-4.1-mini Career Agent

↓

Tool Calling Layer

↓

search_jobs()

analyze_resume()

check_sponsorship()

↓

Final Recommendation

---

# Agentic Behavior

This project implements true agentic behavior.

The model decides:

* Whether to call a tool
* Which tool to call
* When to call multiple tools
* When enough information exists
* When to stop

The Python application does not hardcode a fixed workflow.

Instead, GPT-4.1-mini determines the next action during execution.

---

# MCP Tool Definitions

## Tool 1

search_jobs()

Purpose:

Search live job postings using Tavily.

Inputs:

* role
* city

Returns:

* job title
* URL
* job description snippet

---

## Tool 2

analyze_resume()

Purpose:

Extract text from uploaded resume PDFs.

Inputs:

* PDF file

Returns:

* Resume text

---

## Tool 3

check_sponsorship()

Purpose:

Analyze sponsorship likelihood.

Inputs:

* company name

Returns:

* GREEN
* YELLOW

plus explanation

---

# Grounding

The system uses multiple grounding sources.

## User Profile

* Visa Status
* Experience
* Skills
* Target Role
* Target City

## Resume Grounding

Uploaded resume PDF content.

## Live Search Grounding

Tavily web search results.

These sources provide information unavailable from model pretraining.

---

# Prompt Engineering

## Prompt Version 1

Search for jobs matching the user's role.

Problem:

Returned many irrelevant results.

---

## Prompt Version 2

Search only for jobs that:

* Match role
* Match location
* Consider sponsorship
* Consider resume skills
* Use live search evidence

Result:

Improved relevance and recommendation quality.

---

# Evaluation

Evaluation was performed using 10 sponsorship test cases.

Metrics:

{
"accuracy": 1.00,
"total_cases": 10,
"correct_predictions": 10
}

Interpretation:

The sponsorship classifier correctly identified all benchmark cases.

Evaluation script:

evaluation/eval.py

Test cases:

evaluation/test_cases.json

---

# Example Interaction

Input

Role:
Data Analyst

City:
Atlanta

Visa:
F-1 STEM OPT

Skills:
Python, SQL, Power BI

Output

* Job recommendations
* Sponsorship analysis
* Resume feedback
* Application strategy

---

# Iteration Based On Feedback

Draft Version:

* Sequential pipeline
* Limited evaluation
* Minimal documentation

Feedback:

* Need stronger agentic behavior
* Need MCP tools
* Need evaluation evidence

Final Version:

* Added MCP tool definitions
* Added tool execution loop
* Added autonomous decision making
* Added evaluation framework
* Added documentation

---

# Limitations

* Sponsorship analysis uses heuristics
* Not connected to USCIS sponsor database
* Search quality depends on Tavily results
* Large resumes may be truncated

---

# Future Work

* Real H-1B sponsor database integration
* Application tracking dashboard
* Resume tailoring agent
* Salary intelligence tools
* Multi-agent collaboration

---

# Deployment

Requirements:

* OPENAI_API_KEY
* TAVILY_API_KEY

Run:

streamlit run app.py

Deploy:

Streamlit Community Cloud

---

# Repository

Author: Finnete

Capstone Project

Generative AI Applications
