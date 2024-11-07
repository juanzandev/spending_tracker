import streamlit as st
from streamlit_navigation_bar import st_navbar
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
from pages.utils.agent import ScoreAgent
from db.db_functions import fetch_user_info
import math as mt
#from pages.util.score_details import ScoreDetails

def spending_score():
    st.title("Spending Analyzer")
    st.text("Below you can find your latest Spending Score, interesting metrics that you should consider when reviewing your spending habits, as well as the recommendation from our fancy Large Language Model (LLM).")
    st.divider()

    # -------- Metric Retrieval -------- #
    score_agent = ScoreAgent()
    username = st.session_state['username']
    user_info = fetch_user_info(username)
    spending_score = user_info['spending_score']
    # : calculate score, this score is based on the data from USER_1.csv
    #spending_score = int(score_agent.fetch_score())
    # :: logic for spending score label
    if spending_score <= 3:
        label = "Good! You are earning +1% cashback on groceries."
    elif 4 >= spending_score <= 6:
        label = "Great! You are earning +1% cashback on groceries and online purchases."
    elif 7 >= spending_score <= 8:
        label = "Nice! You are earning +2% cashback on linked subscription rewards."
    elif 9 >= spending_score <= 10:
        label = "Awesome score! You are earning +1% extra cashback on top of your current cashback reward."

    spending_score = float(spending_score)
    # : fetch recommendation, based on the given score
    actual_recomendation = score_agent.recommendation(score = spending_score)
    # ------------- end ------------ #

    # ----------- Analyser ------------ #
    #df = pd.read_csv("util/User_1.csv")
    #categories = df["Category"].value_counts().to_frame().reset_index()
    #categories.columns = ["Category", "Count"]
    #categories
    # ----------------------------------#

    def display_top_tiles():
        col1, col2 = st.columns(2)

        col1.metric(label="Spending Score", value=spending_score, delta=label, delta_color = 'off')
        #col2.bar_chart(categories, x = "Category", y = "Count",
                       #color = "Category")

        style_metric_cards(background_color='#000')
    display_top_tiles()

    st.divider()

    def display_mid_tiles():
        col1, col2 = st.columns(2)

        col1.subheader("Our LLM recomendation is powered by:")
        col2.subheader("LLAMA 3.1 70B Parameters")
    
    display_mid_tiles()
    st.text("Keep in mind that the recommendation is based on your *current* Spending Score.")
    
    with st.chat_message("assistant"):
        st.write(actual_recomendation)
    
    # Interactive feature
    user_input = st.text_input("Enter your Spending Score: ", 0)
    ht_recommendation = score_agent.recommendation(score = float(user_input))
    
    with st.chat_message("assistant"):
        st.write(f"Using a hypotetical score, {ht_recommendation}")

if __name__=="__main__":
    spending_score()