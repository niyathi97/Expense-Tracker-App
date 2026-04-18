import pandas as pd

# -----------------------------
# LOAD DATA
# -----------------------------
print("\n--- Loading Dataset ---")

file_path = "data/Expenses_clean.csv"
df = pd.read_csv(file_path)

print("\nFirst 5 Rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())


# -----------------------------
# DATA CLEANING
# -----------------------------
print("\n--- Data Cleaning ---")

# Standardize column names
df.columns = df.columns.str.strip().str.lower()
print("Columns:", df.columns)

# Convert date_time column
if 'date_time' in df.columns:
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')

# Remove missing values
df = df.dropna()

# Remove duplicates
df = df.drop_duplicates()

# Convert amount to numeric
if 'amount' in df.columns:
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

# Drop invalid rows again
df = df.dropna()

print("\nCleaned Data:")
print(df.head())


# -----------------------------
# FEATURE ENGINEERING
# -----------------------------
print("\n--- Feature Engineering ---")

if 'date_time' in df.columns:
    df['month'] = df['date_time'].dt.month
    df['year'] = df['date_time'].dt.year
    df['day'] = df['date_time'].dt.day
    df['weekday'] = df['date_time'].dt.day_name()
    df['month_year'] = df['date_time'].dt.to_period('M')

print(df.head())


# -----------------------------
# DATA ANALYSIS
# -----------------------------
print("\n--- Data Analysis ---")

# Total expense
total_expense = df['amount'].sum()
print("\nTotal Expense:", total_expense)

# Category-wise spending
category_expense = df.groupby('category')['amount'].sum().sort_values(ascending=False)
print("\nCategory-wise Expense:")
print(category_expense)

# Monthly spending
monthly_expense = df.groupby('month_year')['amount'].sum()
print("\nMonthly Expense:")
print(monthly_expense)

# Weekday spending
weekday_expense = df.groupby('weekday')['amount'].sum()
print("\nWeekday-wise Expense:")
print(weekday_expense)


# -----------------------------
# INSIGHTS GENERATION
# -----------------------------
print("\n--- Insights ---")

# Highest spending category
top_category = category_expense.idxmax()
print(f"\nYou spend the most on: {top_category}")

# Highest spending month
top_month = monthly_expense.idxmax()
print(f"Highest spending month: {top_month}")

# Average spending
avg_spending = df['amount'].mean()
print(f"Average transaction amount: {round(avg_spending, 2)}")

# High spending alert
threshold = df['amount'].mean() * 2
high_spend = df[df['amount'] > threshold]

print("\nHigh Spending Transactions:")
print(high_spend[['date_time', 'category', 'amount']])


# -----------------------------
# SAVE CLEAN DATA
# -----------------------------
df.to_csv("outputs/cleaned_expenses.csv", index=False)

print("\nCleaned data saved to outputs/cleaned_expenses.csv")

import matplotlib.pyplot as plt
import seaborn as sns

print("\n--- Generating Visualizations ---")

# Set style
sns.set()

# -----------------------------
# 1. Category-wise Spending (Bar Chart)
# -----------------------------
plt.figure(figsize=(10, 5))
category_expense.plot(kind='bar')
plt.title("Category-wise Spending")
plt.xlabel("Category")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/category_spending.png")
plt.show()


# -----------------------------
# 2. Monthly Spending (Line Chart)
# -----------------------------
plt.figure(figsize=(10, 5))
monthly_expense.plot(marker='o')
plt.title("Monthly Spending Trend")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.tight_layout()
plt.savefig("outputs/monthly_trend.png")
plt.show()


# -----------------------------
# 3. Category Distribution (Pie Chart)
# -----------------------------
plt.figure(figsize=(7, 7))
category_expense.plot(kind='pie', autopct='%1.1f%%')
plt.title("Spending Distribution by Category")
plt.ylabel("")
plt.tight_layout()
plt.savefig("outputs/category_pie.png")
plt.show()


# -----------------------------
# 4. Weekday Spending (Bar Chart)
# -----------------------------
plt.figure(figsize=(10, 5))
weekday_expense.plot(kind='bar')
plt.title("Weekday-wise Spending")
plt.xlabel("Day")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/weekday_spending.png")
plt.show()

print("\nCharts saved in outputs/ folder")