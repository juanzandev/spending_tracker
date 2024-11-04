import streamlit as st
from streamlit_navigation_bar import st_navbar
import pandas as pd
import matplotlib as mt
import decimal
from db.db_functions import insert_transaction, fetch_user_info

def spending_tracker():
    username = st.session_state['username']
    user_info = fetch_user_info(username)
    user_id = user_info['user_id']
    last_balance = user_info['balance']
    st.title("Spending Tracker")
    data_editor = pd.DataFrame(columns=[
                               'date', 'description', 'transaction_type', 'amount', 'category', 'payment_method', 'merchant'])
    transaction_type = ['Credit', 'Debit']
    category = ['Rent', 'Groceries', 'Dining Out',
                'Entertainment', 'Utilities', 'Transportation', 'Salary']
    payment_method = ['Account Transfer', 'Direct Deposit',
                      'Debit Card', 'Credit Card', 'ACH Transfer', 'Online Payment']
    config = {
        'date': st.column_config.DateColumn('Date', width='small', required=True),
        'transaction_type': st.column_config.SelectboxColumn('Transaction Type', options=transaction_type, required=True),
        'amount': st.column_config.NumberColumn('Amount', required=True),
        'description': st.column_config.TextColumn('Description', width='large', required=True),
        'payment_method': st.column_config.SelectboxColumn('Payment Method', options=payment_method, required=True),
        'category': st.column_config.SelectboxColumn('Category', options=category, required=True),
        'merchant': st.column_config.TextColumn('Merchant', required=True)
    }

    add_transaction_table = st.data_editor(
        data_editor, column_config=config, num_rows='dynamic')
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
                        st.success(f"Transaction {
                                   index + 1} added successfully.")
                        # Update last_balance for the next transaction
                        last_balance = new_balance
                    else:
                        st.error(f"Failed to add transaction {index + 1}.")