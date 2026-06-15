# OPT Career Intelligence Agent

## Live Application

https://opt-career-intelligence-agent.streamlit.app/

## GitHub Repository

https://github.com/mutuac-bit/opt-career-intelligence-agent


---

# Project Overview

OPT Career Intelligence Agent is an AI-powered career strategy platform designed specifically for international students studying in the United States under F-1 OPT and STEM OPT status.

The application helps students identify career opportunities, evaluate sponsorship potential, analyze resumes, discover skill gaps, and create a targeted application strategy using autonomous AI decision-making.

Unlike traditional job boards that only return job listings, this system combines live job market intelligence, visa sponsorship analysis, resume evaluation, and career planning into a single AI-driven workflow.

---

# Problem Statement

International students face a unique challenge when applying for jobs in the United States.

Many companies advertise positions without clearly indicating whether visa sponsorship is available. Students often spend significant time applying to positions that are unlikely to support long-term employment authorization.

This project was created to help international students make smarter application decisions by:

* Finding relevant job opportunities
* Evaluating sponsorship potential
* Analyzing resumes
* Identifying skill gaps
* Prioritizing applications
* Creating personalized action plans

Target Users:

* F-1 Students
* STEM OPT Students
* International Graduates
* Early Career Professionals
* Students seeking H-1B sponsorship pathways

---

# System Architecture

The system combines GPT-4.1-mini, live web search, tool calling, grounding, evaluation, and deployment.

Architecture Flow:

User Input

↓

GPT-4.1-mini Agent

↓

Autonomous Tool Selection

↓

search_jobs()

analyze_resume()

check_sponsorship()

↓

Tool Results Returned

↓

GPT-4.1-mini Reasoning

↓

Career Intelligence Report

---

# Technologies Used

Frontend:

* Streamlit

AI Model:

* GPT-4.1-mini

External Tool:

* Tavily Search API

Programming Language:

* Python

Deployment:

* Streamlit Community Cloud

Version Control:

* GitHub

---

# Agentic Architecture

This project was intentionally designed to satisfy the requirements of an agentic AI system.

The model is responsible for deciding:

* Whether tools should be called
* Which tools should be called
* How many tools should be called
* Whether additional information is needed
* When sufficient evidence has been gathered
* When to stop execution

The application does not use hardcoded routing logic.

The model drives execution through OpenAI tool-calling.

This satisfies the project definition of agentic behavior.

---

# MCP Tool Definitions

The project implements three MCP-style tools.

## Tool 1: search_jobs

Purpose:

Search for live job opportunities using Tavily Search.

Inputs:

* role
* city

Example:

search_jobs(
role="Data Analyst",
city="Atlanta"
)

Returns:

* job titles
* company names
* URLs
* job descriptions

Why It Matters:

Provides information unavailable from model pretraining.

---

## Tool 2: analyze_resume

Purpose:

Read uploaded PDF resumes.

Inputs:

* PDF resume

Returns:

* extracted text
* resume context

Why It Matters:

Allows the model to evaluate user-specific information rather than guessing.

---

## Tool 3: check_sponsorship

Purpose:

Estimate sponsorship likelihood.

Inputs:

* company name

Returns:

* sponsorship rating
* reasoning
* confidence level

Possible Outputs:

GREEN

Likely sponsor

YELLOW

Uncertain sponsorship

Why It Matters:

Provides sponsorship intelligence unavailable from static model knowledge.

---

# Evidence of MCP Tool Execution

Example Run:

User Request:

"Find sponsorship-friendly Data Analyst jobs in Atlanta."

Step 1

GPT-4.1-mini decides to call:

search_jobs()

Step 2

Tavily returns live search results.

Step 3

GPT-4.1-mini decides to call:

check_sponsorship()

Step 4

Tool returns sponsorship analysis.

Step 5

GPT-4.1-mini combines:

* tool outputs
* user profile
* resume data

Step 6

Final recommendations are generated.

This demonstrates actual tool execution and autonomous decision making.

---

# Grounding Strategy

A major requirement of Project 3 was grounding.

The system uses three grounding sources.

## User Profile Grounding

