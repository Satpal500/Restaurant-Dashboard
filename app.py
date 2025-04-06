
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("restaurant_data_4months.csv")
df['date'] = pd.to_datetime(df['date'])

# Add calculated columns
df['total_amount'] = df['quantity'] * df['price']
df['day'] = df['date'].dt.date
df['weekday'] = df['date'].dt.day_name()

st.set_page_config(page_title="Restaurant Analytics Dashboard", layout="wide")
st.title("🍽️ Restaurant Analytics Dashboard")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
date_range = st.sidebar.date_input("Select Date Range", [df['date'].min(), df['date'].max()])
items = st.sidebar.multiselect("Select Items", options=df['item_name'].unique(), default=df['item_name'].unique())
payments = st.sidebar.multiselect("Select Payment Modes", options=df['payment_mode'].unique(), default=df['payment_mode'].unique())

# Apply filters
filtered_df = df[
    (df['date'] >= pd.to_datetime(date_range[0])) &
    (df['date'] <= pd.to_datetime(date_range[1])) &
    (df['item_name'].isin(items)) &
    (df['payment_mode'].isin(payments))
]

st.markdown(f"### Total Revenue: ₹{filtered_df['total_amount'].sum():,.0f}")
st.markdown(f"### Total Orders: {filtered_df['quantity'].sum():,}")

# Revenue Over Time
st.subheader("📈 Revenue Over Time")
rev_by_day = filtered_df.groupby('day')['total_amount'].sum().reset_index()
fig1, ax1 = plt.subplots()
ax1.plot(rev_by_day['day'], rev_by_day['total_amount'], marker='o')
ax1.set_title("Daily Revenue")
ax1.set_xlabel("Date")
ax1.set_ylabel("Revenue")
st.pyplot(fig1)

# Top Selling Items
st.subheader("🍔 Top Selling Items")
top_items = filtered_df.groupby('item_name').agg({'quantity': 'sum', 'total_amount': 'sum'}).sort_values(by='quantity', ascending=False).head(10)
st.dataframe(top_items.style.format({'total_amount': '₹{:.0f}'}))

# Payment Mode Distribution
st.subheader("💳 Payment Mode Usage")
payment_counts = filtered_df['payment_mode'].value_counts()
fig2, ax2 = plt.subplots()
ax2.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%', startangle=140)
ax2.set_title("Payment Method Distribution")
st.pyplot(fig2)

# Sales by Weekday
st.subheader("📅 Sales by Weekday")
weekday_sales = filtered_df.groupby('weekday')['total_amount'].sum().reindex([
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
fig3, ax3 = plt.subplots()
sns.barplot(x=weekday_sales.index, y=weekday_sales.values, ax=ax3)
ax3.set_ylabel("Revenue")
ax3.set_title("Revenue by Weekday")
st.pyplot(fig3)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
