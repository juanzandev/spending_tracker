import streamlit as st
from db.db_functions import fetch_user_info, add_budget, calculate_user_spending_current_month
import streamlit_shadcn_ui as ui


def get_started():
    st.title("Get Started")
    st.subheader(f'Welcome *{st.session_state["name"]}*')
    username = st.session_state["username"]
    user_info = fetch_user_info(username)
    if user_info is None:
        st.error("Failed to fetch user information")
        return
    user_id = user_info['user_id']
    spending_score = user_info['spending_score']
    budget = user_info['latest_budget']
    if user_id is None:
        st.error("Failed to fetch user ID.")
    else:
        if spending_score is None:
            st.error("Failed to fetch spending score.")
        if budget is None:
            st.error("Failed to fetch budget")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.image('images/syntax_society_logo.svg', width=500)
        col1.subheader("Welcome to Your Personal Finance Companion")
        col1.write("""
        This app is designed to help you gain control over your finances, track spending habits, and work towards financial goals with greater ease. Our tools offer a personalized and insightful experience for users, utilizing data and recommendations to make financial decisions simpler and more informed.
        """)

    with col2:
        col2.subheader("App Sections Overview")
        col2.write("""
        - **Dashboard**: Get a quick snapshot of your financials right when you open the app. The dashboard offers a convenient overview of your recent transactions, account balance, and spending score, so you can monitor your finances efficiently.
        
        - **Spending Analyzer**: This section features the spending score, a measure of your spending habits. You’ll also find AI-generated recommendations based on your score to help you improve your financial health and make more responsible spending choices.
        
        - **Spending Tracker**: Dive deeper into your spending patterns with visualizations that allow you to analyze transactions over time. This tool helps you track where your money goes, empowering you to make data-driven adjustments to your budget.

        - **Sample Data**: Curious to see the app’s full potential? This section provides analytics based on sample data, giving you a preview of how the app can help you achieve financial goals over time with consistent use.

        - **About Us**: Meet the team behind the app—Syntax Society. Here, you’ll find our profiles, contact information, and links to our website. Feel free to reach out with any questions or feedback!
        """)

    st.divider()
    add_budget_cols = st.columns(2)
    with add_budget_cols[0]:
        st.subheader("Understanding Your Budget in the App")
        st.write("""
        Your personal budget plays a crucial role in helping you manage and improve your financial health. By setting a budget in this app, you’re able to:
        
        - **Track and Control Spending**: Set limits on your spending to stay on track with your financial goals. The app monitors your transactions and alerts you if you're nearing or exceeding your budget.

        - **Personalized Budget Recommendations**: Based on your income and spending patterns, the app provides budget suggestions that align with your financial situation. Choose from preset budgets based on recommended spending habits or create your own tailored to your needs.

        - **Spending Score Impact**: Your budget is linked to your Spending Score (SS), a measure of your financial responsibility and spending behavior. Maintaining a balanced budget positively impacts your SS, while exceeding it can decrease it, potentially limiting reward benefits.

        - **Goal Setting and Savings**: Use your budget to allocate a portion of your income towards savings. If your spending habits align with your savings goal, you’ll maintain a high SS. If your budget doesn’t allow room for savings, the SS will adjust accordingly, encouraging responsible budgeting.

        Setting a budget is more than just limiting spending; it’s a proactive way to make the most of your income, earn rewards, and reach your financial goals with confidence. Let’s get started on setting up a budget that works for you!
        """)

    with add_budget_cols[1]:
        st.subheader('Add your budget')
        budget_input = st.number_input('Enter your budget here')
        if st.button("Submit"):
            if add_budget(user_id, budget_input):
                st.success("Budget added successfully!")
            else:
                st.error("Failed to add budget.")
        ui.metric_card(title="Your Budget", content=f"${budget}",
                       description="#change your budget on the Get Started tab", key="budget")
