import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import dateutil.relativedelta as rd

st.title("📦 Shelf-Life Progress Calculator")

# Sidebar inputs
st.sidebar.header("Enter Details")
product_name = st.sidebar.text_input("Product Name")
start_date = st.sidebar.date_input("Start Date", datetime.today())
end_date = st.sidebar.date_input("End Date (optional)", None)
months = st.sidebar.number_input("Shelf Life (Months)", min_value=0, value=0)
days = st.sidebar.number_input("Shelf Life (Days)", min_value=0, value=0)
weeks = st.sidebar.number_input("Shelf Life (Weeks)", min_value=0, value=0)

today = datetime.today().date()

# --- Formula 1: Month-based ---
progress_months = None
if months > 0:
    expiry_months = start_date + rd.relativedelta.relativedelta(months=months)
    progress_months = 100 * max(0, min(1, (expiry_months - today).days / (expiry_months - start_date).days))

# --- Formula 2: Fixed start–end dates ---
progress_fixed = None
if end_date:
    progress_fixed = 100 - (((end_date - today).days / (end_date - start_date).days) * 100)

# --- Formula 3: Days-based ---
progress_days = None
if days > 0:
    expiry_days = start_date + timedelta(days=days)
    progress_days = 100 * max(0, min(1, (expiry_days - today).days / days))

# --- Formula 4: Weeks-based ---
progress_weeks = None
if weeks > 0:
    expiry_weeks = start_date + timedelta(days=weeks*7)
    progress_weeks = 100 * max(0, min(1, (expiry_weeks - today).days / (weeks*7)))

# --- Display results ---
st.subheader("📊 Results")
st.write(f"**Product:** {product_name}")
if progress_months is not None:
    st.write(f"Month-based progress: {progress_months:.2f}%")
if progress_fixed is not None:
    st.write(f"Fixed start–end progress: {progress_fixed:.2f}%")
if progress_days is not None:
    st.write(f"Days-based progress: {progress_days:.2f}%")
if progress_weeks is not None:
    st.write(f"Weeks-based progress: {progress_weeks:.2f}%")

# Progress bar (show whichever is last calculated)
if progress_months is not None:
    st.progress(progress_months/100)
elif progress_fixed is not None:
    st.progress(progress_fixed/100)
elif progress_days is not None:
    st.progress(progress_days/100)
elif progress_weeks is not None:
    st.progress(progress_weeks/100)

# Dashboard storage
if "data" not in st.session_state:
    st.session_state["data"] = []

if st.sidebar.button("Add to Dashboard"):
    st.session_state["data"].append({
        "Product": product_name,
        "Start Date": start_date,
        "End Date": end_date if end_date else "-",
        "Months": months,
        "Days": days,
        "Weeks": weeks,
        "Progress (Months)": round(progress_months,2) if progress_months else "-",
        "Progress (Fixed)": round(progress_fixed,2) if progress_fixed else "-",
        "Progress (Days)": round(progress_days,2) if progress_days else "-",
        "Progress (Weeks)": round(progress_weeks,2) if progress_weeks else "-"
    })

if st.session_state["data"]:
    st.subheader("📋 Dashboard")
    df = pd.DataFrame(st.session_state["data"])
    st.dataframe(df)
