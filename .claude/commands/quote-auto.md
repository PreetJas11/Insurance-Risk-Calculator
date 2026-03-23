---
description: Generate an auto insurance quote combining CDC mortality risk and NHTSA vehicle risk
argument-hint: "[age] [province/state] [vehicle-type]"
allowed-tools: [Read, Bash, Write]
---

You are an expert actuary AI. Your task is to generate a comprehensive auto insurance quote based on the user's provided arguments. 

The user has provided the following inputs:
$ARGUMENTS

Please follow these steps exactly:
1. Extract the **age**, **location (province/state)**, and **vehicle type** from the arguments (format: "[age] [province/state] [vehicle-type]").
2. Call the NHTSA fetcher script (`python -m actuary.main --type auto ...`) to retrieve vehicle risk data. 
3. Call the CDC fetcher script (`python -m actuary.main --type life ...`) to retrieve mortality/age.
4. Combine the insights from both sources into a formatted auto insurance risk report.
5. In the final report, you MUST display:
   - A combined **risk score (0-100)**.
   - An **estimated annual premium range in CAD**.
   - The **top 3 risk factors** specific to this profile.
6. Call `python actuary/diagram.py '{"overall_score": 68, "age_risk": 50, "vehicle_risk": 60, "location_risk": 40, "premium_low": 1840, "premium_high": 2210}'` (injecting real calculated data) to generate the Excalidraw visual diagram.
7. Print the returned Excalidraw URL at the bottom labeled exactly:
   "📊 Visual breakdown: <URL>"
8. Call `python -c "import sys; sys.path.append('.'); from actuary.notion_sync import save_quote; print(save_quote({'overall_score': 68}))"` (inject real calculated quote data instead of 68) to push the report to Notion.
9. Print the returned Notion page URL at the very bottom strictly labeled exactly:
   "📝 Saved to Notion: <URL>"
