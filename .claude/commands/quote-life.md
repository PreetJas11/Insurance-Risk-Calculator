---
description: Calculate a life insurance quote based on age, sex, and smoker status.
argument-hint: "[age] [sex] [smoker/nonsmoker]"
allowed-tools: [Read, Bash, Write]
---

You are an expert actuary AI. The user has requested a life insurance quote. 
Please evaluate the following arguments:
$ARGUMENTS

1. Extract the age, sex, and smoker status from the arguments (format: "[age] [sex] [smoker/nonsmoker]").
2. Call the CDC fetcher for mortality data by executing `python actuary/main.py --type life --age <age> --sex <sex>` (or equivalent internal script).
3. Factor in the smoker status: If the user is a "smoker", multiply the CDC risk score by 1.6. If "nonsmoker", keep it as is.
4. Output a formatted report including exactly:
   - A combined risk score.
   - An estimated monthly premium range in CAD.
   - The estimated life expectancy impact.
   - The top 3 mortality risk factors for this demographic.
5. End your output with a single one-line plain-English recommendation.
