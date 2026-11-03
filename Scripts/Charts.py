import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("charts",exist_ok=True)

cust = pd.read_excel("aml_output.xlsx", sheet_name="Customer_Risk")
alerts = pd.read_excel("aml_output.xlsx", sheet_name="Alerts")
txns = pd.read_excel("aml_output.xlsx", sheet_name="Transactions")

# Chart 1: customers by risk level
order = ["Low", "Medium", "High"]
counts = cust["risk_level"].value_counts().reindex(order).fillna(0)
ax = counts.plot(kind="bar", color=["#00FF08", "#FFBF01", "#FC0703"])
ax.set_title("Customers by Risk Level")
ax.set_xlabel("")
ax.set_ylabel("Number of Transactions")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/risk_levels.png", dpi=150)
plt.clf()

# Chart 2: alerts by reason
alerts["alert_reason"].value_counts().plot(kind="barh", color="#087DE4")
plt.title("Alerts by Reason")
plt.xlabel("Number of alerts")
plt.tight_layout()
plt.savefig("charts/alerts_by_reason.png", dpi=150)
plt.clf()

# Chart 3: alerts per month
alerts["month"] = pd.to_datetime(alerts["txn_date"]).dt.strftime("%Y-%m")
alerts["month"].value_counts().sort_index().plot(kind="line", marker="o")
plt.title("Alerts per Month")
plt.savefig("chart_monthly.png")
plt.close()

# Chart 4: transaction amounts
plt.hist(txns["amount_aed"].clip(upper=100000), bins=50)
plt.axvline(55000, color="red", linestyle="--")
plt.title("Transaction Amounts (red line = 55,000 AED limit)")
plt.savefig("chart_amounts.png")
plt.close()

import pandas as pd

x = "aml_output.xlsx"
pd.read_excel(x, sheet_name="Customer_Risk").to_csv("customer_risk.csv", index=False)
pd.read_excel(x, sheet_name="Alerts").to_csv("alerts.csv", index=False)
print("Done")