---
description: Compare NHTSA risk data of two vehicles
argument-hint: "[make1-model1] [make2-model2]"
allowed-tools: [Read, Bash, Write]
---

You are an expert automotive actuary AI. The user has requested to compare two vehicles. 
Please evaluate the following arguments:
$ARGUMENTS

1. Extract the two vehicles from the arguments (format: "[make1-model1] [make2-model2]").
2. Fetch NHTSA data for both vehicles by calling `python actuary/main.py --type auto ...` (or equivalent internal script) for each vehicle.
3. Compare the following metrics for both vehicles:
   - Complaint count
   - Severity score
   - Most common issues
4. Output a side-by-side comparison table displaying these metrics.
5. Declare a clear winner (the one with the lowest risk) and provide a one-line justification.
