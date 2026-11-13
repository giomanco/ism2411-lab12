"""
ISM2411 Lab 12 — Read a Sales CSV, Write a Cleaned Report

Reflection:
1. In Excel, where filtering, calculating totals, and exporting require manual clicking and formula dragging that must be repeated each time new data arrives, a Python ETL script automates the entire code consistently in a few seconds. Unlike Excel, Python easily scales to infinite amounts of rows, integrates with APIs or databases, and enforces strict data-cleaning logic without accidental manual edits, whereas Excel is faster for quick ad-hoc visual inspection, pivot-table exploration, and sharing formatted spreadsheets with non-technical stakeholders.
2. A real business process that would benefit from an append-mode log file would be an automated nightly inventory sync or payment-processing service. They would be able to  record each batch run's timestamp, record count, and status. Append mode is the right tool because it safes the history of every past execution without overwriting previous entries, allowing engineers or auditors to trace when outliers happen.
"""

import csv
from datetime import datetime


# Exercise 1: Get The File
print("=== Exercise 1: Verify sales.csv ===")
with open("data/sales.csv", mode="r", newline="") as f:
    reader = csv.reader(f)
    all_rows = list(reader)
print(f"Loaded data/sales.csv: header={all_rows[0]}, data rows={len(all_rows) - 1}\n")

# Exercise 2: Read and Print Raw Rows
print("=== Exercise 2: Raw Rows ===")
with open("data/sales.csv", mode="r", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
print()

#Exercise 3: Skip the Header
print("=== Exercise 3: Skip Header ===")
with open("data/sales.csv", mode="r", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    print("Header:", header)
    for row in reader:
        print(row)
print()

#Exercise 4: Compute Totals
print("=== Exercise 4: Compute Totals ===")
overall_total = 0.0
with open("data/sales.csv", mode="r", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        overall_total += line_total
        print(f"{product}: {quantity} units x ${price:.2f} = ${line_total:.2f}")
print(f"Overall Total Revenue: ${overall_total:.2f}\n")

#Execise 5: Filter and Write
print("=== Exercise 5: Filter and Write cleaned.csv ===")
original_count = 0
written_count = 0

with open("data/sales.csv", mode="r", newline="") as infile, open(
    "data/cleaned.csv", mode="w", newline=""
) as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    next(reader) 
    writer.writerow(["Product", "Price", "Qty", "Total"])

    for row in reader:
        original_count += 1
        product = row[0]
        price = float(row[1])
        qty = int(row[2])
        total = price * qty

        if total > 100:
          writer.writerow([product, f"{price:.2f}", qty, f"{total:.2f}"])
          written_count += 1

print(f"Wrote {written_count} qualifying rows out of {original_count} original rows to data/cleaned.csv.\n")


#Exercise 6: csv.DictReader
# Prefer csv.DictReader when columns have clear headers. 
# Prefer csv.reader when files lack headers or if column order is strictly fixed.
print("=== Exercise 6: csv.DictReader ===")
dict_overall_total = 0.0
with open("data/sales.csv", mode="r", newline="") as f:
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        product = row["product"]
        price = float(row["price"])
        quantity = int(row["quantity"])
        line_total = price * quantity
        dict_overall_total += line_total
        print(f"{product}: {quantity} units x ${price:.2f} = ${line_total:.2f}")
print(f"Overall Total Revenue (DictReader): ${dict_overall_total:.2f}\n")

# Exercise 7: Sales Summary By Product
print("=== Exercise 7: Sales Summary by Product ===")
product_summary = {}
with open("data/sales.csv", mode="r", newline="") as f:
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        product = row["product"]
        revenue = float(row["price"]) * int(row["quantity"])
        product_summary[product] = product_summary.get(product, 0.0) + revenue

for product in sorted(product_summary):
    print(f"{product}: ${product_summary[product]:.2f}")
print()


# Exercise 8: Append Mode Log
print("=== Exercise 8: Append Mode Log ===")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entry = f"[{timestamp}] Total Revenue: ${overall_total:.2f}\n"
with open("data/run_log.txt", mode="a") as log_file:
    log_file.write(log_entry)
print(f"Appended to data/run_log.txt: {log_entry.strip()}")
