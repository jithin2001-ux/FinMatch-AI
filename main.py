import pandas as pd

# ==========================================
# FINMATCH AI - FINANCE RECONCILIATION AGENT
# ==========================================

# Load data
invoices = pd.read_csv("data/invoices.csv")
payments = pd.read_csv("data/payments.csv")

results = []

# Check every invoice
for _, invoice in invoices.iterrows():

    invoice_id = invoice["invoice_id"]
    invoice_amount = invoice["amount"]
    vendor = invoice["vendor"]

    # Find payments for this invoice
    matching_payments = payments[
        payments["invoice_id"] == invoice_id
    ]

    # CASE 1: No payment
    if len(matching_payments) == 0:

        status = "MISSING PAYMENT"
        priority = "HIGH"
        impact = invoice_amount

        explanation = (
            f"No payment was found for the invoice "
            f"of ₹{invoice_amount:,.0f}."
        )

        action = (
            "Follow up with the payment team and "
            "verify whether payment is overdue."
        )

    # CASE 2: Multiple payments
    elif len(matching_payments) > 1:

        status = "DUPLICATE PAYMENT"

        total_paid = matching_payments["amount"].sum()

        # Amount paid above the invoice value
        overpayment = max(0, total_paid - invoice_amount)

        priority = "HIGH"
        impact = overpayment

        explanation = (
            f"{len(matching_payments)} payments were found. "
            f"Invoice value: ₹{invoice_amount:,.0f}. "
            f"Total paid: ₹{total_paid:,.0f}. "
            f"Potential overpayment: ₹{overpayment:,.0f}."
        )

        action = (
            "Review the duplicate transaction and verify "
            "whether a refund or adjustment is required."
        )

    # CASE 3: One payment
    else:

        payment_amount = matching_payments.iloc[0]["amount"]

        difference = invoice_amount - payment_amount

        # Correct payment
        if payment_amount == invoice_amount:

            status = "MATCHED"
            priority = "LOW"
            impact = 0

            explanation = (
                "Invoice amount and payment amount match exactly."
            )

            action = "No action required."

        # Incorrect payment
        else:

            status = "AMOUNT MISMATCH"
            priority = "MEDIUM"
            impact = abs(difference)

            explanation = (
                f"Invoice value is ₹{invoice_amount:,.0f}, "
                f"but payment received is ₹{payment_amount:,.0f}. "
                f"Difference: ₹{abs(difference):,.0f}."
            )

            action = (
                "Review the payment and verify whether this "
                "is an authorized partial payment."
            )

    # Store the result
    results.append({
        "Invoice": invoice_id,
        "Vendor": vendor,
        "Invoice Amount": invoice_amount,
        "Status": status,
        "Priority": priority,
        "Financial Impact": impact,
        "Explanation": explanation,
        "Recommended Action": action
    })


# Convert results to a table
results_df = pd.DataFrame(results)


# ==========================================
# SUMMARY
# ==========================================

total = len(results_df)

matched = len(
    results_df[results_df["Status"] == "MATCHED"]
)

exceptions = total - matched

match_rate = (matched / total) * 100

high_priority = len(
    results_df[results_df["Priority"] == "HIGH"]
)

medium_priority = len(
    results_df[results_df["Priority"] == "MEDIUM"]
)

exception_value = results_df[
    results_df["Status"] != "MATCHED"
]["Financial Impact"].sum()


# ==========================================
# DISPLAY SUMMARY
# ==========================================

print("\n==========================================")
print("              FINMATCH AI")
print("     FINANCE RECONCILIATION AGENT")
print("==========================================")

print("\nRECONCILIATION SUMMARY")
print("------------------------------------------")

print(f"Total invoices       : {total}")
print(f"Matched invoices     : {matched}")
print(f"Exceptions           : {exceptions}")
print(f"Match rate           : {match_rate:.1f}%")
print(f"High priority        : {high_priority}")
print(f"Medium priority      : {medium_priority}")
print(f"Exception impact     : ₹{exception_value:,.0f}")


# ==========================================
# DISPLAY EXCEPTIONS
# ==========================================

print("\nEXCEPTION DETAILS")
print("------------------------------------------")

exceptions_df = results_df[
    results_df["Status"] != "MATCHED"
]

for _, row in exceptions_df.iterrows():

    print("\n------------------------------------------")

    print(f"Invoice   : {row['Invoice']}")
    print(f"Vendor    : {row['Vendor']}")
    print(f"Amount    : ₹{row['Invoice Amount']:,.0f}")
    print(f"Status    : {row['Status']}")
    print(f"Priority  : {row['Priority']}")
    print(f"Impact    : ₹{row['Financial Impact']:,.0f}")

    print("\nExplanation:")
    print(row["Explanation"])

    print("\nRecommended Action:")
    print(row["Recommended Action"])


# ==========================================
# SAVE RESULTS
# ==========================================

results_df.to_csv(
    "data/reconciliation_results.csv",
    index=False
)

print("\n==========================================")
print("Results saved to:")
print("data/reconciliation_results.csv")
print("==========================================")