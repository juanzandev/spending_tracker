import streamlit as st
from streamlit_navigation_bar import st_navbar
import pandas as pd
import matplotlib as mt
from .misc.descriptions import *

def about_us():
    
    st.title("About Us")
    st.write("---") #divider

    col1, col2, col3, = st.columns(3)

    with st.container():
        col1.image("images/nolan_pfp.png", use_column_width=True)
        col2.image("images/juan_pfp.png", use_column_width=True)
        col3.image("images/destiny_pfp.png", use_column_width=True)
        col1.markdown(f"<div style='text-align: center;'>{nolanDescription}</div>", unsafe_allow_html=True)
        col2.markdown(f"<div style='text-align: center;'>{juanDescription}</div>", unsafe_allow_html=True)
        col3.markdown(f"<div style='text-align: center;'>{destinyDescription}</div>", unsafe_allow_html=True)

    st.write("---")
    st.markdown(f"<p style='text-align: center;'>{overallDescription}</p>", unsafe_allow_html=True)
