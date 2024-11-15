import streamlit as st
from streamlit_navigation_bar import st_navbar
import streamlit_shadcn_ui as ui
import pandas as pd
import matplotlib as mt
from plotly import graph_objects as go
from .misc.descriptions import pieChartDescription
import decimal
from db.db_functions import insert_transaction, fetch_user_info, calculate_user_spending_current_month, fetch_user_transactions_current_month, fetch_transactions_by_period, fetch_transactions_for_candles, fetch_expenses_by_category
from datetime import datetime, timedelta
import uuid


def displayPlot(user_id):
    transactions = fetch_user_transactions_current_month(user_id)
    username = st.session_state['username']
    user_info = fetch_user_info(username)
    user_id = user_info['user_id']
    last_balance = user_info['balance']
    budget = user_info['latest_budget']
    categories = {}
    total_spent = 0

    for transaction in transactions:
        category = transaction['category']
        amount = transaction['amount']
        if amount < 0:  # Only consider negative amounts
            total_spent += abs(amount)
            if category in categories:
                categories[category] += abs(amount)
            else:
                categories[category] = abs(amount)

    # Filter out categories with a positive total amount
    categories = {k: v for k, v in categories.items() if v > 0}

    remaining_budget = budget - total_spent

    if not categories:
        st.markdown(
            """
            <h4 style='text-align: center;font-family: consolas; vertical-align:middle;'>It looks like you haven't made any transactions this month. Time to start spending wisely!</h3>""", unsafe_allow_html=True)
    else:
        labels = ["Budget"] + list(categories.keys()) + ["Remaining Budget"]
        parents = [""] + ["Budget"] * len(categories) + ["Budget"]
        values = [budget] + list(categories.values()) + [remaining_budget]

        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total"
        ))
        fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
        st.plotly_chart(fig, theme="streamlit")


def spending_tracker():
    username = st.session_state['username']
    user_info = fetch_user_info(username)
    user_id = user_info['user_id']
    last_balance = user_info['balance']
    budget = user_info['latest_budget']
    st.title("Spending Tracker")
    current_month_spending = calculate_user_spending_current_month(user_id)
    data_editor = pd.DataFrame(columns=[
                               'date', 'description', 'transaction_type', 'amount', 'category', 'payment_method', 'merchant'])
    transaction_type = ['Credit', 'Debit', 'Transfer']
    category = ['Rent', 'Groceries', 'Dining Out',
                'Entertainment', 'Utilities', 'Transportation', 'Salary', 'Gift', 'Education', 'Insurance', 'Other']
    payment_method = ['Account Transfer', 'Direct Deposit',
                      'Debit Card', 'Credit Card', 'ACH Transfer', 'Online Payment', 'Cash', 'Check', 'Other']
    config = {
        'date': st.column_config.DateColumn('Date', width='small', required=True),
        'transaction_type': st.column_config.SelectboxColumn('Transaction Type', options=transaction_type, required=True),
        'amount': st.column_config.NumberColumn('Amount', required=True),
        'description': st.column_config.TextColumn('Description', width='large', required=True),
        'payment_method': st.column_config.SelectboxColumn('Payment Method', options=payment_method, required=True),
        'category': st.column_config.SelectboxColumn('Category', options=category, required=True),
        'merchant': st.column_config.TextColumn('Merchant', required=True)
    }

    cols = st.columns(2)

    with cols[1]:
        displayPlot(user_id)

    # totalSpent = 90  # db.calculate_user_spending_current_month()
    # totalBudget = 100  # find the budget from database
    # totalMoneyLeft = totalBudget - totalSpent

    with cols[0]:
        pieChartDescription(
            current_month_spending, budget, float(budget) - float(current_month_spending))

    st.write("---")
    st.markdown(
        """
        ### Add Transactions
        - **Amount Input**: 
          - Enter a **negative value** for expenses (transactions).
          - Enter a **positive value** for income.
        - **Required Fields**: 
          - All columns per row must be filled for the transaction to be inserted successfully.
        - **Transaction Types**: 
          - Choose between **Credit** and **Debit**.
        - **Categories**: 
          - Select the appropriate category for your transaction.
        - **Payment Methods**: 
          - Specify the payment method used for the transaction.
        - **Row Deletion**:
          - After adding a row, you can delete it by selecting that row and clicking the trash icon on the right.
          - Please do this before adding another transaction.
        
        Make sure to fill in all the details accurately to keep your financial records up to date!
        """,
        unsafe_allow_html=True
    )
