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

# Build Log — OPT Career Intelligence Agent

This is the real story of how this project evolved, what broke, and how I fixed it.

## Why I built this
I'm an international student on F-1 STEM OPT. The single most exhausting part of my job search is not finding jobs, it's not knowing which employers will actually sponsor a visa. I have wasted applications on companies that were never going to sponsor. I built this tool because I needed it myself.

## Why these tools

**Why Tavily for search:** I needed live job postings, not the model's stale training data. Tavily returns real current listings with a simple API and a free tier, and it lets the agent search any role/city combination on demand. I chose it over scraping job boards directly because scraping breaks constantly and many boards block it.

**Why I moved off OpenAI to Groq:** My first working version used GPT-4.1-mini. It worked, but I didn't want the project to depend on a paid key, and I realized the model is the most replaceable part of the system, the real value is the data and the workflow. Groq runs Llama 3.3 70B for free and supports the same OpenAI-style tool calling, so the agent loop didn't have to change much. This gave me insight on what API I can use for large-scale production.

**Why Llama 3.3 70B specifically:** I first tried the smaller 8B model to save tokens when I hit rate limits. It was noticeably worse, it started labeling companies "Company A / Company B" instead of extracting real names. I switched back to 70B because accuracy of company extraction is the whole point.

## The biggest change: real sponsorship data
My draft used a hardcoded list of ~11 "known sponsor" companies for check_sponsorship. My instructor correctly flagged this as a mock, not a real tool — if you replaced it with a lookup table, nothing would change.

So I replaced it with the **real USCIS H-1B Employer Data Hub dataset (FY2026)** — 36,631 real employers with actual approval and denial counts. Now when the agent checks "Amazon," it gets 4,102 real approvals and a 98.1% approval rate from government data, not my guess. This single change fixed three things at once: it made the tool real, made my grounding real, and made my evaluation honest.

## What broke along the way (the honest part)
- **CrewAI wouldn't install** on Python 3.14 in an earlier version of this project. I stopped fighting the framework and built the agent loop manually. Lesson: frameworks aren't worth it when they fight your environment.
- **A PostgreSQL SSL certificate** on my machine kept breaking every HTTPS call (`Could not find a suitable TLS CA certificate bundle`). I fixed it by pointing SSL_CERT_FILE and REQUESTS_CA_BUNDLE at the correct certifi bundle.
- **Groq rate limits (12k tokens/min)** kept crashing the app on repeated runs. I added an automatic wait-and-retry so the user sees a friendly "retrying" message instead of a red error.
- **Uploading a resume made results worse, not better.** This surprised me. The raw resume text was eating my token budget every loop, starving the actual job analysis. It's beneficial to know that more information does not mean that you will achieve higher accuracy. Rather, it could mean that it eats up a lot of your tokens then come up with inaccurate results cause they were already maxxed before it can give you good analysis.

## How I evaluated it
I threw out my old evaluation. It scored 100%, but only because it tested the hardcoded list against itself — meaningless. I wrote a new evaluation (evaluation/eval_real.py) testing 10 real companies against known sponsorship reality. It scored **80% (8/10)**, and the two "failures" were actually the real data correcting my assumptions — Dice (a job board) genuinely files H-1Bs, which I hadn't expected. I'd rather show an honest 80% with real failures than a fake 100%.

## What I'd fix with more time
Filter out job-board aggregators so the agent surfaces direct employers; handle companies that file under different legal names (Coca-Cola problem); move the CSV into a database with quarterly auto-refresh; add salary data from DOL LCA filings