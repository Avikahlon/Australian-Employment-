import streamlit as st
from graph.stacked_bar import load_employment_data, plot_stacked_bar_chart


def show_case_study():

    # Load employment data
    au_data, wa_data = load_employment_data()
    
    # Plot stacked bar chart for GFC period
    plot_stacked_bar_chart("Industry Sector Employment Rate During GFC (2010)", au_data, wa_data)

    with st.expander("Industry Sector Employment Rate During GFC (2010)", expanded=True):
        st.subheader("Key Insights")
        st.write("- During the GFC (2008), Western Australia's employment rate was relatively more volatile compared to the national average due to its reliance on the mining sector.")

    # Plot stacked bar chart for COVID-19 period
    plot_stacked_bar_chart("Industry Sector Employment Rate During COVID-19 (2021)", au_data, wa_data)

    with st.expander("Industry Sector Employment Rate During COVID-19 (2021)", expanded=True):
        st.subheader("Key Insights")
        st.write("""
        - The COVID-19 recession (2020 - 2024) had a significant impact on both Australia and Western Australia, but Western Australia's employment rate showed quicker signs of recovery, reflecting its resource-driven economy.
        - Despite quicker recoveries, Western Australia's economic dependence on global commodity demand makes it vulnerable to future global economic downturns.
        """)
