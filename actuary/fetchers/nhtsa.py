import requests
from dataclasses import dataclass
import sys

@dataclass
class NHTSAResult:
    total_complaints: int
    most_common_issue: str
    severity_score: float

def fetch_nhtsa_data(make: str, model: str, year: int) -> NHTSAResult:
    url = f"https://api.nhtsa.gov/complaints/complaintsByVehicle?make={make}&model={model}&modelYear={year}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = data.get("results", [])
        total_complaints = len(results)
        
        # Calculate most common issue
        issues = {}
        for r in results:
            comp = r.get("components", "Unknown").split(",")[0]
            issues[comp] = issues.get(comp, 0) + 1
            
        most_common_issue = max(issues, key=issues.get) if issues else "None"
        
        # Calculate severity 0-100 (simple heuristic based on total complaints)
        # Assuming 1000+ complaints is max severity
        severity_score = min(total_complaints / 10.0, 100.0)
        
        return NHTSAResult(
            total_complaints=total_complaints,
            most_common_issue=most_common_issue,
            severity_score=severity_score
        )
    except requests.exceptions.RequestException as e:
        print(f"Error fetching NHTSA data: {e}", file=sys.stderr)
        # Return default/empty result in case of error
        return NHTSAResult(0, "Error", 0.0)

if __name__ == "__main__":
    result = fetch_nhtsa_data(make="Honda", model="Civic", year=2020)
    print(f"Honda Civic 2020 Results: {result}")
