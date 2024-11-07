import streamlit as st
from streamlit_navigation_bar import st_navbar
from plotly import graph_objects as go
import pandas as pd
from .misc.descriptions import pieChartDescription
from db import db_functions as db



def spending_analyzer(): 

    st.title("Spending Analyzer")
    
    cols = st.columns(2)

    with cols[0]:
        displayPlot()
    
    totalSpent = 90  #db.calculate_user_spending_current_month()
    totalBudget = 100 # find the budget from database
    totalMoneyLeft = totalBudget - totalSpent
    description = pieChartDescription(totalSpent, totalBudget, totalMoneyLeft)

    with cols[1]:
        st.markdown(f"<p>{description}</p>",unsafe_allow_html=True)

    st.write("---")



def displayPlot():
    # Note:
    # each part of the graph (node) follows this format:

    #     Label
    #     Parent
    #     Value
        
    # Example:
    #     Paper Towels
    #     Groceries
    #     $14.12
    
    # Each node is defined by its Label's index
    # the Parent of each node is the Label's value
    # the Value of each node must be numerical

    # The arrays' indexies must be the same per node


    #SAMPLE DATA (change and calculate with the database)
    labels=["Budget", "Groceries", "Food"  , "Entertainment", "Movies"       , "Games"]
    parents=[""     , "Budget"   , "Budget", "Budget"       , "Entertainment", "Entertainment"]
    values=[100     , 30         , 40      , 20             , 5              , 15]

    #Budget is the root
    #Groceries, Food, and Enter. are children of Budget
    #Movies and Games are children of Entertainment
    
    fig =go.Figure(go.Sunburst(
        labels = labels,
        parents = parents,
        values = values,
        branchvalues="total" #change this to NONE if budget being exceeded is okay, it looks ugly though
    ))
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

    st.plotly_chart(fig, theme="streamlit")

#test
#spending_analyzer()  