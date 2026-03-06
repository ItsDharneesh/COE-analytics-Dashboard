import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# -----------------------------
# Resolve project root
# -----------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from utils.data_generator import generate_dataset
from utils.cleaning import clean_data

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="COE Analytics Dashboard", layout="wide")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("COE Analytics")
st.sidebar.write("Center of Excellence Initiative Monitoring Dashboard")

# -----------------------------
# Dynamic Dataset Generation
# -----------------------------
box = st.sidebar.container()

box.markdown(
    """
    <div style="
        border:2px solid #4CAF50;
        padding:15px;
        border-radius:10px;
        margin-bottom:10px;
    ">
        <h4 style="margin-bottom:5px;">
        ⬇️ Generate a New Dataset
        </h4>
        <p style="font-size:13px;">
        Click the button below to create a fresh dataset of 100 initiatives
        and observe how the dashboard updates dynamically.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

with box:
    if st.button("🔄 Generate New Dataset", use_container_width=True):

        new_df = generate_dataset(100)

        save_path = os.path.join(ROOT_DIR, "datasets", "coe_initiatives.csv")

        new_df.to_csv(save_path, index=False)

        st.success("New dataset generated!")

        st.rerun() 
# -----------------------------
# Title
# -----------------------------
st.title("COE Analytics Dashboard")

# -----------------------------
# Load and clean data
# -----------------------------
df = pd.read_csv(os.path.join(ROOT_DIR, "datasets", "coe_initiatives.csv"))
df = clean_data(df)

# -----------------------------
# Initiative Health Score
# -----------------------------
def calculate_health(row):
    if row["Status"] == "Delayed" or row["KPI %"] < 70:
        return "🔴 Red"
    elif row["KPI %"] < 90:
        return "🟡 Yellow"
    else:
        return "🟢 Green"

df["Health"] = df.apply(calculate_health, axis=1)

# -----------------------------
# Sidebar Filters
# -----------------------------
status_filter = st.sidebar.multiselect(
    "Filter by Status",
    options=df["Status"].unique(),
    default=df["Status"].unique()
)

owner_filter = st.sidebar.multiselect(
    "Filter by Owner",
    options=df["Owner"].unique(),
    default=df["Owner"].unique()
)

df = df[
    (df["Status"].isin(status_filter)) &
    (df["Owner"].isin(owner_filter))
]

# -----------------------------
# KPI Metrics
# -----------------------------
total_initiatives = len(df)
avg_kpi = df["KPI %"].mean()
on_track_pct = (df["Status"] == "On Track").mean() * 100
total_benefit = df["Business Benefit"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Initiatives", total_initiatives)
col2.metric("Average KPI Achievement", f"{avg_kpi:.2f}%")
col3.metric("On Track Initiatives", f"{on_track_pct:.1f}%")
col4.metric("Total Business Value Generated", f"₹{total_benefit:,.0f}")

st.divider()

# -----------------------------
# Status Distribution
# -----------------------------
st.subheader("Initiative Status Distribution")

status_counts = df["Status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]

fig_status = px.bar(
    status_counts,
    x="Status",
    y="Count",
    color="Status",
    title="Initiatives by Status"
)

st.plotly_chart(fig_status, use_container_width=True)

st.divider()

# -----------------------------
# Business Benefit Distribution
# -----------------------------
st.subheader("Business Benefit Distribution")

fig_benefit_dist = px.histogram(
    df,
    x="Business Benefit",
    nbins=20,
    title="Distribution of Initiative Business Benefits"
)

st.plotly_chart(fig_benefit_dist, use_container_width=True)

st.divider()

# -----------------------------
# Business Benefit by Owner
# -----------------------------
st.subheader("Business Benefit by Owner")

benefit_owner = df.groupby("Owner")["Business Benefit"].sum().reset_index()

fig_owner = px.bar(
    benefit_owner,
    x="Owner",
    y="Business Benefit",
    color="Owner",
    title="Total Business Benefit by Initiative Owner"
)

st.plotly_chart(fig_owner, use_container_width=True)

st.divider()

# -----------------------------
# Top Initiatives by Benefit
# -----------------------------
st.subheader("Top 3 Initiatives by Business Benefit")

top3 = df.sort_values("Business Benefit", ascending=False).head(3)

fig_top = px.bar(
    top3,
    x="Initiative Name",
    y="Business Benefit",
    color="Owner",
    title="Top Performing Initiatives"
)

st.plotly_chart(fig_top, use_container_width=True)

st.divider()

# -----------------------------
# Initiative Timeline
# -----------------------------
st.subheader("Initiative Timeline")

fig_gantt = px.timeline(
    df,
    x_start="Start Date",
    x_end="End Date",
    y="Initiative Name",
    color="Status",
    title="COE Initiative Timeline"
)

fig_gantt.update_yaxes(autorange="reversed")

st.plotly_chart(fig_gantt, use_container_width=True)

st.divider()

# -----------------------------
# Initiative Performance Table
# -----------------------------
st.subheader("Initiative Performance Overview")

display_df = df[
    [
        "Initiative Name",
        "Owner",
        "Status",
        "Health",
        "KPI %",
        "Business Benefit",
        "Start Date",
        "End Date",
    ]
]

st.dataframe(
    display_df,
    column_config={
        "KPI %": st.column_config.ProgressColumn(
            "KPI Achievement %",
            min_value=0,
            max_value=150,
        )
    },
    use_container_width=True,
)
