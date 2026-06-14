# BUILD LOG

## Project

OPT Career Intelligence Agent

Author: Cynthia Mutua

---

# Project Goal

Build an AI-powered career advisor for F-1 STEM OPT students that combines:

* Prompt engineering
* Grounding
* MCP tools
* Agentic behavior
* Evaluation
* Deployment

into a complete production-ready application.

---

# Initial Idea

The original concept was a simple sponsorship-aware job search assistant.

Users would enter:

* skills
* role
* city

and receive job recommendations.

Issue:

The first version behaved like a traditional pipeline and did not demonstrate autonomous decision-making.

---

# First Prototype

Workflow:

Search Jobs

↓

Analyze Results

↓

Generate Recommendations

Problem:

The same sequence executed every time.

This was workflow automation rather than agentic behavior.

---

# Sponsorship Analysis

Added sponsorship screening logic.

Goal:

Estimate whether employers were likely to sponsor international students.

Output:

GREEN

YELLOW

Issue:

Many companies do not explicitly mention sponsorship in job postings.

---

# Grounding Improvements

Added three grounding sources.

## User Profile Grounding

* Visa status
* Skills
* Experience
* Role
* City

## Resume Grounding

PDF resume upload and extraction.

## Live Search Grounding

Real-time Tavily search.

Result:

Recommendations became more relevant and personalized.

---

# Prompt Iteration

## Version 1

Search for jobs matching the user's role.

Issue:

Large number of irrelevant opportunities.

---

## Version 2

Search only for jobs that:

* Match role
* Match location
* Consider sponsorship
* Use grounding context
* Prioritize user skills

Result:

Higher recommendation quality.

---

# MCP Tool Development

Implemented three MCP-style tools.

## search_jobs()

Live job search via Tavily.

---

## analyze_resume()

PDF resume reader.

---

## check_sponsorship()

Sponsorship classification.

---

# Agentic Architecture

Instructor feedback emphasized the distinction between pipelines and agents.

Original:

Search

↓

Analyze

↓

Score

This was deterministic.

New Architecture:

GPT-4.1-mini decides:

* whether tools are needed
* which tools to call
* when to stop

Decision making moved into the model.

---

# Evaluation Framework

Created:

evaluation/test_cases.json

evaluation/eval.py

evaluation/results.json

Evaluation Results:

Total Cases: 10

Correct: 10

Accuracy: 100%

Example Outputs:

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

---

# Challenges Encountered

## Challenge 1

API key management during deployment.

Solution:

Streamlit secrets configuration.

---

## Challenge 2

GitHub push protection.

Solution:

Removed secrets from repository history and updated .gitignore.

---

## Challenge 3

Need for stronger agentic behavior.

Solution:

Implemented OpenAI tool-calling loop.

---

# Final Improvements

Compared to the draft:

✓ Added MCP tools

✓ Added autonomous tool selection

✓ Added grounding

✓ Added evaluation

✓ Added deployment

✓ Added build documentation

✓ Added detailed README

---

# Future Work

* Verified H-1B sponsorship database
* Salary intelligence
* Resume tailoring
* Multi-agent collaboration
* Application tracking

---

# Reflection

The most important lesson from this project was understanding the difference between a pipeline and an agent.

A pipeline follows predefined steps.

An agent decides what actions to take.

Moving tool selection into GPT-4.1-mini transformed the application into an agentic system while satisfying the project requirements.
