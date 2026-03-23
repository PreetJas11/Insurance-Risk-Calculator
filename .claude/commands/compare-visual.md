---
description: Visually compare two vehicles
argument-hint: "[make1-model1] [make2-model2]"
allowed-tools: [Read, Bash, Write]
---

You are an expert automotive actuary AI.
The user provided these arguments:
$ARGUMENTS

Please follow these steps exactly:
1. Extract the vehicle pairs from the arguments, format: "[make1-model1] [make2-model2]".
2. Call the NHTSA fetcher (`python -m actuary.main --type auto ...`) for BOTH vehicles to get complaint rates, issues, and severity.
3. Compare the complaint count, severity score, and implicit risk factors.
4. Call `python actuary/diagram.py` (or use the Excalidraw MCP native tools) to generate a diagram showing:
   - Two columns, one per vehicle
   - Side by side bars for: complaint_rate, severity_score, recall_count
   - A winner banner at the bottom highlighting the lower-risk vehicle in green.
5. Output the text comparison and at the very bottom print:
   "📊 Visual breakdown: <URL>"
