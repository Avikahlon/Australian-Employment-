# main.py
import streamlit as st

# Set Streamlit page configuration to use wide layout
st.set_page_config(layout="wide")

# Updated CSS to enforce a max width for the main content area
st.markdown("""
    <style>
    .main-content {
        width: 60vw;
        max-width: 1145px;
        margin: auto;
    }
    .stApp {
        overflow: hidden;
    }
    .main-content .stPlotlyChart {
        width: 100% !important;
        max-width: 1145px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Importing the independent modules for each section
from graph.intro import show_intro
from graph.un_number import show_unemployment_numbers
from graph.un_rate import show_unemployment_rate
from graph.gfc import show_gfc_section
from graph.covid import show_covid_section
from graph.case import show_case_study

# Streamlit app layout
st.title("Unemployment Analysis in Australia (1978 - 2024)")

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select Section:", [
    "Introduction",
    "1978 - 2024 Total Number of Unemployed People in All States of Australia",
    "1978 - 2024 Unemployment Rate of All States in Australia",
    "2008 - 2012 Global Financial Crisis",
    "2020 - 2024 Covid-19 Recession",
    "Case Study"
])

# Wrap content in a centered container
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Display content based on the selected section
    if options == "Introduction":
        show_intro()
    elif options == "1978 - 2024 Total Number of Unemployed People in All States of Australia":
        show_unemployment_numbers()
    elif options == "1978 - 2024 Unemployment Rate of All States in Australia":
        show_unemployment_rate()
    elif options == "2008 - 2012 Global Financial Crisis":
        show_gfc_section()
    elif options == "2020 - 2024 Covid-19 Recession":
        show_covid_section()
    elif options == "Case Study":
        show_case_study()

    st.markdown('</div>', unsafe_allow_html=True)
