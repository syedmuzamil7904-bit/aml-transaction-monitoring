import pandas as pd

customers = pd.read_csv('C:/Users/Syedm/Documents/AML Project/customers.csv')
transaction = pd.read_csv(
    'C:/Users/Syedm/Documents/AML Project/transactions.csv')

print('customers')
print(customers.head(10))
print(customers.shape)


print("\n Transactions")
print(transaction.head(10))
print(transaction.shape)

print('/n Summary of transaction Amount:')
print(transaction["amount_aed"].describe())

print('/n Types of Transaction:')
print(transaction['amount_aed'].value_counts())

print('/n Diffrent Countries:')
print(transaction["destination_country"].value_counts())
