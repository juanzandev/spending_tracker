import streamlit as st
import streamlit_shadcn_ui as ui
from db.db_functions import fetch_transactions, fetch_user_info, calculate_user_spending_current_month
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime, timedelta


def dashboard():
    username = st.session_state["username"]
    user_info = fetch_user_info(username)
    if user_info is None:
        st.error("Failed to fetch user information")
        return
    user_id = user_info['user_id']
    spending_score = user_info['spending_score']
    last_balance = user_info['balance']
    budget = user_info['latest_budget']
    last_ten_transactions = fetch_transactions(username, 10)
    current_month_spending = calculate_user_spending_current_month(user_id)
    today = datetime.today()
    first_day_current_month = today.replace(day=1)
    last_day_current_month = (today.replace(
        day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Format the dates as strings
    first_day_str = first_day_current_month.strftime("%d/%m/%Y")
    last_day_str = last_day_current_month.strftime("%d/%m/%Y")
    st.title("Dashboard")
    st.subheader(
        f"Welcome *{st.session_state["name"]}* to Your Personal Finance Dashboard!")
    st.write("""
    Manage your finances with ease. Track your spending, monitor your budget, and stay on top of your financial goals.
    Use the tools and insights provided to make informed decisions and improve your financial health.
    """)
    st.divider()
    # METRIC CARDS
    card_cols = st.columns(3)
    with card_cols[0]:
        ui.metric_card(title="Spending Score", content=f"{spending_score}/10.0",
                       description="+5.5% from last month", key="card1")
    with card_cols[1]:
        ui.metric_card(title=f"Budget Used ({first_day_str} - {last_day_str})", content=f"${current_month_spending:.2f}/${budget}",
                       description="#change your budget on the Get Started tab", key="card2")
    with card_cols[2]:
        ui.metric_card(title="Account Balance",
                       content=f"${last_balance}",
                       description="#total balance in your Discover account", key="card3")
    st.divider()

    # LAST 10 TRANSACTIONS
    st.subheader("Your Last 10 Transactions:")
    st.write("""
             This section provides a clear view of your most recent spending activities, allowing you to track each transaction’s impact on your overall balance.

                The table displays essential details for each transaction, including dates, amounts, categories, and updated balances. With this information, you can easily identify spending patterns and review past purchases.

                Accompanying the table is a line graph, visually illustrating how your balance changes with each transaction. By observing the upward and downward trends, you can quickly gauge periods of increased spending or saving, helping you make informed financial decisions.

                Use this section as a powerful tool to monitor your daily financial habits and stay in control of your budgeting goals.""")
    transaction_graph = st.columns(2)

    if last_ten_transactions:
        # LEFT COLUMN/ LAST 10 TRANSACTIONS TABLE
        # Define column names based on the SELECT query
        columns = ["Date", "Description", "Transaction Type", "Amount",
                   "Category", "Payment Method", "Merchant", "Balance"]

        # Convert transactions to a pandas DataFrame
        df = pd.DataFrame(last_ten_transactions, columns=columns)
        styled_balance = df['Balance'].apply(lambda x: f"${x:.2f}")
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

        def color_amount(val):
            color = 'red' if val < 0 else 'green'
            return f'color: {color}'

        # Apply the style to the Amount column
        styled_df = df.style.map(color_amount, subset=['Amount'])
        # Display the DataFrame using st.table

        with transaction_graph[0]:

            st.dataframe(styled_df, hide_index=True,
                         use_container_width=True, )

        # RIGHT COLUMN / LAST 10 TRANSACTIONS GRAPH
        # Create an index column for transaction sequence
        df_inverted = df.iloc[::-1].reset_index(drop=True)
        df_inverted['Transaction Number'] = range(1, len(df_inverted) + 1)

        # Plot the chart using Matplotlib
        plt.rcParams.update({
            'text.color': 'white',
            'axes.labelcolor': 'white',
            'xtick.color': 'white',
            'ytick.color': 'white'
        })
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')

        # Add colors for line segments based on balance direction
        for i in range(1, len(df_inverted)):
            color = 'green' if df_inverted['Balance'][i] >= df_inverted['Balance'][i-1] else 'red'
            ax.plot(df_inverted['Transaction Number'].iloc[i-1:i+1],
                    df_inverted['Balance'].iloc[i-1:i+1], color=color, marker='o')

        # Annotate each transaction with the balance value
        for i, balance in enumerate(df_inverted['Balance']):
            ax.annotate(f"${balance:.2f}", (df_inverted['Transaction Number'][i], balance),
                        textcoords="offset points", xytext=(0, 5), ha='center')

        # Format y-axis labels to include a dollar sign
        ax.yaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f'${x:,.2f}'))

        # Set labels and title
        ax.set_xlabel('Transaction Number')
        ax.set_ylabel('Balance')
        ax.set_title('Balance Evolution Over Last 10 Transactions')

        plt.xticks(rotation=45)
        plt.tight_layout()

        with transaction_graph[1]:
            st.pyplot(fig)
    else:
        st.write("No transactions found.")
