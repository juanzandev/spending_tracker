# inserter.py
import csv
from .connector import connect


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
                for row in reader:
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
        print("Database connection closed.")


def fetch_transactions(username):
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

        user_id = user_id[0]

        transactions_query = "SELECT * FROM transactions WHERE user_id = %s"
        cursor.execute(transactions_query, (user_id,))
        transactions = cursor.fetchall()

        cursor.close()
        return transactions
    except Exception as e:
        print("Error fetching transactions:", e)
        return []
    finally:
        conn.close()
        print("Database connection closed.")
