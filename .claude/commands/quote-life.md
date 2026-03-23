---
description: Calculate a life insurance quote based on age, sex, and smoker status.
argument-hint: "[age] [sex] [smoker/nonsmoker]"
allowed-tools: [Read, Bash, Write]
---

You are an expert actuary AI. The user has requested a life insurance quote. 
Please evaluate the following arguments:
$ARGUMENTS

1. Extract the age, sex, and smoker status from the arguments (format: "[age] [sex] [smoker/nonsmoker]").
2. Call the CDC fetcher for mortality data by executing `python -m actuary.main --type life --age <age> --sex <sex>`.
3. Factor in the smoker status: If the user is a "smoker", multiply the CDC risk score by 1.6. If "nonsmoker", keep it as is.
4. Output a formatted report including exactly:
   - A combined risk score.
   - An estimated monthly premium range in CAD.
   - The estimated life expectancy impact.
   - The top 3 mortality risk factors for this demographic.
5. Call `python actuary/diagram.py` (with mortality_risk, lifestyle_risk, age_risk, and a life_expectancy field) to generate the visual report.
6. Print the returned Excalidraw URL at the bottom labeled exactly:
   "📊 Visual breakdown: <URL>"
7. Call `python -c "import sys; sys.path.append('.'); from actuary.notion_sync import save_quote; print(save_quote({'overall_score': <risk>}))"` to log the report to Notion.
8. Print the returned Notion page URL at the very bottom labeled exactly:
   "📝 Saved to Notion: <URL>"
