import argparse
import sys
# from actuary.fetchers.nhtsa import fetch_nhtsa_data
# from fetchers.cdc import fetch_cdc_data

from actuary.fetchers.nhtsa import fetch_nhtsa_data
from actuary.fetchers.cdc import fetch_cdc_data


def print_summary(risk_type, data_dict):
    print(f"\n{'='*40}")
    print(f"INSURANCE RISK SUMMARY: {risk_type.upper()}")
    print(f"{'='*40}")
    for key, value in data_dict.items():
        print(f"{key:<25}: {value}")
    print(f"{'='*40}\n")

def main():
    parser = argparse.ArgumentParser(description="Insurance Risk Calculator CLI")
    parser.add_argument("--type", choices=["auto", "life"], required=True, help="Type of risk to calculate")
    parser.add_argument("--age", type=int, help="Age of the individual (for life risk)")
    parser.add_argument("--vehicle-make", type=str, help="Make of the vehicle (for auto risk)")
    parser.add_argument("--vehicle-model", type=str, help="Model of the vehicle (for auto risk)")
    parser.add_argument("--sex", type=str, choices=["male", "female"], default="male", help="Sex of the individual (default: male)")
    
    args = parser.parse_args()
    
    if args.type == "auto":
        if not args.vehicle_make or not args.vehicle_model:
            print("Error: --vehicle-make and --vehicle-model are required for auto risk.")
            sys.exit(1)
            
        print(f"Fetching NHTSA data for {args.vehicle_make} {args.vehicle_model}...")
        # Since year wasn't specified in requirements, defaulting to 2020
        result = fetch_nhtsa_data(make=args.vehicle_make, model=args.vehicle_model, year=2020)
        
        summary = {
            "Vehicle": f"{args.vehicle_make} {args.vehicle_model}",
            "Total Complaints": result.total_complaints,
            "Most Common Issue": result.most_common_issue,
            "Severity Score (0-100)": f"{result.severity_score:.1f}"
        }
        print_summary("Auto", summary)
        
    elif args.type == "life":
        if not args.age:
            print("Error: --age is required for life risk.")
            sys.exit(1)
            
        print(f"Fetching CDC Wonder mortality data for age {args.age}...")
        result = fetch_cdc_data(age=args.age, sex=args.sex)
        
        summary = {
            "Individual": f"Age {args.age}, {args.sex.title()}",
            "Mortality Rate": result.mortality_rate,
            "Life Expectancy": f"{result.life_expectancy} years",
            "Risk Percentile (0-100)": f"{result.risk_percentile:.1f}"
        }
        print_summary("Life", summary)

if __name__ == "__main__":
    main()
