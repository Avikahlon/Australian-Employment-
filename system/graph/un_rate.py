# un_rate.py
import streamlit as st
from graph.line_graph import load_data, plot_unemployment_graph
from graph.bar_graph import plot_unemployment_bar_graph
from graph.choropleth_map import plot_choropleth_map, load_data_map
import os


def show_unemployment_rate():
    st.header("1978 - 2024 Unemployment Rate of All States in Australia")

    # Load data
    _, df2 = load_data()  # df2 is the unemployment rate

    # Line Graph
    st.subheader("Line Graph")
    plot_unemployment_graph(df2, "Unemployment Rate in Australia (1978 - 2024)", "Unemployment Rate (%)", key='unemployment_rate_line')

    # Bar Graph
    st.subheader("Bar Graph")
    plot_unemployment_bar_graph(
        df2,
        title="Unemployment Rate in Australian States (1978 - 2024)",
        yaxis_title="Unemployment Rate (%)",
        key='unemployment_rate_bar',
        value_vars=['Australia', 'New South Wales', 'Victoria', 'Queensland', 'South Australia', 'Western Australia', 'Tasmania', 'Northern Territory', 'Australian Capital Territory'],
        range_y=[-2, 15]
    )

    # Choropleth Map
    st.subheader("Choropleth Map")
    base_dir = os.path.dirname(__file__)
    geojson_path = os.path.join(base_dir, "../../datatset/australia_states.geojson")
    plot_choropleth_map(df2, geojson_path, "Unemployment Rate (1978-2024)")
