# intro.py
import streamlit as st
from streamlit_elements import elements, mui, dashboard

def show_intro():
    # Define the layout for draggable and resizable elements
    layout = [
        dashboard.Item("project_overview", x=0, y=0, w=6, h=2),
        dashboard.Item("technologies_used", x=6, y=0, w=6, h=2),
        dashboard.Item("team_introduction", x=0, y=2, w=6, h=2),
        dashboard.Item("datasets", x=6, y=2, w=6, h=2)
    ]

    # Begin the `streamlit-elements` session
    with elements("intro_dashboard"):
        # Create a draggable, resizable dashboard with more columns for better resizing
        with dashboard.Grid(layout, maxColumns=12, draggableHandle=".draggable-handle", style={"width": "100%"}):
            
            # Project Overview Card
            with mui.Paper(key="project_overview", elevation=3, style={"padding": "20px"}):
                mui.Typography("Project Overview", variant="h5", className="draggable-handle")
                mui.Typography("""
                    This project provides an analysis of unemployment in Australia from 1978 to 2024.
                    It includes interactive visualisations of unemployment data across different states,
                    using line graphs, bar graphs, and choropleth maps.
                """)
            
            # Technologies Used Card
            with mui.Paper(key="technologies_used", elevation=3, style={"padding": "20px"}):
                mui.Typography("Technologies Used", variant="h5", className="draggable-handle")
                mui.Typography("""
                    - Python
                    - Streamlit
                    - Plotly
                    - Pandas
                """)
            
            # Team Introduction Card
            with mui.Paper(key="team_introduction", elevation=3, style={"padding": "20px"}):
                mui.Typography("Team Introduction", variant="h5", className="draggable-handle")
                mui.Typography("""
                    This project was created by a dedicated team of data enthusiasts who study at Murdoch University with a passion for
                    understanding economic trends and their impact on society. (just wanna secure a job after Grad : ( 
                """)
            
            # Datasets Card
            with mui.Paper(key="datasets", elevation=3, style={"padding": "20px"}):
                mui.Typography("Datasets", variant="h5", className="draggable-handle")
                mui.Button("Download Unemployment Dataset - Industry Data", variant="contained", color="primary")
                mui.Button("Download Unemployment Dataset - Labour Force", variant="contained", color="primary")
                mui.Button("Download Unemployment Dataset - All States", variant="contained", color="primary")
