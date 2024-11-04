import csv
from .connector import connect
from datetime import datetime, timedelta


def insert_transactions_from_csv(user_id, csv_file_path):
    # Connect to the database
    conn = connect()
    if conn is None:
        print("Connection to the database failed.")
        return

    try:
        print(f"Inserting transactions for user_id: {user_id}")

        # Open the CSV file and insert transactions
        with conn.cursor() as cur:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                # Read all rows into a list to preserve order
                transactions = list(reader)

                for row in transactions:
                    cur.execute("""
                        INSERT INTO transactions (user_id, date, description, transaction_type, amount, category, payment_method, merchant, balance)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, (
                        user_id,
                        row['Date'],
                        row['Description'],
                        row['Transaction Type'],
                        float(row['Amount']),
                        row['Category'],
                        row['Payment Method'],
                        row['Merchant'],
                        float(row['Balance'])
                    ))
            conn.commit()
            print("Transactions inserted successfully.")

    except Exception as e:
        print("Error inserting transactions:", e)
    finally:
        conn.close()
        # print("Database connection closed.")


def fetch_transactions(username, limit=None, order='DESC'):
    conn = connect()
    if conn is None:
        print("Connection to the database failed.")
        return []

    try:
        cursor = conn.cursor()
        user_query = "SELECT user_id FROM users WHERE username = %s"
        cursor.execute(user_query, (username,))
        user_id = cursor.fetchone()

        if user_id is None:
            print("User not found")
            return []

        user_id = user_id[0]

        if order not in ['ASC', 'DESC']:
            print("Invalid order parameter. Use 'ASC' or 'DESC'.")
            return []

        if limit is None:
            transactions_query = f"""
                SELECT date, description, transaction_type, amount, category, payment_method, merchant, balance
                FROM transactions
                WHERE user_id = %s
                ORDER BY date {order}, transaction_id {order}
            """
            cursor.execute(transactions_query, (user_id,))
        else:
            transactions_query = f"""
                SELECT date, description, transaction_type, amount, category, payment_method, merchant, balance
                FROM transactions
                WHERE user_id = %s
                ORDER BY date {order}, transaction_id {order}
                LIMIT %s
            """
            cursor.execute(transactions_query, (user_id, limit))

        transactions = cursor.fetchall()
        cursor.close()
        return transactions

    except Exception as e:
        print("Error fetching transactions:", e)
        return []
    finally:
        conn.close()
        # print("Database connection closed.")


def insert_transaction(user_id, date, description, transaction_type, amount, category, payment_method, merchant, balance):
    conn = connect()
    if conn is None:
        print("Connection to the database failed.")
        return False

    try:
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO transactions (user_id, date, description, transaction_type, amount, category, payment_method, merchant, balance)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, date, description, transaction_type,
                       amount, category, payment_method, merchant, balance))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print("Error inserting transaction:", e)
        return False
    finally:
        conn.close()
        # print("Database connection closed.")


def fetch_user_info(username):
    conn = connect()
    if conn is None:
        print("Connection to the database failed.")
        return None

    try:
        cursor = conn.cursor()
        query = """
            SELECT u.user_id, 
                   (SELECT score FROM Spending_Scores WHERE user_id = u.user_id ORDER BY updated_at DESC LIMIT 1) AS spending_score,
                   (SELECT balance FROM transactions WHERE user_id = u.user_id ORDER BY date DESC LIMIT 1) AS balance,
                   (SELECT monthly_limit FROM Budgets WHERE user_id = u.user_id ORDER BY date DESC, budget_id DESC LIMIT 1) AS latest_budget
            FROM users u
            WHERE u.username = %s
        """
        cursor.execute(query, (username,))
        user_info = cursor.fetchone()
        cursor.close()
        if user_info:
            return {
                "user_id": user_info[0],
                "spending_score": user_info[1] if user_info[1] is not None else 0,
                "balance": user_info[2] if user_info[2] is not None else 0,
                "latest_budget": user_info[3] if user_info[3] is not None else 0
            }
        else:
            return None
    except Exception as e:
        print("Error fetching user info:", e)
        return None
    finally:
        conn.close()
        # print("Database connection closed.")


def add_budget(user_id, monthly_limit):
    conn = connect()
    if conn is None:
        print("Connection to the database failed.")
        return False

    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO Budgets (user_id, monthly_limit, date)
            VALUES (%s, %s, CURRENT_DATE)
        """
        cursor.execute(query, (user_id, monthly_limit))
        conn.commit()
        cursor.close()
        print("Budget added successfully.")
        return True
    except Exception as e:
        print("Error adding budget:", e)
        return False
    finally:
        conn.close()
        # print("Database connection closed.")


def calculate_user_spending_last_month(user_id):
    conn = connect()
    if conn is None:
        print("Connection to the database failed.")
        return None

    try:
        cursor = conn.cursor()
        # Calculate the first and last day of the previous month
        today = datetime.today()
        first_day_last_month = (today.replace(
            day=1) - timedelta(days=1)).replace(day=1)
        last_day_last_month = today.replace(day=1) - timedelta(days=1)

        query = """
            SELECT ABS(SUM(amount))
            FROM transactions
            WHERE user_id = %s
              AND date >= %s
              AND date <= %s
              AND amount < 0
        """
        cursor.execute(
            query, (user_id, first_day_last_month, last_day_last_month))
        budget_used = cursor.fetchone()[0]
        cursor.close()
        return float(budget_used) if budget_used is not None else 0.0
    except Exception as e:
        print("Error calculating user spending:", e)
        return 0.0
    finally:
        conn.close()
        # print("Database connection closed.")


def calculate_user_spending_current_month(user_id):
    conn = connect()
    if conn is None:
        print("Connection to the database failed.")
        return None

    try:
        cursor = conn.cursor()
        # Calculate the first and last day of the current month
        today = datetime.today()
        first_day_current_month = today.replace(day=1)
        last_day_current_month = (today.replace(
            day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        query = """
            SELECT ABS(SUM(amount))
            FROM transactions
            WHERE user_id = %s
              AND date >= %s
              AND date <= %s
              AND amount < 0
        """
        cursor.execute(
            query, (user_id, first_day_current_month, last_day_current_month))
        budget_used = cursor.fetchone()[0]
        cursor.close()
        return float(f"{budget_used:.2f}") if budget_used is not None else 0.0
    except Exception as e:
        print("Error calculating user spending:", e)
        return 0.0
    finally:
        conn.close()
        # print("Database connection closed.")
