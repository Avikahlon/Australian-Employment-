# choropleth_map.py (updated version)
import os
import pandas as pd
import plotly.graph_objects as go
import json
import streamlit as st

def load_data_map():
    # Construct the path to the CSV file relative to the directory of choropleth_map.py
    base_dir = os.path.dirname(__file__)  # Gets the directory of the current script
    file_path = os.path.join(base_dir, "../../datatset/unemployment_of_all_states.csv")  # Adjust relative path

    # Load the dataset
    df = pd.read_csv(file_path)

    # Select data from the 11th row onward (index 10) and reset the index
    df = df.iloc[9:].reset_index(drop=True)

    # Split the dataset into two DataFrames for total number of unemployed people and unemployment rate
    df_people = df.iloc[:, [0 , 2, 3, 4, 5, 6, 7, 8, 9]]
    df_rate = df.iloc[:, [0, 83, 84, 85, 86, 87, 88, 89, 90]]

    # Rename the columns for easier reference
    columns_people = ['Date', 'New South Wales', 'Victoria', 'Queensland',
                      'South Australia', 'Western Australia', 'Tasmania',
                      'Northern Territory', 'Australian Capital Territory']
    columns_rate = ['Date', 'New South Wales', 'Victoria', 'Queensland',
                    'South Australia', 'Western Australia', 'Tasmania',
                    'Northern Territory', 'Australian Capital Territory']
    df_people.columns = columns_people
    df_rate.columns = columns_rate

    # Convert 'Date' column to datetime format
    df_people['Date'] = pd.to_datetime(df_people['Date'], format='%Y-%m-%d %H:%M:%S')
    df_rate['Date'] = pd.to_datetime(df_rate['Date'], format='%Y-%m-%d %H:%M:%S')

    # Convert the rest of the columns to numeric, coercing errors
    for col in columns_people[1:]:
        df_people[col] = pd.to_numeric(df_people[col], errors='coerce')
    for col in columns_rate[1:]:
        df_rate[col] = pd.to_numeric(df_rate[col], errors='coerce')

    return df_people, df_rate

def plot_choropleth_map(df, geojson_path, graph_type):
    """Function to create and display choropleth maps of unemployment data."""
    with st.expander(f"View Choropleth Map: {graph_type}", expanded=True):
        # Load GeoJSON data for Australian states
        with open(geojson_path) as f:
            aus_geojson = json.load(f)

        if graph_type == "Total Number of Unemployed People (1978-2024)":
            df_data = df
            zmax_value = 320
            title_text = "Interactive Choropleth Map of Total Number of Unemployed People (1978-2024)"
            date_range = pd.date_range(start='1978-01-01', end='2024-8-31', freq='Y')

        elif graph_type == "Unemployment Rate (1978-2024)":
            df_data = df
            zmax_value = 14
            title_text = "Interactive Choropleth Map of Unemployment Rate (1978-2024)"
            date_range = pd.date_range(start='1978-01-01', end='2024-8-31', freq='Y')

        elif graph_type == "Total Number of Unemployed People during GFC (2008-2012)":
            df_data = df
            zmax_value = 200
            title_text = "Interactive Choropleth Map of Total Number of Unemployed People during Global Financial Crisis (2008-2012)"
            date_range = pd.date_range(start='2008-01-01', end='2012-12-31', freq='M')

        elif graph_type == "Unemployment rate during GFC (2008-2012)":
            df_data = df
            zmax_value = 8
            title_text = "Interactive Choropleth Map of Unemployment rate during Global Financial Crisis (2008-2012)"
            date_range = pd.date_range(start='2008-01-01', end='2012-12-31', freq='M')

        elif graph_type == "Total Number of Unemployed People during COVID-19 (2020-2024)":
            df_data = df
            zmax_value = 200
            title_text = "Interactive Choropleth Map of Unemployment rate during Global Financial Crisis (2008-2012)"
            date_range = pd.date_range(start='2008-01-01', end='2012-12-31', freq='M')

        elif graph_type ==  "Unemployment Rate during COVID-19 (2020-2024)":
            df_data = df
            zmax_value = 8
            title_text = "Interactive Choropleth Map of Unemployment rate during Global Financial Crisis (2008-2012)"
            date_range = pd.date_range(start='2008-01-01', end='2012-12-31', freq='M')

        # Create frames for each date in the specified date range
        frames = []
        for date in date_range:
            df_period = df_data[df_data['Date'].dt.to_period('M') == date.to_period('M')].mean(skipna=True).to_frame().reset_index()
            df_period.columns = ['State', 'Average Value']
            choropleth = go.Choroplethmapbox(
                geojson=aus_geojson,
                locations=df_period['State'],
                featureidkey='properties.name',
                z=df_period['Average Value'], zmin=0, zmax=zmax_value,
                colorscale='Portland',
                autocolorscale=False,
                marker_line_width=1,
                marker_opacity=0.8,
                text=df_period['State'],
                hovertemplate="<b>%{text}</b><br>Average Value: %{z}<br><extra></extra>"
            )
            frames.append(go.Frame(data=[choropleth], name=str(date)[:7]))
        layout = go.Layout(
            title={'text': title_text, 'font': {'size': 15}},
            mapbox=dict(
                center=dict(lat=-25.0, lon=133.0),
                zoom=3.5,
                style="carto-positron",
                accesstoken="YOUR_MAPBOX_ACCESS_TOKEN",
            ),
            autosize=True,
            height=600,
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    buttons=[
                        dict(label="Play",
                             method="animate",
                             args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)]),
                        dict(label="Pause",
                             method="animate",
                             args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])
                    ]
                )
            ],
            sliders=[
                dict(
                    steps=[
                        dict(method='animate',
                             args=[[str(date)[:7]], dict(mode='immediate', frame=dict(duration=500, redraw=True))],
                             label=str(date)[:7]) for date in date_range
                    ],
                    active=0
                )
            ]
        )
        fig = go.Figure(data=[frames[0].data[0]], layout=layout, frames=frames)

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)