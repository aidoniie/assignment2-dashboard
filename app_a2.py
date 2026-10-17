
import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
df = pd.read_csv("college_dashboard.csv")

st.set_page_config(
    page_title="College Comparison Dashboard",
    layout="wide"
)

st.title("How do private and non-private colleges differ?")
st.write(
    "This dashboard compares graduation outcomes, tuition, "
    "applications, and enrolment across college types."
)

# Sidebar filter
college_type = st.sidebar.multiselect(
    "Select college type",
    options=sorted(df["Private"].unique()),
    default=sorted(df["Private"].unique())
)

# Apply filter
filtered = df[df["Private"].isin(college_type)]

# KPI cards
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Colleges selected",
    f"{len(filtered):,}"
)

c2.metric(
    "Average graduation rate",
    f"{filtered['Grad.Rate'].mean():.1f}%"
)

c3.metric(
    "Average out-of-state tuition",
    f"${filtered['Outstate'].mean():,.0f}"
)

c4.metric(
    "Average enrolment",
    f"{filtered['Enroll'].mean():,.0f}"
)

# Chart 1
fig1 = px.box(
    filtered,
    x="Private",
    y="Grad.Rate",
    title="Graduation rates differ by college type",
    labels={
        "Private": "Private college",
        "Grad.Rate": "Graduation rate (%)"
    }
)

# Chart 2
fig2 = px.box(
    filtered,
    x="Private",
    y="Outstate",
    title="Private colleges generally charge higher tuition",
    labels={
        "Private": "Private college",
        "Outstate": "Out-of-state tuition ($)"
    }
)

# Chart 3
fig3 = px.scatter(
    filtered,
    x="Outstate",
    y="Grad.Rate",
    color="Private",
    title="Tuition and graduation rate show a positive relationship",
    labels={
        "Outstate": "Out-of-state tuition ($)",
        "Grad.Rate": "Graduation rate (%)",
        "Private": "Private college"
    }
)

# Chart 4
fig4 = px.scatter(
    filtered,
    x="Apps",
    y="Enroll",
    color="Private",
    title="More applications are associated with higher enrolment",
    labels={
        "Apps": "Applications",
        "Enroll": "Enrolled students",
        "Private": "Private college"
    }
)

# Layout
left, right = st.columns(2)

with left:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)

with right:
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)

st.caption(
    "All four visualisations are linked to the college-type filter in the sidebar."
)
