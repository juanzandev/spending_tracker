#
import streamlit as st
from utils.config import set_app_config
set_app_config()
from styles.nav_bar_styles import styles
from streamlit_navigation_bar import st_navbar
import pages as pg

# Top navigation bar setup
page = st_navbar(
    ["Get Started","Dashboard", "Spending Analyzer", "Spending Tracker", "About Us"],
    styles=styles, logo_page="Dashboard", logo_path="images/syntax_society_logo_only.svg",
    options={"show_menu": True, "show_sidebar": True, "hide_nav": True}
)

st.sidebar.image("images/syntax_society_logo.svg", width=None)
with st.sidebar:
    dashboard_button = st.button("Dashboard")
    get_started_button = st.button("Get Started")
    spending_analyzer_button = st.button("Spending Analyzer")
    spending_tracker_button = st.button("Spending Tracker")
    about_us_button = st.button("About Us")
pg.login()

if st.session_state['authentication_status']:

    # Load the custom HTML styling
    with open("styles/source.html", "r") as file:
        html_style = file.read()
    st.html(html_style)

    # Sidebar navigation using buttons
    
    if 'page' not in st.session_state:
        st.session_state.page = "Get Started"
        
    if dashboard_button:
        page = "Dashboard"
    elif spending_analyzer_button:
        page = "Spending Analyzer"
    elif get_started_button:
        page = "Get Started"
    elif spending_tracker_button:
        page = "Spending Tracker"
    elif about_us_button:
        page = "About Us"

    # Display the content based on either the navbar or sidebar button click
    if page == "Dashboard" or dashboard_button:
        pg.dashboard()
    elif page == "Spending Analyzer" or spending_analyzer_button:
        pg.spending_score()
    elif page == "Get Started" or get_started_button:
        pg.get_started()
    elif page == "Spending Tracker" or spending_tracker_button:
        pg.spending_tracker()
    elif page == "About Us" or about_us_button:
        pg.about_us()
