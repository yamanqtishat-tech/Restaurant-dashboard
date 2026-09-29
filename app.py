import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Page settings
st.set_page_config(
    page_title="Restaurant Sales Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# Title and introduction
st.title("🍽️ Restaurant Sales Dashboard")
st.write("Interactive dashboard for exploring restaurant bills and tips.")

# Load dataset
tips = sns.load_dataset("tips")

# Show first 10 rows
st.subheader("First 10 Rows")
st.dataframe(tips.head(10), use_container_width=True)

# Sidebar filters
st.sidebar.header("Filters")

days = sorted(tips["day"].dropna().unique())

if "selected_day" not in st.session_state:
    st.session_state.selected_day = days[0]

if "bill_range" not in st.session_state:
    st.session_state.bill_range = (0.0, 50.0)

# Reset button
if st.sidebar.button("Reset Filters"):
    st.session_state.selected_day = days[0]
    st.session_state.bill_range = (0.0, 50.0)
    st.rerun()

selected_day = st.sidebar.selectbox(
    "Select a day",
    days,
    key="selected_day"
)

min_bill, max_bill = st.sidebar.slider(
    "Total Bill Range",
    min_value=0.0,
    max_value=50.0,
    key="bill_range"
)

# Filter data
filtered_tips = tips[
    (tips["day"] == selected_day) &
    (tips["total_bill"] >= min_bill) &
    (tips["total_bill"] <= max_bill)
]

# KPI section
st.subheader("Key Performance Indicators")

col1, col2, col3 = st.columns(3)

if not filtered_tips.empty:
    col1.metric("عدد الطلبات", len(filtered_tips))
    col2.metric(
        "متوسط الفاتورة",
        f"${filtered_tips['total_bill'].mean():.2f}"
    )
    col3.metric(
        "متوسط الإكرامية",
        f"${filtered_tips['tip'].mean():.2f}"
    )
else:
    col1.metric("عدد الطلبات", 0)
    col2.metric("متوسط الفاتورة", "$0.00")
    col3.metric("متوسط الإكرامية", "$0.00")

# Tabs
tab1, tab2 = st.tabs(["Overview", "Details"])

with tab1:

    if filtered_tips.empty:
        st.warning("لا توجد بيانات تطابق الفلاتر الحالية.")
    else:

        # Histogram
        st.subheader("Distribution of Total Bill")

        fig, ax = plt.subplots(figsize=(8, 4))

        sns.histplot(
            filtered_tips["total_bill"],
            bins=20,
            kde=True,
            ax=ax
        )

        ax.set_xlabel("Total Bill")
        ax.set_ylabel("Number of Orders")

        st.pyplot(fig)
        plt.close(fig)

        # Average tip by day
        st.subheader("Average Tip by Day")

        avg_tip_by_day = (
            filtered_tips
            .groupby("day", observed=False)["tip"]
            .mean()
            .reset_index()
        )

        fig2 = px.bar(
            avg_tip_by_day,
            x="day",
            y="tip",
            title="Average Tip by Day",
            labels={
                "day": "Day",
                "tip": "Average Tip"
            }
        )

        st.plotly_chart(fig2, use_container_width=True)

with tab2:

    st.subheader("Filtered Data")

    st.dataframe(
        filtered_tips,
        use_container_width=True
    )

    st.write("Number of filtered records:", len(filtered_tips))