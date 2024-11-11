import streamlit as st
import streamlit_shadcn_ui as ui

overallDescription = """Meet the Syntax Society Team!"""

# Nolan is a first year undergraduate student from Kentucky, focusing in software and hardware engineering.

# J from Argentina: J is a computer science student from Buenos Aires with interests in software development and cybersecurity, who loves tango, football, and Argentine cuisine.

# D from Chicago: D is a computer science student focused on data science and cloud computing, who enjoys Chicago's cultural scene, live music, and deep-dish pizza."""

# (do this later)


juanDescription = """
<h3>Juan Zanguitu</h3>

<h6>Third Year CS Student</h6>

jzanguitu@hawk.iit.edu
"""

destinyDescription = """
<h3>Destiny Medina</h3>

<h6>Third Year CS Student</h6>

dmedina8@hawk.iit.edu
"""

nolanDescription = """
<h3>Nolan Lawrence</h3>

<h6>First Year CS Student</h6>

nlawrence1@hawk.iit.edu
"""

pieDescription = "<h4>Here you can see a summary of your transactions over the current month, and how they effect your overall budget.</h4>"
pieDescription2 = "<h5>Congratulations! You are on track to increasing your spending score this month! </h5>"

def pieChartDescription(totalSpending, totalBudget, moneyLeft):
    
    st.markdown(f"<p>{pieDescription}</p>", unsafe_allow_html=True)

    card_cols = st.columns(3)
    with card_cols[0]:
        ui.metric_card(title="Budget", content=f"${totalBudget}")
    with card_cols[1]:
        ui.metric_card(title="Total spent", content=f"${totalSpending}")
    with card_cols[2]:
        ui.metric_card(title="Remaining Budget", content=f"${moneyLeft}")
    
    st.markdown(f"<p>{pieDescription2}</p>", unsafe_allow_html=True)