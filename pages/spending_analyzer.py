import streamlit as st
from streamlit_navigation_bar import st_navbar
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
from pages.utils.agent import ScoreAgent
from db.db_functions import fetch_user_info, fetch_spending_scores
import plotly.graph_objects as go
import streamlit_shadcn_ui as ui
import math as mt
# from pages.util.score_details import ScoreDetails


def spending_score():
    st.title("Spending Analyzer")
    st.write("Below you can find your latest Spending Score, interesting metrics that you should consider when reviewing your spending habits, as well as the recommendation from our fancy Large Language Model (LLM).")
    st.divider()

    # -------- Metric Retrieval -------- #
    score_agent = ScoreAgent()
    username = st.session_state['username']
    user_info = fetch_user_info(username)
    spending_score = user_info['spending_score']
    user_id = user_info['user_id']

    # Determine label based on spending score
    if spending_score <= 3:
        label = "Good! You are earning +1% cashback on groceries."
    elif 4 >= spending_score <= 6:
        label = "Great! You are earning +1% cashback on groceries and online purchases."
    elif 7 >= spending_score <= 8:
        label = "Nice! You are earning +2% cashback on linked subscription rewards."
    elif 9 >= spending_score <= 10:
        label = "Awesome score! You are earning +1% extra cashback on top of your current cashback reward."

    spending_score = float(spending_score)
    # Fetch recommendation based on the given score
    actual_recommendation = score_agent.recommendation(score=spending_score)

    def display_top_tiles(user_id):
        col1, col2 = st.columns(2)
        with col1:
            ui.metric_card(title="Spending Score", content=f"{spending_score}/10.0",
                           description=label, key="card1")
            scores = fetch_spending_scores(user_id)
            # Define the benefits
            benefits = {
                1: "+1% cashback on groceries",
                2: "+1% cashback on groceries",
                3: "+1% cashback on groceries",
                4: "Previous rewards remain active. +1% cashback on online purchases",
                5: "Previous rewards remain active. +1% cashback on online purchases",
                6: "Previous rewards remain active. +1% cashback on online purchases",
                7: "Previous rewards remain active. +2% cashback on linked subscription rewards",
                8: "Previous rewards remain active. +2% cashback on linked subscription rewards",
                9: "Previous rewards remain active. +1% cashback on seasonal cashback rewards hosted by Discover",
                10: "Previous rewards remain active. +1% cashback on seasonal cashback rewards hosted by Discover"
            }

            # Create a DataFrame with a "Status" column and set "Score" as the index
            df_benefits = pd.DataFrame(list(benefits.items()), columns=[
                                       "Score", "Benefit Description"])
            df_benefits['Status'] = df_benefits['Score'].apply(
                lambda x: "✅" if x <= spending_score else "")
            df_benefits.set_index("Score", inplace=True)

            # Define a function to apply conditional formatting
            def highlight_benefits(row):
                score = row.name  # Get index value as the score
                if score <= spending_score:
                    return ['font-weight: bold; color: white'] * len(row)
                else:
                    return ['color: gray'] * len(row)

            # Apply the conditional formatting
            styled_df_benefits = df_benefits.style.apply(
                highlight_benefits, axis=1)

            # Custom CSS for font size, padding, and row height
            custom_css = """
            <style>
                table {
                    font-size: 16px;
                    border-collapse: collapse;
                    width: 100%;
                    line-height: 1.2;
                    background-color: transparent; /* Make the table background transparent */
                }
                th, td {
                    padding: 5px 10px;
                    background-color: transparent; /* Make cell backgrounds transparent */
                }
                tr:nth-child(even) {
                    background-color: transparent; /* Transparent background for even rows */
                }
                tr:nth-child(odd) {
                    background-color: transparent; /* Transparent background for odd rows */
                }
                th {
                    font-size: 16px;
                    color: white;
                    text-align: center;
                    background-color: transparent; /* Transparent background for header */
                }
                td {
                    color: white;
                }
            </style>
            """

            # Render the custom CSS
            st.markdown(custom_css, unsafe_allow_html=True)

            # Convert the styled DataFrame to HTML and display it
            st.markdown(styled_df_benefits.to_html(), unsafe_allow_html=True)
        with col2:
            if scores:
                if len(scores) == 1:
                    st.write(
                        "Not enough data to display evolution, this graph will be available next month.")
                else:
                    dates = [score['updated_at'] for score in scores]
                    scores_values = [score['score'] for score in scores]

                    fig = go.Figure()

                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=scores_values,
                        mode='lines+markers+text',
                        text=scores_values,
                        textposition='top center',
                        marker=dict(color='cyan'),
                        line=dict(color='cyan')
                    ))

                    fig.update_layout(
                        title='Spending Score Evolution',
                        xaxis_title='Date',
                        yaxis_title='Spending Score',
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        xaxis=dict(showgrid=False),
                        yaxis=dict(showgrid=False),
                        width=800,  # Set the width of the graph
                        height=700  # Set the height of the graph
                    )

                    st.plotly_chart(fig, use_container_width=True)

    display_top_tiles(user_id)

    st.divider()

    def display_mid_tiles():
        col1, col2 = st.columns(2)
        col1.header("Budget Buddy Chatbot")
        col1.subheader("Powered by: LLAMA 3.1 70B Parameters")

    display_mid_tiles()
    st.write(
        "Keep in mind that the recommendation is based on your *current* Spending Score.")

    with st.chat_message("assistant"):
        st.write(actual_recommendation)

    # Interactive feature
    st.divider()
    st.subheader("Hypothetical Spending Score")
    st.write("In this section, you can ask our AI Agent to simulate recommendations for a specific spending score.")
    user_input = st.text_input("Enter your Spending Score: ", None)
    if user_input is not None:
        ht_recommendation = score_agent.recommendation(score=float(user_input))

        with st.chat_message("assistant"):
            st.write(f"Using a hypothetical score, {ht_recommendation}")


if __name__ == "__main__":
    spending_score()
