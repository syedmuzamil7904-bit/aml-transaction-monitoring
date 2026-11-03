# aml-transaction-monitoring
Rule-based AML transaction monitoring with Python, Fabric and Power BI
# AML transaction monitoring

A rule-based anti-money-laundering (AML) monitoring project. It generates synthetic banking data, flags suspicious transactions with risk rules, scores customers, and shows the results in a Power BI dashboard.

## Tools used
Python (pandas, Faker, matplotlib), Microsoft Fabric Lakehouse, Power BI

## What it does
1. Generates 500 customers and about 20,000 transactions (synthetic data, no real people)
2. Applies three risk rules:
   - Large cash deposit (20,000 AED or more)
   - Structuring: 3 or more cash deposits just under the 55,000 AED reporting limit
   - Transfers to high-risk countries
3. Scores every customer as Low, Medium or High risk
4. Creates an alerts table for analyst review
5. Loads the data into Fabric and visualizes it in Power BI

## Key findings
- 15 customers were flagged as High risk
- The structuring pattern shows as a cluster of deposits just below the reporting limit
- Alerts rise sharply in the most recent two months

## How to run
1. Install the libraries: pip install pandas faker numpy openpyxl matplotlib
2. Run scripts/generate_data.py
3. Run scripts/risk_rules.py
4. Run scripts/simple_charts.py

## Next steps
- Add a Power Apps review app for analysts
- Try the project with the public IBM AML dataset

## Author
Syed Muzamil | https://www.linkedin.com/in/syed-muzamil-5069a0215/
