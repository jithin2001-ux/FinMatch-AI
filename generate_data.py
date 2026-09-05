import pandas as pd
import random
from datetime import date, timedelta

# Make the random data repeatable
random.seed(42)

# Vendor names
vendors = [
    "ABC Supplies",
    "XYZ Technologies",
    "PQR Services",
    "DEF Solutions",
    "LMN Traders",
    "Global Office",
    "Smart Systems",
    "Prime Logistics",
    "Green Energy",
    "Metro Services"
]

invoices = []
payments = []

start_date = date(2026, 8, 1)

# Create 100 invoices
for i in range(1, 101):

    invoice_id = f"INV{i:03d}"
    vendor = random.choice(vendors)

    invoice_date = start_date + timedelta(days=random.randint(0, 30))

    amount = random.choice([
        5000, 7500, 8000, 9500, 10000,
        12000, 15000, 18000, 20000,
        25000, 30000
    ])

    invoices.append({
        "invoice_id": invoice_id,
        "vendor": vendor,
        "invoice_date": invoice_date,
        "amount": amount
    })

    # Most invoices get a correct payment
    if i <= 75:

        payment_date = invoice_date + timedelta(days=random.randint(1, 10))

        payments.append({
            "payment_id": f"PAY{i:03d}",
            "invoice_id": invoice_id,
            "vendor": vendor,
            "payment_date": payment_date,
            "amount": amount
        })

    # 10 invoices get partial payments
    elif i <= 85:

        payment_date = invoice_date + timedelta(days=random.randint(1, 10))

        partial_amount = amount - random.choice([1000, 2000, 5000])

        payments.append({
            "payment_id": f"PAY{i:03d}",
            "invoice_id": invoice_id,
            "vendor": vendor,
            "payment_date": payment_date,
            "amount": partial_amount
        })

    # 5 invoices have no payment
    elif i <= 90:
        pass

    # Last 10 invoices have correct payment + duplicate payment
    else:

        payment_date = invoice_date + timedelta(days=random.randint(1, 10))

        payments.append({
            "payment_id": f"PAY{i:03d}",
            "invoice_id": invoice_id,
            "vendor": vendor,
            "payment_date": payment_date,
            "amount": amount
        })

        payments.append({
            "payment_id": f"PAY{i:03d}D",
            "invoice_id": invoice_id,
            "vendor": vendor,
            "payment_date": payment_date + timedelta(days=1),
            "amount": amount
        })


# Convert to tables
invoices_df = pd.DataFrame(invoices)
payments_df = pd.DataFrame(payments)

# Save the files
invoices_df.to_csv("data/invoices.csv", index=False)
payments_df.to_csv("data/payments.csv", index=False)

print("================================")
print("FINMATCH AI - DATA GENERATOR")
print("================================")

print(f"\nInvoices created: {len(invoices_df)}")
print(f"Payments created: {len(payments_df)}")

print("\nFiles saved successfully!")
print("data/invoices.csv")
print("data/payments.csv")