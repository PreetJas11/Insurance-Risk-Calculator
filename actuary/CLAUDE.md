# Actuary Project Documentation

CLI insurance risk calculator.
Conventions:
- Python
- Type hints required
- Use `requests` and `pandas` only
- All risk scores should be normalized to a 0-100 scale

Data Sources:
1. NHTSA: https://api.nhtsa.gov/
2. CDC: https://data.cdc.gov/
3. US Census: https://api.census.gov/
4. FBI UCR (Placeholder): https://api.usa.gov/crime/

# Structure
```
actuary/
  ├── CLAUDE.md
  ├── fetchers/
  │   ├── __init__.py
  │   ├── nhtsa.py
  │   ├── cdc.py
  │   └── census.py
  ├── main.py
```