Collected through the sidebar:

* Visa Status
* Experience
* Skills
* Target Role
* Target City

---

## Resume Grounding

Users can upload resumes in PDF format.

Resume content is extracted and provided to the model.

This enables personalized recommendations.

---

## Live Search Grounding

Job opportunities are retrieved using Tavily.

This provides:

* current market information
* current company information
* current job opportunities

The model receives information unavailable from pretraining.

---

# Prompt Engineering

Prompt engineering was deliberately iterative.

## Prompt Version 1

Original Prompt

"Find jobs matching the user's role."

Problem:

Returned generic recommendations.

Many results were irrelevant.

No sponsorship focus.

---

## Prompt Version 2

Added:

* sponsorship focus
* visa awareness
* user profile grounding
* structured output requirements

Improvement:

Better role matching.

More actionable recommendations.

---

## Prompt Version 3 (Final)

Added:

* executive summary
* sponsorship strategy
* resume review
* skills gap analysis
* action planning
* scoring framework

Improvement:

Generated detailed career intelligence reports instead of generic advice.

---

# Example Output

The system generates:

## Executive Summary

Candidate strengths

Candidate weaknesses

Sponsorship outlook

---

## Job Market Intelligence

Company

Role Fit

Location Fit

Sponsorship Confidence

Risk Level

Recommended Action

---

## Skills Gap Analysis

Current Skills

Missing Skills

Recommended Certifications

Recommended Projects

---

## Resume Recommendations

Missing Keywords

Weak Areas

Optimization Suggestions

---

## Sponsorship Strategy

Priority Companies

Networking Recommendations

Risk Assessment


---

## Final Scores

Skill Match Score

Market Readiness Score

Sponsorship Readiness Score

Overall Competitiveness Score

---

# Evaluation

A formal evaluation framework was implemented.

Files:

evaluation/test_cases.json

evaluation/eval.py

evaluation/results.json

---

## Evaluation Dataset


10 sponsorship classification scenarios.

Examples:

Microsoft

Google

Amazon

Apple

Meta

Small Local Consulting

Neighborhood IT Services

Regional Accounting Group

Local Manufacturing Company


---

## Evaluation Results

Actual Run:

Total Cases: 10

Correct Predictions: 10

Accuracy: 100.00%

Console Output:

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

Results saved to:

evaluation/results.json

---

# Iteration Based On Feedback

The draft version received several areas for improvement.

## Draft Weaknesses

* Limited documentation
* Weak evaluation evidence
* Generic recommendations
* Insufficient explanation of agentic behavior
* Missing MCP tool documentation

---

## Improvements Made

Added:

✓ OpenAI Tool Calling

✓ MCP Tool Definitions

✓ Tool Execution Loop

✓ Evaluation Framework

✓ Build Log

✓ Detailed README

✓ Deployment

✓ Sponsorship Analysis

✓ Resume Analysis

✓ Grounding Sources

✓ Structured Reporting

---

# Limitations

Current limitations include:

* Sponsorship ratings are estimates
* No direct USCIS integration
* Search quality depends on Tavily results
* Some job boards restrict content access
* Resume parsing is basic

---

# Future Enhancements

Potential future improvements include:

* H-1B sponsor database integration
* Salary intelligence
* Resume tailoring agent
* Interview preparation agent
* Application tracking dashboard
* LinkedIn profile optimization
* Multi-agent collaboration
* Employer sponsorship history analysis


---

# Repository Structure

opt-career-intelligence-agent/

├── app.py

├── tools.py

├── requirements.txt

├── README.md

├── BUILD_LOG.md

├── evaluation/

│   ├── eval.py

│   ├── test_cases.json

│   └── results.json

└── .streamlit/

```
└── secrets.toml (local only)
```

---

# Conclusion

OPT Career Intelligence Agent demonstrates the complete set of concepts covered throughout the course:

* Prompt Engineering
* System Prompts
* Grounding
* MCP Tools
* Agentic Decision Making
* Evaluation
* Deployment
* Iteration

The final application provides real-world value to international students by helping them make more informed career decisions while navigating sponsorship challenges in the United States job market.
