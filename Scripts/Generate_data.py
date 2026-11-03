import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()
random.seed(42)
np.random.seed(42)

N_CUSTOMERS = 500
N_TRANSACTIONS = 20000

high_risk_countries = ["Iran", "North Korea", "Syria", "Myanmar", "Yemen"]
normal_countries = ["UAE", "India", "UK", "USA", "Germany", "Singapore", "Pakistan", "Egypt"]
txn_types = ["Cash Deposit", "Wire Transfer", "Cash Withdrawal", "Online Transfer"]

customers = pd.DataFrame({
    "customer_id": [f"C{str(i).zfill(4)}" for i in range(N_CUSTOMERS)],
    "customer_name": [fake.name() for _ in range(N_CUSTOMERS)],
    "country": [random.choice(normal_countries) for _ in range(N_CUSTOMERS)],
    "occupation": [fake.job() for _ in range(N_CUSTOMERS)],
})

rows = []
for i in range(N_TRANSACTIONS):
    cust = customers.sample(1).iloc[0]
    amount = round(np.random.lognormal(mean=7, sigma=1), 2)
    dest = random.choices(
        normal_countries + high_risk_countries,
        weights=[10] * len(normal_countries) + [1] * len(high_risk_countries)
    )[0]
    rows.append({
        "txn_id": f"T{str(i).zfill(6)}",
        "customer_id": cust["customer_id"],
        "txn_date": fake.date_time_between(start_date="-1y", end_date="now"),
        "txn_type": random.choice(txn_types),
        "amount_aed": amount,
        "destination_country": dest,
    })

txns = pd.DataFrame(rows)

# Plant suspicious pattern: many deposits just under the 55,000 AED reporting limit
suspects = customers.sample(15)["customer_id"].tolist()
planted = []
for cid in suspects:
    for _ in range(random.randint(6, 12)):
        planted.append({
            "txn_id": f"S{len(planted):05d}",
            "customer_id": cid,
            "txn_date": fake.date_time_between(start_date="-60d", end_date="now"),
            "txn_type": "Cash Deposit",
            "amount_aed": round(random.uniform(50000, 54900), 2),
            "destination_country": "UAE",
        })

txns = pd.concat([txns, pd.DataFrame(planted)], ignore_index=True)

customers.to_csv("customers.csv", index=False)
txns.to_csv("transactions.csv", index=False)
print("Done:", len(customers), "customers,", len(txns), "transactions")