# test.py (updated version)
import streamlit as st
from graph.line_graph import load_data, plot_unemployment_graph  # Import functions from line_graph.py
from graph.bar_graph import plot_unemployment_bar_graph  # Import function from bar_graph.py
from graph.choropleth_map import plot_choropleth_map_people, plot_choropleth_map_rate  # Import functions from choropleth_map.py
import os

# Streamlit app layout
st.title("Unemployment Rates in Australia and States (1978 - 2024)")

# Load data
df_people, df_rate = load_data()

# Sidebar for graph type selection
st.sidebar.title("Graph Options")
graph_type = st.sidebar.radio("Select Graph Type:", ("Line Graph", "Bar Graph", "Choropleth Map"))

# Display graphs based on the user's selection
if graph_type == "Line Graph":
    plot_unemployment_graph(df_people, "Unemployment Numbers in Australia and States (1978 - 2024)", "Unemployment Number", key='smoothing_numbers')
    plot_unemployment_graph(df_rate, "Unemployment Rates in Australia and States (1978 - 2024)", "Unemployment Rate (%)", key='smoothing_rates')

elif graph_type == "Bar Graph":
    # Plot the first bar graph (Unemployment Numbers)
    plot_unemployment_bar_graph(
        df_people,
        title="Unemployment Numbers in Australian States (1978 - 2024)",
        yaxis_title="Unemployment Number",
        key='bar_graph_numbers',
        value_vars=['New South Wales', 'Victoria', 'Queensland', 'South Australia', 'Western Australia', 'Tasmania', 'Northern Territory', 'Australian Capital Territory'],
        range_y=[0, 500]
    )
    
    # Plot the second bar graph (Unemployment Rates)
    plot_unemployment_bar_graph(
        df_rate,
        title="Unemployment Rates in Australian States (1978 - 2024)",
        yaxis_title="Unemployment Rate (%)",
        key='bar_graph_rates',
        value_vars=['New South Wales', 'Victoria', 'Queensland', 'South Australia', 'Western Australia', 'Tasmania', 'Northern Territory', 'Australian Capital Territory'],
        range_y=[-2, 15]
    )

elif graph_type == "Choropleth Map":
    # Define the path to the GeoJSON file
    base_dir = os.path.dirname(__file__)  # Gets the directory of the current script
    geojson_path = os.path.join(base_dir, "../datatset/australia_states.geojson")  # Adjust relative path
    
    # Display choropleth maps in individual expanders
    plot_choropleth_map_people(df_people, geojson_path)
    plot_choropleth_map_rate(df_rate, geojson_path)