from tavily import TavilyClient
from pypdf import PdfReader


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
            "content": item.get("content", "")
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

    company_name = company_name.lower()

    known_sponsors = [
        "amazon",
        "microsoft",
        "google",
        "meta",
        "apple",
        "deloitte",
        "accenture",
        "ibm",
        "oracle",
        "intel",
        "salesforce"
    ]

    if any(
        sponsor in company_name
        for sponsor in known_sponsors
    ):
        return {
            "company": company_name,
            "rating": "GREEN",
            "reason": "Known large employer with sponsorship history."
        }

    return {
        "company": company_name,
        "rating": "YELLOW",
        "reason": "No strong sponsorship evidence found."
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
                    "role": {
                        "type": "string"
                    },
                    "city": {
                        "type": "string"
                    }
                },
                "required": [
                    "role",
                    "city"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_resume",
            "description": "Read uploaded resume PDF.",
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
            "description": "Check sponsorship likelihood.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string"
                    }
                },
                "required": [
                    "company_name"
                ]
            }
        }
    }
]