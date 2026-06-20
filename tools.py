import os
import pandas as pd
from tavily import TavilyClient
from pypdf import PdfReader

# ==========================
# H-1B SPONSORSHIP DATA (real USCIS FY2026 Employer Data Hub)
# Loaded once at module level so lookups are fast.
# File is UTF-16, tab-separated — these settings are required.
# ==========================

_H1B_PATH = os.path.join(os.path.dirname(__file__), "h1b_employer_data.csv")

_APPROVAL_COLS = [
    "New Employment Approval",
    "Continuation Approval",
    "Change with Same Employer Approval",
    "New Concurrent Approval",
    "Change of Employer Approval",
    "Amended Approval",
]
_DENIAL_COLS = [
    "New Employment Denial",
    "Continuation Denial",
    "Change with Same Employer Denial",
    "New Concurrent Denial",
    "Change of Employer Denial",
    "Amended Denial",
]


def _load_h1b_data():
    df = pd.read_csv(_H1B_PATH, sep="\t", encoding="utf-16", low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    for col in _APPROVAL_COLS + _DENIAL_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df


_H1B_DF = _load_h1b_data()
_EMP_COL = "Employer (Petitioner) Name"


def search_jobs(role, city, tavily_api_key):
    client = TavilyClient(api_key=tavily_api_key)
    query = f"{role} jobs in {city} sponsorship"
    result = client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )
    jobs = []
    for item in result.get("results", []):
        jobs.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", "")[:300]
        })
    return jobs


def analyze_resume(pdf_file):
    if pdf_file is None:
        return "No resume uploaded."
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text[:10000]


def check_sponsorship(company_name):
    """
    Look up a company's REAL H-1B petition history in the USCIS
    FY2026 Employer Data Hub. Returns actual approval/denial counts.
    This is grounded government data, not an estimate.
    """
    query = str(company_name).strip().upper()

    if not query:
        return {
            "company": company_name,
            "rating": "RED",
            "reason": "No company name provided."
        }

    hits = _H1B_DF[
        _H1B_DF[_EMP_COL].astype(str).str.upper().str.contains(
            query, na=False, regex=False
        )
    ]

    if len(hits) == 0:
        return {
            "company": company_name,
            "rating": "RED",
            "total_approvals": 0,
            "total_denials": 0,
            "reason": "No H-1B petition records found in USCIS FY2026 data. "
                      "This company likely does not sponsor, or files under a different legal name."
        }

    approvals = int(hits[_APPROVAL_COLS].sum().sum())
    denials = int(hits[_DENIAL_COLS].sum().sum())
    total = approvals + denials
    approval_rate = round(approvals / total * 100, 1) if total > 0 else 0.0

    if approvals >= 10:
        rating = "GREEN"
        reason = f"Strong sponsor: {approvals} H-1B approvals in FY2026."
    elif approvals >= 1:
        rating = "YELLOW"
        reason = f"Limited sponsor: only {approvals} H-1B approval(s) in FY2026."
    else:
        rating = "RED"
        reason = "Records exist but no approvals in FY2026."

    return {
        "company": company_name,
        "rating": rating,
        "total_approvals": approvals,
        "total_denials": denials,
        "approval_rate": approval_rate,
        "matched_entities": int(len(hits)),
        "data_source": "USCIS H-1B Employer Data Hub FY2026",
        "reason": reason
    }


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_jobs",
            "description": "Search live job postings using Tavily.",
            "parameters": {
                "type": "object",
                "properties": {
                    "role": {"type": "string"},
                    "city": {"type": "string"}
                },
                "required": ["role", "city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_resume",
            "description": "Read the uploaded resume PDF. Takes no arguments.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_sponsorship",
            "description": "Look up a company's real H-1B petition history (approvals, denials, approval rate) from USCIS FY2026 government data. Use this to verify whether an employer actually sponsors visas.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {"type": "string"}
                },
                "required": ["company_name"]
            }
        }
    }
]