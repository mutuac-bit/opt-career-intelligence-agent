import json
import time
import streamlit as st
from groq import Groq

from tools import (
    search_jobs,
    analyze_resume,
    check_sponsorship,
    TOOLS
)

st.set_page_config(
    page_title="OPT Career Intelligence Agent",
    layout="wide"
)

st.title("🎯 OPT Career Intelligence Agent")
st.caption("Agentic AI Career Advisor for F-1 STEM OPT Students — grounded in real USCIS H-1B data")

# ==========================
# API KEYS
# ==========================

groq_api_key = st.secrets["GROQ_API_KEY"]
tavily_api_key = st.secrets["TAVILY_API_KEY"]

client = Groq(api_key=groq_api_key)

# ==========================
# SIDEBAR
# ==========================

st.sidebar.header("👤 Student Profile")

visa_status = st.sidebar.selectbox(
    "Visa Status",
    ["F-1 STEM OPT", "F-1 OPT", "H-1B"]
)

years_experience = st.sidebar.slider("Years of Experience", 0, 10, 1)

skills = st.sidebar.text_area("Skills", "Python, SQL, Power BI, Machine Learning")

target_role = st.sidebar.text_input("Target Role", "Data Analyst")

target_city = st.sidebar.text_input("Target City", "Atlanta")

resume_file = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])

# ==========================
# PROFILE SUMMARY
# ==========================

st.subheader("📋 Profile Summary")
st.write(f"**Visa Status:** {visa_status}")
st.write(f"**Years Experience:** {years_experience}")
st.write(f"**Skills:** {skills}")
st.write(f"**Target Role:** {target_role}")
st.write(f"**Target City:** {target_city}")

# ==========================
# RUN AGENT
# ==========================

if st.button("🚀 Run Career Intelligence Agent"):

    with st.spinner("Running autonomous agent... searching jobs and checking real H-1B data..."):

        resume_text = analyze_resume(resume_file)

        system_prompt = f"""
You are OPT Career Intelligence Agent, an expert advisor for international students on F-1 OPT/STEM OPT seeking U.S. jobs with visa sponsorship.

STUDENT PROFILE (grounding):
- Visa Status: {visa_status}
- Years Experience: {years_experience}
- Skills: {skills}
- Target Role: {target_role}
- Target City: {target_city}
- Resume: {resume_text[:2000]}

YOUR REQUIRED WORKFLOW — follow every step:
1. Call search_jobs to find real job postings for the target role and city.
2. For EVERY company you find in the search results, you MUST call check_sponsorship with that company's name. This returns REAL USCIS H-1B approval data. Do not skip any company. Do not guess sponsorship — always call the tool.
3. After gathering all sponsorship data, produce a final report.

OUTPUT FORMAT — produce exactly this structure:

## 📊 Job Comparison Chart

Create a markdown table with these columns:
| Company | Role | Location | Fit Score (0-100) | H-1B Approvals (FY2026) | Approval Rate | Sponsorship Rating | Action |

For each job:
- Fit Score: score 0-100 based on how well the student's skills/experience match the role.
- H-1B Approvals + Approval Rate + Sponsorship Rating: use the REAL numbers returned by check_sponsorship. If a company returned 0 records, mark approvals as 0 and rating as RED.
- Action: "Apply Now" (GREEN + good fit), "Apply with Caution" (YELLOW), or "Skip" (RED or poor fit).

## 🎯 Top 3 Recommendations
List the 3 best jobs and one sentence why each.

## 📈 Strategy Summary
## 📈 Strategy Summary
Write 3-4 sentences of genuinely useful, respectful strategy for an international student on F-1 OPT/STEM OPT. This person is highly skilled, has invested enormously in their education, and legally requires employment that offers sponsorship to preserve their visa status — applying to non-sponsoring jobs is NOT an option for them.

RULES for the strategy:
- DO recommend prioritizing the proven sponsors found in the data (companies with real H-1B approval history).
- DO mention cap-exempt employers (universities, nonprofits, research institutions) as a path to H-1B outside the lottery.
- DO advise using their OPT/STEM OPT timeline strategically so an employer can initiate H-1B in time.
- DO encourage networking into sponsor companies rather than only cold-applying.
- DO affirm that their existing skills are strong assets.
- NEVER tell them to "update their skills," "gain more experience first," "apply to jobs that don't require sponsorship," or "switch careers." These are insensitive and unhelpful given their constraints.
- Be honest but encouraging. They have real options — point them to the good ones.
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Find sponsorship-friendly {target_role} jobs in {target_city} and check the real H-1B data for every company."}
        ]

        final_answer = ""
        tool_log = []

        try:
            for _ in range(8):

                response = None
                for attempt in range(4):
                    try:
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=messages,
                            tools=TOOLS
                        )
                        break
                    except Exception as api_err:
                        err_text = str(api_err)
                        if "rate_limit" in err_text or "429" in err_text:
                            wait_time = 20
                            st.info(f"⏳ Rate limit reached. Waiting {wait_time}s and retrying... (attempt {attempt + 1}/4)")
                            time.sleep(wait_time)
                        else:
                            raise
                if response is None:
                    st.error("Rate limit persisted after several retries. Please wait a minute and try again.")
                    st.stop()
                assistant_message = response.choices[0].message

                if assistant_message.tool_calls:

                    messages.append({
                        "role": "assistant",
                        "content": assistant_message.content or "",
                        "tool_calls": [tc.model_dump() for tc in assistant_message.tool_calls]
                    })

                    for tool_call in assistant_message.tool_calls:
                        function_name = tool_call.function.name
                        arguments = json.loads(tool_call.function.arguments)

                        if function_name == "search_jobs":
                            result = search_jobs(arguments["role"], arguments["city"], tavily_api_key)
                            tool_log.append(f"🔍 search_jobs({arguments['role']}, {arguments['city']})")

                        elif function_name == "check_sponsorship":
                            result = check_sponsorship(arguments["company_name"])
                            tool_log.append(f"🏢 check_sponsorship({arguments['company_name']}) → {result.get('rating')}")

                        elif function_name == "analyze_resume":
                            result = analyze_resume(resume_file)
                            tool_log.append("📄 analyze_resume()")

                        else:
                            result = {"error": "Unknown tool"}

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result)
                        })

                else:
                    final_answer = assistant_message.content
                    break

            st.success("✅ Analysis Complete")

            st.subheader("🤖 Career Intelligence Report")
            st.markdown(final_answer)

            with st.expander("🔧 Agent Tool Calls (proof of agentic execution)"):
                for entry in tool_log:
                    st.write(entry)

        except Exception as e:
            st.error(f"Error: {str(e)}")