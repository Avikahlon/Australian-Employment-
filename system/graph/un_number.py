# un_number.py
import streamlit as st
from graph.line_graph import load_data, plot_unemployment_graph
from graph.bar_graph import plot_unemployment_bar_graph
from graph.choropleth_map import plot_choropleth_map, load_data_map
import os

def show_unemployment_numbers():
    st.header("1978 - 2025 Total Number of Unemployed People in All States of Australia")

    # Load data
    df1, _ = load_data()  # df1 is the total number of unemployed people

    # Line Graph
    st.subheader("Line Graph")
    plot_unemployment_graph(df1, "Total Number of Unemployed People in Australia (1978 - 2025)", "Unemployment Number (thousand)", key='total_unemployed_line')

    # Bar Graph
    st.subheader("Bar Graph")
    plot_unemployment_bar_graph(
        df1,
        title="Total Number of Unemployed People in Australian States (1978 - 2025)",
        yaxis_title="Unemployment Number (thousand)",
        key='total_unemployed_bar',
        value_vars=['New South Wales', 'Victoria', 'Queensland', 'South Australia', 'Western Australia', 'Tasmania', 'Northern Territory', 'Australian Capital Territory'],
        range_y=[0, 500]
    )

    # Choropleth Map
    st.subheader("Choropleth Map")
    base_dir = os.path.dirname(__file__)
    geojson_path = os.path.join(base_dir, "../../datatset/australia_states.geojson")
    df1, _ = load_data_map()
    plot_choropleth_map(df1, geojson_path, "Total Number of Unemployed People (1978-2025)")
