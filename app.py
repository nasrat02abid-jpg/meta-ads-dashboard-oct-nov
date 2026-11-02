import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Meta Ads Performance Dashboard", layout="wide")


# د ډېټا لود کولو فنکشن (که فایل مو پاک کړی وي او که اصلي وي)
@st.cache_data
def load_data():
  try:
    return pd.read_csv("Cleaned_Ads_Data_Oct_2026.csv")
  except:
    df = pd.read_excel("N.-A-id-Ads-Oct-1-2026-Nov-1-2026.xlsx")
    df["Results"] = df["Results"].fillna(0)
    return df


df = load_data()

st.title("📊 Meta Ads Campaign Dashboard")
st.markdown("### Overview (Oct 1, 2026 – Nov 1, 2026)")

# --- د مهمو مټریکونو (Metrics) برخه ---
total_spend = df["Amount spent (PKR)"].sum()
total_impressions = df["Impressions"].sum()
total_reach = df["Reach"].sum()

# دلته د مېسجونو دقیق شمېر (Total Messages = 1,290) راوباسو
messaging_df = df[
    df["Result indicator"].str.contains(
        "messaging_conversation_started", na=False
    )
]
total_messages = int(messaging_df["Results"].sum())

avg_cpr = (
    df[df["Cost per results"] > 0]["Cost per results"].mean()
    if not df[df["Cost per results"] > 0].empty
    else 0
)

# په ډشبورډ کې د کارډونو ښودل
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Spend (PKR)", f"₨{total_spend:,.2f}")
c2.metric("Total Impressions", f"{total_impressions:,}")
c3.metric("Total Reach", f"{total_reach:,}")
c4.metric(
    "Total Messages", f"{total_messages:,}"
)  # دلته به اوس دقیق 1290 وښيي
c5.metric("Avg Cost / Result", f"₨{avg_cpr:.2f}")

st.divider()

# --- د څنګ فلټرونه (Sidebar Filters) ---
st.sidebar.header("Filter Ads")
selected_ad_set = st.sidebar.multiselect(
    "Select Ad Set",
    options=df["Ad set name"].unique(),
    default=df["Ad set name"].unique(),
)
filtered_df = df[df["Ad set name"].isin(selected_ad_set)]

# --- چارټونه (Charts) ---
col_left, col_right = st.columns(2)

with col_left:
  fig_spend = px.bar(
      filtered_df,
      x="Ad set name",
      y="Amount spent (PKR)",
      color="Ad set name",
      title="Amount Spent by Ad Set",
  )
  st.plotly_chart(fig_spend, use_container_width=True)

with col_right:
  fig_results = px.scatter(
      filtered_df,
      x="Amount spent (PKR)",
      y="Results",
      size="Impressions",
      hover_name="Ad name",
      title="Spend vs. Results (Bubble Size = Impressions)",
  )
  st.plotly_chart(fig_results, use_container_width=True)

# --- د تفصيلي ډېټا جدول (Data Table) ---
st.subheader("Detailed Ads Performance")
st.dataframe(
    filtered_df[
        [
            "Ad set name",
            "Ad name",
            "Amount spent (PKR)",
            "Impressions",
            "Reach",
            "Results",
            "Cost per results",
            "Quality ranking",
        ]
    ]
)