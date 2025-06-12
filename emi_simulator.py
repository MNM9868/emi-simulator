import streamlit as st
import pandas as pd
import numpy as np

# EMI calculation function
def calculate_emi(principal, rate, tenure_years):
    monthly_rate = rate / (12 * 100)
    tenure_months = tenure_years * 12
    emi = principal * monthly_rate * (1 + monthly_rate)**tenure_months / ((1 + monthly_rate)**tenure_months - 1)
    return emi, tenure_months

# Expanded lender data with all 25 institutions
lender_data = [
    {"Institution": "SBI – Surya Shakti", "Min Amount": 10_00_000, "Max Amount": 10_00_00_000, "Rate": 10.15, "Tenure": 10, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "SIDBI – MSME Solar Loan", "Min Amount": 10_00_000, "Max Amount": 3_00_00_000, "Rate": 9.4, "Tenure": 7, "Collateral": "No", "Location": "Pan-India"},
    {"Institution": "Solfin Finance", "Min Amount": 50_000, "Max Amount": 1_00_00_000, "Rate": 13.5, "Tenure": 5, "Collateral": "No", "Location": "Pan-India"},
    {"Institution": "ICICI – C&I Solar Loan", "Min Amount": 10_00_000, "Max Amount": 20_00_00_000, "Rate": 11.0, "Tenure": 10, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "Yes Bank – Renewable Loan", "Min Amount": 2_00_00_000, "Max Amount": 100_00_00_000, "Rate": 11.5, "Tenure": 15, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "IDBI – Surya Shakti", "Min Amount": 5_00_000, "Max Amount": 25_00_000, "Rate": 10.5, "Tenure": 7, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "BoB Solar Scheme", "Min Amount": 20_00_000, "Max Amount": 5_00_00_000, "Rate": 10.2, "Tenure": 10, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "PNB Solar Loan", "Min Amount": 10_00_000, "Max Amount": 5_00_00_000, "Rate": 10.0, "Tenure": 10, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "Canara Bank Solar Finance", "Min Amount": 25_00_000, "Max Amount": 2_00_00_000, "Rate": 10.0, "Tenure": 10, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "HDFC Bank – Solar Loan", "Min Amount": 5_00_000, "Max Amount": 1_00_00_000, "Rate": 11.0, "Tenure": 7, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "Axis Bank MSME Energy Loan", "Min Amount": 10_00_000, "Max Amount": 5_00_00_000, "Rate": 11.0, "Tenure": 10, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "Electronica Finance Ltd.", "Min Amount": 5_00_000, "Max Amount": 3_00_00_000, "Rate": 12.5, "Tenure": 5, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "cKers / NetZero Finance", "Min Amount": 20_00_000, "Max Amount": 5_00_00_000, "Rate": 11.5, "Tenure": 7, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "Orb Energy", "Min Amount": 5_00_000, "Max Amount": 50_00_000, "Rate": 13.0, "Tenure": 5, "Collateral": "No", "Location": "Pan-India"},
    {"Institution": "U GRO Capital", "Min Amount": 5_00_000, "Max Amount": 2_00_00_000, "Rate": 14.5, "Tenure": 5, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "Kinara Capital", "Min Amount": 2_00_000, "Max Amount": 30_00_000, "Rate": 18.0, "Tenure": 5, "Collateral": "Optional", "Location": "Pan-India"},
    {"Institution": "Tata Capital Cleantech", "Min Amount": 5_00_00_000, "Max Amount": 250_00_00_000, "Rate": 11.5, "Tenure": 15, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "L&T Finance RE", "Min Amount": 50_00_000, "Max Amount": 20_00_00_000, "Rate": 11.5, "Tenure": 15, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "REC (via Banks)", "Min Amount": 1_00_00_000, "Max Amount": 500_00_00_000, "Rate": 10.5, "Tenure": 15, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "PFC – Utility Solar", "Min Amount": 5_00_00_000, "Max Amount": 1000_00_00_000, "Rate": 10.0, "Tenure": 15, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "IREDA – Term Financing", "Min Amount": 1_00_00_000, "Max Amount": 500_00_00_000, "Rate": 10.0, "Tenure": 15, "Collateral": "Yes", "Location": "Pan-India"},
    {"Institution": "Adani Capital", "Min Amount": 1_00_000, "Max Amount": 20_00_000, "Rate": 15.0, "Tenure": 5, "Collateral": "Minimal", "Location": "Pan-India"},
    {"Institution": "Muthoot Capital", "Min Amount": 2_00_000, "Max Amount": 25_00_000, "Rate": 15.5, "Tenure": 5, "Collateral": "Optional", "Location": "Pan-India"},
    {"Institution": "Ujjivan / Jana / ESAF SFBs", "Min Amount": 50_000, "Max Amount": 15_00_000, "Rate": 18.0, "Tenure": 5, "Collateral": "Optional", "Location": "Pan-India"},
    {"Institution": "HDB Financial Services", "Min Amount": 1_00_000, "Max Amount": 30_00_000, "Rate": 16.5, "Tenure": 5, "Collateral": "Optional", "Location": "Pan-India"}
]

lenders_df = pd.DataFrame(lender_data)

# UI Inputs
st.title("🌞 Industrial Solar Loan EMI Simulator")

loan_amount = st.number_input("Enter Loan Amount (₹)", min_value=100000, max_value=100000000, step=100000, value=10000000)
tenure = st.slider("Select Tenure (Years)", 1, 15, 5)
collateral_pref = st.selectbox("Do you prefer collateral-free loans?", ["Both", "Yes", "No"])

# Filter lenders
filtered_df = lenders_df[
    (lenders_df["Min Amount"] <= loan_amount) &
    (lenders_df["Max Amount"] >= loan_amount) &
    (lenders_df["Tenure"] >= tenure)
]

if collateral_pref == "Yes":
    filtered_df = filtered_df[filtered_df["Collateral"] == "No"]
elif collateral_pref == "No":
    filtered_df = filtered_df[filtered_df["Collateral"] == "Yes"]

st.subheader("🔍 Matched Lenders")
st.write(filtered_df[["Institution", "Rate", "Tenure", "Collateral"]])

# EMI Calculation Table
st.subheader("📊 EMI Chart")
emi_results = []
for _, row in filtered_df.iterrows():
    emi, months = calculate_emi(loan_amount, row["Rate"], tenure)
    emi_results.append({"Institution": row["Institution"], "Rate (%)": row["Rate"], "EMI (₹)": round(emi, 2), "Total Payable (₹)": round(emi * months, 2)})

emi_df = pd.DataFrame(emi_results)
st.dataframe(emi_df)

# Download link
st.download_button(
    label="📥 Download EMI Table (Excel)",
    data=emi_df.to_csv(index=False).encode('utf-8'),
    file_name="emi_schedule.csv",
    mime="text/csv"
)

st.caption("Note: Rates and tenures are approximate. Please verify with lender before applying.")
