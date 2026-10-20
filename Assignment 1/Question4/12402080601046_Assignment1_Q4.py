import csv
from datetime import datetime
from collections import defaultdict

input_file = input("Enter CSV file path: ")

balances = defaultdict(float)

with open(input_file, "r", newline="") as file:
    reader = csv.DictReader(file)

    with open("credit.csv", "w", newline="") as credit_file, \
         open("debit.csv", "w", newline="") as debit_file, \
         open("error.csv", "w", newline="") as error_file:

        credit_writer = csv.writer(credit_file)
        debit_writer = csv.writer(debit_file)
        error_writer = csv.writer(error_file)

        credit_writer.writerow(reader.fieldnames)
        debit_writer.writerow(reader.fieldnames)
        error_writer.writerow(reader.fieldnames + ["reason"])

        for row in reader:
            try:
                transaction_id = row["tid"]
                account_id = row["acc"]
                transaction_type = row["type"].strip().upper()
                amount = float(row["amount"])
                timestamp = row["time"]

                if not transaction_id or not account_id:
                    raise ValueError("Missing transaction or account ID")

                if transaction_type not in ["CREDIT", "DEBIT"]:
                    raise ValueError("Invalid transaction type")

                if amount <= 0:
                    raise ValueError("Amount must be greater than zero")

                datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")

                if transaction_type == "CREDIT":
                    credit_writer.writerow(row.values())
                    balances[account_id] += amount
                else:
                    debit_writer.writerow(row.values())
                    balances[account_id] -= amount

            except (ValueError, KeyError) as e:
                error_writer.writerow(
                    list(row.values()) + [str(e)]
                )

            except Exception as e:
                error_writer.writerow(
                    list(row.values()) + [str(e)]
                )

print("\nAccount-wise balance changes:")

for account, balance in sorted(
    balances.items(),
    key=lambda item: abs(item[1]),
    reverse=True
):
    print(account, int(balance) if balance.is_integer() else balance)

print("\nFiles created: credit.csv, debit.csv, error.csv")
