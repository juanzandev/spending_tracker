import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import psycopg2
from db.config import config

# Function to insert new user into the database


def insert_new_user(name, email, username):
    """Insert a new user into the database with name, email, and username."""
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        # Insert the new user with username
        insert_query = """
        INSERT INTO Users (name, email, username)
        VALUES (%s, %s, %s)
        ON CONFLICT (email) DO NOTHING;
        """
        cursor.execute(insert_query, (name, email, username))
        connection.commit()

        cursor.close()
        connection.close()
        print(f"Added User {name} Correctly")
    except (Exception, psycopg2.DatabaseError) as error:
        st.error(f"Error inserting new user: {error}")


def login():
    with open(r'pages\utils\user_config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    cols = st.columns(2)

    # Login [widget]
    with cols[0]:
        try:
            authenticator.login()
        except Exception as e:
            st.error(e)

    # Authenticate users
    if st.session_state['authentication_status']:
        authenticator.logout(location="sidebar")
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')

    # Forgot password [widget]
    if not st.session_state['authentication_status']:
        with cols[1]:
            try:
                username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password()
                if username_of_forgotten_password:
                    st.success('New password to be sent securely')
                elif username_of_forgotten_password == False:
                    st.error('Username not found')
            except Exception as e:
                st.error(e)

    # Register new users [widget]
    if not st.session_state['authentication_status']:
        try:
            email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
                pre_authorized=config['pre-authorized']['emails'])
            if email_of_registered_user:
                st.success('User registered successfully')

                # Add the newly registered user to the database
                insert_new_user(name_of_registered_user,
                                email_of_registered_user,
                                username_of_registered_user)
        except Exception as e:
            st.error(e)

    # Update configuration file after modification
    with open(r'pages\utils\user_config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
