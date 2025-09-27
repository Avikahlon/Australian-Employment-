# covid.py
import streamlit as st
from graph.line_graph import load_data, plot_unemployment_graph
from graph.bar_graph import plot_unemployment_bar_graph
from graph.choropleth_map import plot_choropleth_map, load_data_map
import os

# Function to display the section on the COVID-19 Recession
def show_covid_section():
    st.header("2020 - 2024 COVID-19 Recession")

    # Load data
    df1, df2 = load_data()  # df1 is the total number of unemployed people, df2 is the unemployment rate

    # Filter data for the COVID-19 period (2020 - 2024)
    df1_covid = df1[(df1['Date'].dt.year >= 2020) & (df1['Date'].dt.year <= 2024)].reset_index(drop=True)
    df2_covid = df2[(df2['Date'].dt.year >= 2020) & (df2['Date'].dt.year <= 2024)].reset_index(drop=True)

    # Line Graph - Total Number of Unemployed People
    st.subheader("Line Graph - Total Number of Unemployed People (2020 - 2024)")
    plot_unemployment_graph(df1_covid, "Total Number of Unemployed People in Australia during COVID-19 Recession (2020 - 2024)", "Unemployment Number", key='covid_total_unemployed_line')

    # Line Graph - Unemployment Rate
    st.subheader("Line Graph - Unemployment Rate (2020 - 2024)")
    plot_unemployment_graph(df2_covid, "Unemployment Rate in Australia during COVID-19 Recession (2020 - 2024)", "Unemployment Rate (%)", key='covid_unemployment_rate_line')

    # Bar Graph - Total Number of Unemployed People
    st.subheader("Bar Graph - Total Number of Unemployed People (2020 - 2024)")
    plot_unemployment_bar_graph(
        df1_covid,
        title="Total Number of Unemployed People in Australian States during COVID-19 Recession (2020 - 2024)",
        yaxis_title="Unemployment Number",
        key='covid_total_unemployed_bar',
        value_vars=['New South Wales', 'Victoria', 'Queensland', 'South Australia', 'Western Australia', 'Tasmania', 'Northern Territory', 'Australian Capital Territory'],
        range_y=[0, 500]
    )

    # Bar Graph - Unemployment Rate
    st.subheader("Bar Graph - Unemployment Rate (2020 - 2024)")
    plot_unemployment_bar_graph(
        df2_covid,
        title="Unemployment Rate in Australian States during COVID-19 Recession (2020 - 2024)",
        yaxis_title="Unemployment Rate (%)",
        key='covid_unemployment_rate_bar',
        value_vars=['New South Wales', 'Victoria', 'Queensland', 'South Australia', 'Western Australia', 'Tasmania', 'Northern Territory', 'Australian Capital Territory'],
        range_y=[0, 15]
    )

    # Choropleth Map - Total Number of Unemployed People
    st.subheader("Choropleth Map - Total Number of Unemployed People (2020 - 2024)")
    base_dir = os.path.dirname(__file__)
    geojson_path = os.path.join(base_dir, "../../datatset/australia_states.geojson")
    df1_map, df2_map = load_data_map()
    plot_choropleth_map(df1_map, geojson_path, "Total Number of Unemployed People during COVID-19 (2020-2024)")

    # Choropleth Map - Unemployment Rate
    st.subheader("Choropleth Map - Unemployment Rate (2020 - 2024)")
    plot_choropleth_map(df2_map, geojson_path, "Unemployment Rate during COVID-19 (2020-2024)")
