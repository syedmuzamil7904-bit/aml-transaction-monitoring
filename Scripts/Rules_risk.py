import pandas as pd

customers = pd.read_csv("customers.csv")
txns = pd.read_csv("transactions.csv", parse_dates=["txn_date"])

# ---- Settings (easy to explain in your blog post) ----
LARGE_CASH = 20000        # AED, large cash deposit
NEAR_LIMIT_LOW = 50000    # just under the reporting limit
REPORT_LIMIT = 55000      # AED reporting threshold
high_risk = ["Iran", "North Korea", "Syria", "Myanmar", "Yemen"]

# ---- Rule 1: large cash deposit ----
is_cash_deposit = txns["txn_type"] == "Cash Deposit"
txns["flag_large_cash"] = is_cash_deposit & (txns["amount_aed"] >= LARGE_CASH)

# ---- Rule 2: structuring (3+ deposits just under the limit) ----
near_limit = is_cash_deposit & txns["amount_aed"].between(
    NEAR_LIMIT_LOW, REPORT_LIMIT - 0.01)
txns["near_limit"] = near_limit
near_counts = txns.groupby("customer_id")["near_limit"].sum()
structurers = near_counts[near_counts >= 3].index
txns["flag_structuring"] = near_limit & txns["customer_id"].isin(structurers)

# ---- Rule 3: high-risk destination country ----
txns["flag_high_risk_country"] = txns["destination_country"].isin(high_risk)

# ---- Points per transaction ----
txns["risk_points"] = (
    txns["flag_large_cash"] * 20
    + txns["flag_structuring"] * 40
    + txns["flag_high_risk_country"] * 30
)

# ---- Customer risk score ----
cust_risk = txns.groupby("customer_id").agg(
    total_txns=("txn_id", "count"),
    total_amount_aed=("amount_aed", "sum"),
    flagged_txns=("risk_points", lambda s: (s > 0).sum()),
    risk_score=("risk_points", "sum"),
).reset_index()

cust_risk = customers.merge(cust_risk, on="customer_id")
cust_risk["risk_level"] = pd.cut(
    cust_risk["risk_score"],
    bins=[-1, 99, 199, float("inf")],
    labels=["Low", "Medium", "High"],
)

# ---- Alerts table (this is what Power Apps will edit later) ----
alerts = txns[txns["risk_points"] > 0].copy()


def reason(row):
    r = []
    if row["flag_large_cash"]:
        r.append("Large cash deposit")
    if row["flag_structuring"]:
        r.append("Possible structuring")
    if row["flag_high_risk_country"]:
        r.append("High-risk country")
    return "; ".join(r)


alerts["alert_reason"] = alerts.apply(reason, axis=1)
alerts = alerts.sort_values(
    "risk_points", ascending=False).reset_index(drop=True)
alerts.insert(0, "alert_id", [
              f"A{str(i+1).zfill(5)}" for i in range(len(alerts))])
alerts["status"] = "Open"
alerts["analyst_comment"] = ""
alerts["reviewed_by"] = ""

alerts = alerts[[
    "alert_id", "txn_id", "customer_id", "txn_date", "txn_type", "amount_aed",
    "destination_country", "alert_reason", "risk_points",
    "status", "analyst_comment", "reviewed_by",
]]

# ---- Export to Excel ----
with pd.ExcelWriter("aml_output.xlsx", engine="openpyxl") as writer:
    cust_risk.to_excel(writer, sheet_name="Customer_Risk", index=False)
    alerts.to_excel(writer, sheet_name="Alerts", index=False)
    txns.drop(columns=["near_limit"]).to_excel(
        writer, sheet_name="Transactions", index=False)

print("Customers by risk level:")
print(cust_risk["risk_level"].value_counts())
print("\nAlerts by reason:")
print(alerts["alert_reason"].value_counts())
print("\nTotal alerts:", len(alerts))
print("\nTop 10 riskiest customers:")
print(cust_risk.sort_values("risk_score", ascending=False)[
    ["customer_id", "customer_name", "flagged_txns", "risk_score", "risk_level"]
].head(10))
