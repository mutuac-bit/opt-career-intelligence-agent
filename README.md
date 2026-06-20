# OPT Career Intelligence Agent

An agentic AI tool that helps international students on F-1 OPT/STEM OPT find jobs that will actually sponsor their visa — grounded in real USCIS H-1B government data.

**Live app:** https://opt-career-intelligence-agent.streamlit.app/

## What it does

You enter your profile (visa status, skills, experience, target role and city) and optionally upload your resume. An autonomous agent then:
1. Searches live job postings for your role and city
2. Looks up each company's **real H-1B petition history** from USCIS FY2026 data
3. Scores each job for fit against your profile
4. Returns a comparison table ranking jobs by fit and real sponsorship likelihood, plus a personalized strategy

## Who it's for

International students on F-1 OPT/STEM OPT who waste time applying to companies that will never sponsor them. This matters to me because it made my job search experience brutal, and I want to make this experience seamless for students and professionals like us.

## System architecture

- **Model:** Llama 3.3 70B (via Groq) — drives all decisions and tool calls
- **Search tool:** Tavily API — live job postings
- **Sponsorship tool:** local lookup against real USCIS H-1B Employer Data Hub (FY2026, 36,631 employers)
- **Resume tool:** PDF text extraction via pypdf
- **Frontend/deploy:** Streamlit + Streamlit Community Cloud

The agent runs an OpenAI-style tool-calling loop. The model — not hardcoded Python — decides which tools to call, when, and how many times.

## What's agentic about it

The model receives the user request and autonomously decides to call `search_jobs`, then decides to call `check_sponsorship` for each company it finds, reads the results, and decides when it has enough to write the final report. The execution loop in `app.py` provides the tools; the model is in the driver's seat. If you replaced the model with if-statements, the system could not adapt its tool use to different searches — so this passes the agentic test.

## The three tools (MCP)

**search_jobs(role, city)** — queries Tavily for live postings. Returns titles, URLs, and snippets the model could not know from training.

**check_sponsorship(company_name)** — looks up a company in the real USCIS H-1B dataset and returns actual approval counts, denial counts, and approval rate. This is grounded government data, not an estimate.

**analyze_resume()** — extracts text from the uploaded PDF so recommendations are personalized.

## Grounding

The model is grounded by three real sources it could never get from pretraining: the user's profile, their uploaded resume, live Tavily job search, and — most importantly — the real USCIS H-1B petition dataset bundled in this repo.

## Prompt engineering (three versions)

**v1:** "Find jobs matching the user's role." → Too generic, no sponsorship focus.

**v2:** Added sponsorship focus, visa awareness, and profile grounding. → Better matching, but the agent often skipped the sponsorship tool and guessed.

**v3 (final):** Added a required workflow that forces the agent to call check_sponsorship for every company, plus a strict comparison-table output format. → The agent now reliably uses real data for every company and produces a scannable report.

## Evaluation (honest)

I tested `check_sponsorship` against 10 real companies with known sponsorship reality (`evaluation/eval_real.py`).

**Result: 8/10 (80%) accuracy.**

The two misses were informative, not hidden failures:
- **Dice** — I expected RED (it's a job board) but it correctly returned GREEN; the company genuinely files H-1Bs.
- **Coca-Cola** — returned YELLOW instead of RED because it files under multiple legal entity names, a known limitation of name-based lookup.

I deliberately kept this at an honest 80% rather than engineering a fake 100%. Real companies like Amazon (4,102 approvals), Microsoft (2,273), and Deloitte (1,359) all classified correctly with real numbers.

## What changed from my draft

My draft's `check_sponsorship` was a hardcoded list of 11 companies — a mock, not a real tool, and my instructor flagged it. I replaced it with the real USCIS dataset, rewrote the evaluation to be honest, switched from paid OpenAI to free Groq, added a comparison-table output, and added rate-limit retry handling. I also committed incrementally this time so the history shows real development. Full details in BUILD_LOG.md.

## Limitations / what I'd fix with more time

- The agent's sponsorship accuracy depends on the job search returning real employer names rather than job-board aggregators (Dice, OPTnation).
- Companies filing under different legal names (the Coca-Cola problem) can be missed by name lookup.
- The dataset is a quarterly snapshot, not real-time (which is fine for sponsorship history, but worth noting).

## How to run it yourself

1. Clone this repo
2. `pip install -r requirements.txt`
3. Create `.streamlit/secrets.toml` with:
GROQ_API_KEY = "your-key"
TAVILY_API_KEY = "your-key" 
4. `streamlit run app.py`

## Example interaction

Input: Data Analyst, New York, F-1 STEM OPT.
The agent searched live postings, checked each company against USCIS data, and returned a table where Capital One (534 H-1B approvals, 99.3% approval rate) was rated GREEN / Apply Now, while job-board results with no petition history were rated RED / Skip.