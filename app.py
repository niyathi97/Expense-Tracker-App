import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("💰 Expense Tracker Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
file_path = "data/Expenses_clean.csv"
df = pd.read_csv(file_path)

# Clean columns
df.columns = df.columns.str.strip().str.lower()

# Convert date
df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')

# Drop nulls
df = df.dropna()

# Feature engineering
df['month_year'] = df['date_time'].dt.to_period('M')
df['weekday'] = df['date_time'].dt.day_name()

# -----------------------------
# SIDEBAR FILTER
# -----------------------------
st.sidebar.header("Filters")

categories = st.sidebar.multiselect(
    "Select Category",
    options=df['category'].unique(),
    default=df['category'].unique()
)

filtered_df = df[df['category'].isin(categories)]

# -----------------------------
# KPIs
# -----------------------------
total_expense = filtered_df['amount'].sum()
avg_expense = filtered_df['amount'].mean()

col1, col2 = st.columns(2)

col1.metric("Total Expense", f"{total_expense}")
col2.metric("Average Expense", f"{round(avg_expense, 2)}")

# -----------------------------
# CATEGORY CHART
# -----------------------------
st.subheader("Category-wise Spending")

category_expense = filtered_df.groupby('category')['amount'].sum()

fig1, ax1 = plt.subplots()
category_expense.plot(kind='bar', ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

# -----------------------------
# MONTHLY TREND
# -----------------------------
st.subheader("Monthly Spending Trend")

monthly_expense = filtered_df.groupby('month_year')['amount'].sum()

fig2, ax2 = plt.subplots()
monthly_expense.plot(marker='o', ax=ax2)
st.pyplot(fig2)

# -----------------------------
# PIE CHART
# -----------------------------
st.subheader("Spending Distribution")

fig3, ax3 = plt.subplots()
category_expense.plot(kind='pie', autopct='%1.1f%%', ax=ax3)
plt.ylabel("")
st.pyplot(fig3)

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(20))