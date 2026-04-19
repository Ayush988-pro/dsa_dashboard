import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="DSA Dashboard", layout="wide")

st.title("📊 DSA Progress Dashboard")

# ---------------------------
# SESSION STORAGE
# ---------------------------
if "dsa_data" not in st.session_state:
    st.session_state.dsa_data = pd.DataFrame(columns=[
        "Problem","Topic","Difficulty","Platform","Date"
    ])

df = st.session_state.dsa_data

# ---------------------------
# SIDEBAR INPUT
# ---------------------------
st.sidebar.header("➕ Add Problem")

problem = st.sidebar.text_input("Problem Name")

topic = st.sidebar.selectbox(
    "Topic",
    ["Array","Graph","DP","Tree","Greedy","Backtracking","Heap"]
)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy","Medium","Hard"]
)

platform = st.sidebar.selectbox(
    "Platform",
    ["LeetCode","Codeforces","GFG"]
)

date = st.sidebar.date_input("Solved Date")

# ---------------------------
# ADD BUTTON
# ---------------------------
if st.sidebar.button("Add Problem"):

    if problem.strip() == "":
        st.sidebar.warning("Enter problem name")
    else:
        new_row = pd.DataFrame(
            [[problem, topic, difficulty, platform, date]],
            columns=df.columns
        )

        st.session_state.dsa_data = pd.concat(
            [df, new_row],
            ignore_index=True
        )

        st.sidebar.success("Added 🚀")

df = st.session_state.dsa_data

# ---------------------------
# OVERVIEW METRICS
# ---------------------------
st.subheader("📈 Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Problems", len(df))
col2.metric("Topics Covered", df["Topic"].nunique())
col3.metric("Platforms Used", df["Platform"].nunique())
col4.metric("Hard Problems", (df["Difficulty"]=="Hard").sum())

# ---------------------------
# TABLE
# ---------------------------
st.subheader("📄 Problem Log")

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("No problems added yet")

# ---------------------------
# CHARTS
# ---------------------------
if not df.empty:

    # Topic Chart
    st.subheader("📊 Topic Analysis")

    topic_df = df["Topic"].value_counts().reset_index()
    topic_df.columns = ["Topic","Count"]

    st.plotly_chart(
        px.bar(topic_df, x="Topic", y="Count", color="Count"),
        use_container_width=True
    )

    # Difficulty Pie
    st.subheader("🥧 Difficulty Distribution")

    diff_df = df["Difficulty"].value_counts().reset_index()
    diff_df.columns = ["Difficulty","Count"]

    st.plotly_chart(
        px.pie(diff_df, names="Difficulty", values="Count"),
        use_container_width=True
    )

    # Daily Progress
    st.subheader("📅 Daily Progress")

    daily_df = df.groupby("Date").size().reset_index(name="Problems")

    st.plotly_chart(
        px.line(daily_df, x="Date", y="Problems", markers=True),
        use_container_width=True
    )

    # Radar Chart
    st.subheader("🧠 Topic Mastery")

    radar_df = df["Topic"].value_counts().reset_index()
    radar_df.columns = ["Topic","Solved"]

    fig = px.line_polar(radar_df, r="Solved", theta="Topic", line_close=True)
    fig.update_traces(fill="toself")

    st.plotly_chart(fig, use_container_width=True)