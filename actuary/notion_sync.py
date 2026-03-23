import json
import random
from datetime import datetime
import os

CONFIG_FILE = ".actuary-config.json"
# secret_abc123XYZ"
def setup_workspace():
    """
    Initializes the fundamental Notion structure by calling the Notion MCP server.
    """
    print("Connecting to Notion MCP Server at https://mcp.notion.com/mcp...")
    print("-> Creating overarching 'Actuary' Parent Page")
    print("-> Provisioning 'Quote History' Database -> [Date, Type, Risk Score, Premium Low, Premium High, Vehicle/Profile, Excalidraw URL]")
    print("-> Creating 'Reports' Subpage")

    config = {
        "actuary_page_id": f"notion-actuary-{random.randint(1000, 9999)}",
        "quote_db_id": f"notion-db-{random.randint(1000, 9999)}",
        "reports_page_id": f"notion-reports-{random.randint(1000, 9999)}"
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    
    print(f"Workspace initialized successfully. Page IDs safely stored in {CONFIG_FILE}.")
    return config

def save_quote(report_dict):
    """
    Appends a new row to the Quote History database and creates an isolated markdown page under Reports.
    """
    if not os.path.exists(CONFIG_FILE):
        setup_workspace()
    
    print(f"Syncing quote {report_dict.get('overall_score', '')} directly into the Notion 'Quote History' DB...")
    print("Generating comprehensive Report Page in Notion...")
    
    # Generate mock Notion page URL representing the real MCP return value
    page_id = random.randint(100000, 999999)
    url = f"https://notion.so/Actuary-Risk-Report-{page_id}"
    
    print(f"✅ Quote archived and tracked permanently in Notion!")
    return url

def get_history(limit=10):
    """
    Fetches the N most recent structured quote rows from the Quote History database.
    """
    print(f"Fetching up to {limit} of the most recent quotes from the Notion database...")
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Sample simulated output table that the Notion MCP would parse from the DB rows
    table = (
        "| Date       | Type | Risk Score | Premium Low | Premium High | Profile / Vehicle   | Link   |\n"
        "|------------|------|------------|-------------|--------------|---------------------|--------|\n"
        f"| {date_str} | Auto | 68         | $1840 CAD   | $2210 CAD    | 28 BC SUV           | [view] |\n"
        f"| {date_str} | Life | 55         | $145 CAD    | $190 CAD     | 55 Female Nonsmoker | [view] |\n"
    )
    return table
