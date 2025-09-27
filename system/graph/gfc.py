# gfc.py
import streamlit as st
from graph.line_graph import load_data, plot_unemployment_graph
from graph.bar_graph import plot_unemployment_bar_graph
from graph.choropleth_map import plot_choropleth_map, load_data_map
import os


def show_gfc_section():
    st.header("2008 - 2012 Global Financial Crisis: Unemployment Analysis")

    # Load data
    df1, df2 = load_data()  # df1 is the total number of unemployed people, df2 is the unemployment rate

    # Filter the data for the years 2008 to 2012
    df1_gfc = df1[(df1['Date'].dt.year >= 2008) & (df1['Date'].dt.year <= 2012)]
    df2_gfc = df2[(df2['Date'].dt.year >= 2008) & (df2['Date'].dt.year <= 2012)]

    # Line Graph - Total Number of Unemployed People
    st.subheader("Line Graph: Total Number of Unemployed People (2008 - 2012)")
    plot_unemployment_graph(df1_gfc, "Total Number of Unemployed People during GFC (2008 - 2012)", "Unemployment Number", key='gfc_total_unemployed_line')

    # Line Graph - Unemployment Rate
    st.subheader("Line Graph: Unemployment Rate (2008 - 2012)")
    plot_unemployment_graph(df2_gfc, "Unemployment Rate during GFC (2008 - 2012)", "Unemployment Rate (%)", key='gfc_unemployment_rate_line')

    # Bar Graph - Total Number of Unemployed People
    st.subheader("Bar Graph: Total Number of Unemployed People (2008 - 2012)")
    plot_unemployment_bar_graph(
        df1_gfc,
        title="Total Number of Unemployed People in Australian States during GFC (2008 - 2012)",
        yaxis_title="Unemployment Number",
        key='gfc_total_unemployed_bar',
        value_vars=['New South Wales', 'Victoria', 'Queensland', 'South Australia', 'Western Australia', 'Tasmania', 'Northern Territory', 'Australian Capital Territory'],
        range_y=[0, 500]
    )

    # Bar Graph - Unemployment Rate
    st.subheader("Bar Graph: Unemployment Rate (2008 - 2012)")
    plot_unemployment_bar_graph(
        df2_gfc,
        title="Unemployment Rate in Australian States during GFC (2008 - 2012)",
        yaxis_title="Unemployment Rate (%)",
        key='gfc_unemployment_rate_bar',
        value_vars=['Australia', 'New South Wales', 'Victoria', 'Queensland', 'South Australia', 'Western Australia', 'Tasmania', 'Northern Territory', 'Australian Capital Territory'],
        range_y=[-2, 15]
    )

    # Choropleth Map
    st.subheader("Choropleth Map: Unemployment during GFC (2008 - 2012)")
    base_dir = os.path.dirname(__file__)
    geojson_path = os.path.join(base_dir, "../../datatset/australia_states.geojson")
    df1_map, df2_map = load_data_map()
    plot_choropleth_map(df1_map, geojson_path, "Total Number of Unemployed People during GFC (2008-2012)")
    plot_choropleth_map(df2_map, geojson_path, "Unemployment rate during GFC (2008-2012)")