# Initialize session state for data editor key if not already initialized
    if 'dek' not in st.session_state:
        st.session_state.dek = str(uuid.uuid4())

    def update_data_editor():
        # Change the key of the data editor to start over
        st.session_state.dek = str(uuid.uuid4())

    add_transaction_table = st.data_editor(
        data_editor, column_config=config, num_rows='dynamic', key=st.session_state.dek)

    if st.button('Add transaction'):
        if user_id is None:
            st.error("Failed to fetch user ID.")
        else:
            if last_balance is None:
                st.error("Failed to fetch last balance.")
            else:
                for index, row in add_transaction_table.iterrows():
                    date = row['date']
                    description = row['description']
                    transaction_type = row['transaction_type']
                    amount = decimal.Decimal(row['amount'])
                    category = row['category']
                    payment_method = row['payment_method']
                    merchant = row['merchant']

                    # Calculate the new balance
                    new_balance = last_balance + amount

                    # Insert the transaction into the database
                    success = insert_transaction(
                        user_id, date, description, transaction_type, amount, category, payment_method, merchant, new_balance)
                    if success:
                        st.success(f"Transaction {index + 1} added successfully.")
                        # Update last_balance for the next transaction
                        last_balance = new_balance
                    else:
                        st.error(f"Failed to add transaction {index + 1}.")

                # Clear the input in the data editor by updating the key
                update_data_editor()

    st.divider()

    # Slider section
    st.markdown(
        """
        ### Transaction Analyzer
        Use the slider below to filter transactions by period.
        """
    )

    graph_type = ui.tabs(options=['Transactions Chart', 'Expenses/Income Histogram',
                         'Categorized Expenses'], default_value='Transactions Chart', key="graph_tabs")

    # Tabs section
    period = ui.tabs(options=['All time', 'Last year', 'Last month',
                     'Year'], default_value='All time', key="period_tabs")

    today = datetime.today()
    year = None
    if period == 'Year':
        year = st.slider('Select year', min_value=2000,
                         max_value=today.year, value=today.year)

    transactions = fetch_transactions_by_period(user_id, period, year)

    if transactions:
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])

        if period == 'Last year':
            df['month'] = df['date'].dt.to_period('M').astype(str)
            x_axis = 'month'
        elif period == 'Last month':
            df['day'] = df['date'].dt.to_period('D').astype(str)
            x_axis = 'day'
        elif period == 'Year':
            df['month'] = df['date'].dt.to_period('M').astype(str)
            x_axis = 'month'
        else:
            df['quarter'] = df['date'].dt.to_period('Q').astype(str)
            x_axis = 'quarter'

        # Summarize transactions per day
        df = df.sort_values(by=['date', 'transaction_id']).groupby(
            'date').last().reset_index()

        if graph_type == 'Transactions Chart':
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['balance'],
                mode='lines+markers',
                fill='tozeroy',  # Fill the area under the line
                marker=dict(color='cyan'),
                line=dict(color='cyan')
            ))

            fig.update_layout(
                title='Transactions Over Time',
                xaxis_title=x_axis.capitalize(),
                yaxis_title='Balance',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False),
                width=1200,  # Set the width of the graph
                height=600  # Set the height of the graph
            )

            st.plotly_chart(fig, use_container_width=True)

        elif graph_type == 'Expenses/Income Histogram':
            transactions_candle = fetch_transactions_for_candles(
                user_id, period, year)
            df_candle = pd.DataFrame(transactions_candle)
            df_candle['date'] = pd.to_datetime(df_candle['date'])

            if period in ['Year', 'All time']:
                df_candle['month'] = df_candle['date'].dt.to_period('M')
                df_expenses = df_candle[df_candle['amount'] < 0].groupby(
                    'month')['amount'].sum().reset_index()
                df_income = df_candle[df_candle['amount'] > 0].groupby(
                    'month')['amount'].sum().reset_index()
                x_axis = 'month'
            else:
                df_candle['day'] = df_candle['date'].dt.to_period('D')
                df_expenses = df_candle[df_candle['amount'] < 0].groupby(
                    'day')['amount'].sum().reset_index()
                df_income = df_candle[df_candle['amount'] > 0].groupby(
                    'day')['amount'].sum().reset_index()
                x_axis = 'day'

            # Convert expenses to positive values for comparison
            df_expenses['amount'] = df_expenses['amount'].abs()

            # Convert amounts to float for y-axis range calculation
            max_expense = float(df_expenses['amount'].max())
            max_income = float(df_income['amount'].max())

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=df_expenses[x_axis].astype(str),
                y=df_expenses['amount'],
                name='Expense',
                marker_color='red'
            ))

            fig.add_trace(go.Bar(
                x=df_income[x_axis].astype(str),
                y=df_income['amount'],
                name='Income',
                marker_color='green'
            ))

            fig.update_layout(
                title='Transactions Candle',
                xaxis_title=x_axis.capitalize(),
                yaxis_title='Amount',
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False),
                # Ensure y-axis starts at 0
                yaxis_range=[0, max(max_expense, max_income) * 1.1],
                width=1200,  # Set the width of the graph
                height=600  # Set the height of the graph
            )

            st.plotly_chart(fig, use_container_width=True)

        elif graph_type == 'Categorized Expenses':
            expenses_by_category = fetch_expenses_by_category(
                user_id, period, year)
            df_expenses = pd.DataFrame(expenses_by_category)

            # Ensure the amounts are positive for the pie chart
            df_expenses['total_amount'] = df_expenses['total_amount'].abs()

            fig = go.Figure(go.Pie(
                labels=df_expenses['category'],
                values=df_expenses['total_amount'],
                hole=.3
            ))

            fig.update_layout(
                title='Transactions Pie Chart',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                width=1200,  # Set the width of the graph
                height=600  # Set the height of the graph
            )

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.write("No transactions found for the selected period.")
