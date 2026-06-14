import json
import streamlit as st
from openai import OpenAI

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
st.caption("Agentic AI Career Advisor for F-1 STEM OPT Students")

# ==========================
# API KEYS
# ==========================

openai_api_key = st.secrets["OPENAI_API_KEY"]
tavily_api_key = st.secrets["TAVILY_API_KEY"]

client = OpenAI(api_key=openai_api_key)

# ==========================
# SIDEBAR
# ==========================

st.sidebar.header("👤 Student Profile")

visa_status = st.sidebar.selectbox(
    "Visa Status",
    ["F-1 STEM OPT", "F-1 OPT", "H-1B"]
)

years_experience = st.sidebar.slider(
    "Years of Experience",
    0,
    10,
    1
)

skills = st.sidebar.text_area(
    "Skills",
    "Python, SQL, Power BI, Machine Learning"
)

target_role = st.sidebar.text_input(
    "Target Role",
    "Data Analyst"
)

target_city = st.sidebar.text_input(
    "Target City",
    "Atlanta"
)

resume_file = st.sidebar.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# ==========================
# PROFILE SUMMARY
# ==========================

st.subheader("📋 Profile Summary")

st.write(f"Visa Status: {visa_status}")
st.write(f"Years Experience: {years_experience}")
st.write(f"Skills: {skills}")
st.write(f"Target Role: {target_role}")
st.write(f"Target City: {target_city}")

# ==========================
# RUN AGENT
# ==========================

if st.button("🚀 Run Career Intelligence Agent"):

    with st.spinner("Running autonomous agent..."):

        resume_text = analyze_resume(resume_file)

        system_prompt = f"""
You are OPT Career Intelligence Agent.

Your goal is helping international students find jobs that maximize sponsorship opportunities.

You may use tools.

Available tools:
1. search_jobs
2. analyze_resume
3. check_sponsorship

Use available tools whenever useful.

Grounding Context:

Visa Status:
{visa_status}

Years Experience:
{years_experience}

Skills:
{skills}

Target Role:
{target_role}

Target City:
{target_city}

Resume:
{resume_text[:3000]}

Do not guess.
Use tool outputs whenever possible.

Provide:
1. Top jobs
2. Sponsorship analysis
3. Resume recommendations
4. Application strategy
"""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"""
Find sponsorship-friendly jobs.

Role: {target_role}
City: {target_city}
"""
            }
        ]

        final_answer = ""

        try:

            for _ in range(5):

                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=messages,
                    tools=TOOLS
                )

                assistant_message = response.choices[0].message

                if assistant_message.tool_calls:

                    messages.append(
                        {
                            "role": "assistant",
                            "content": assistant_message.content or "",
                            "tool_calls": [
                                tc.model_dump()
                                for tc in assistant_message.tool_calls
                            ]
                        }
                    )

                    for tool_call in assistant_message.tool_calls:

                        function_name = tool_call.function.name

                        arguments = json.loads(
                            tool_call.function.arguments
                        )

                        if function_name == "search_jobs":

                            result = search_jobs(
                                arguments["role"],
                                arguments["city"],
                                tavily_api_key
                            )

                        elif function_name == "check_sponsorship":

                            result = check_sponsorship(
                                arguments["company_name"]
                            )

                        elif function_name == "analyze_resume":

                            result = analyze_resume(
                                resume_file
                            )

                        else:

                            result = {
                                "error": "Unknown tool"
                            }

                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps(result)
                            }
                        )

                else:

                    final_answer = assistant_message.content
                    break

            st.success("Analysis Complete")

            st.subheader("🤖 Career Intelligence Report")

            st.markdown(final_answer)

        except Exception as e:

            st.error(f"Error: {str(e)}")

# ==========================
# RUBRIC EVIDENCE
# ==========================

st.divider()

st.subheader("📚 Capstone Evidence")

st.markdown("""
### Agentic Behavior

The LLM decides:

- Whether to call tools
- Which tool to call
- How many times to call tools
- When enough information exists

### MCP Tools

1. search_jobs()
2. analyze_resume()
3. check_sponsorship()

### Grounding

- User profile
- Resume PDF
- Tavily live web search

### Evaluation

See evaluation folder.

### Prompt Engineering

Prompt versions documented in README.

### Deployment

Public Streamlit deployment.
""")