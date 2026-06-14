# BUILD LOG

## Project

OPT Career Intelligence Agent

Author: Cynthia

Capstone Project

---

# Week 1

## Initial Idea

The original concept was a job search assistant for international students.

Goal:

Help F-1 STEM OPT students identify jobs likely to support long-term sponsorship.

---

## First Prototype

Built a basic job search workflow.

Process:

Search Jobs

↓

Analyze Results

↓

Provide Recommendations

Problem:

The workflow behaved like a fixed pipeline and did not demonstrate true agentic behavior.

---

# Week 2

## Sponsorship Analysis

Added sponsorship screening logic.

Purpose:

Provide a sponsorship likelihood rating for employers.

Output:

GREEN

YELLOW

RED

Problem:

Many employers do not explicitly mention sponsorship in job postings.

Result:

The system required additional context and grounding.

---

# Week 3

## Grounding Improvements

Added:

* User profile grounding
* Resume grounding
* Live search grounding

Sources:

* Resume PDF
* Tavily Search
* User profile data

Improvement:

Recommendations became more personalized and relevant.

---

## Prompt Iteration

### Prompt Version 1

Search for jobs matching the target role.

Issue:

Returned jobs that were not relevant to the user's background.

---

### Prompt Version 2

Search only for jobs that:

* Match role
* Match location
* Consider sponsorship
* Consider resume skills
* Use available grounding

Result:

Higher quality recommendations.

---

# Week 4

## Agentic Architecture

Instructor feedback emphasized that a fixed pipeline is not the same as an agent.

Problem:

The original architecture executed the same sequence every time.

Search

↓

Analyze

↓

Score

This limited autonomous behavior.

---

## Solution

Implemented a tool-calling architecture using GPT-4.1-mini.

The model can:

* Decide whether to call a tool
* Decide which tool to call
* Decide when to stop

This moved decision-making into the model rather than Python control flow.

---

# MCP Tool Development

Implemented MCP-style tools.

Tool 1

search_jobs()

Purpose:

Retrieve live job postings.

---

Tool 2

analyze_resume()

Purpose:

Read uploaded PDF resumes.

---

Tool 3

check_sponsorship()

Purpose:

Analyze sponsorship likelihood.

---

# Evaluation Development

Created:

evaluation/test_cases.json

evaluation/eval.py

Measured:

* Sponsorship classification accuracy
* Pass rate

Results:

Accuracy = 100%

Test Cases = 10

Passed = 10

---

# Challenges Encountered

## Challenge 1

Job search results often contained aggregator pages.

Mitigation:

Improved search prompts and filtering.

---

## Challenge 2

Resume content extraction produced noisy text.

Mitigation:

Truncated and cleaned extracted text.

---

## Challenge 3

Need for stronger agentic behavior.

Mitigation:

Added OpenAI tool-calling loop and autonomous decision making.

---

# Final Capstone Improvements

Compared with earlier versions:

Added:

✓ MCP tools

✓ Tool execution loop

✓ Autonomous decision making

✓ Resume grounding

✓ Evaluation framework

✓ Build log

✓ Detailed documentation

✓ Public deployment support

---

# Future Improvements

* Real USCIS sponsorship database
* Salary intelligence API
* Application tracker
* Resume tailoring agent
* Multi-agent collaboration

---

# Reflection

This project evolved from a simple job search assistant into an autonomous career intelligence system.

The most important lesson was understanding the difference between:

Pipeline Logic

and

Agentic Decision Making

Moving tool selection and execution decisions into the model created a more flexible and intelligent system while satisfying the requirements of the capstone project.
