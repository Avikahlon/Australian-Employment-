# bar_graph.py (new file to be created)
import os
import pandas as pd
import plotly.express as px
import streamlit as st

def load_data():
    # Construct the path to the CSV file relative to the directory of bar_graph.py
    base_dir = os.path.dirname(__file__)  # Gets the directory of the current script
    file_path = os.path.join(base_dir, "../../datatset/unemployment_of_all_states.csv")  # Adjust relative path

    # Load the dataset
    df = pd.read_csv(file_path)

    # Select data from the 11th row onward (index 10) and reset the index
    df = df.iloc[9:].reset_index(drop=True)

    # Select the relevant columns (Date, and unemployment data for Australia and states)
    df_person = df.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    df_rate = df.iloc[:, [0, 82, 83, 84, 85, 86, 87, 88, 89, 90]]

    # Rename the columns for easier reference
    columns = ['Date', 'Australia', 'New South Wales', 'Victoria', 'Queensland',
               'South Australia', 'Western Australia', 'Tasmania',
               'Northern Territory', 'Australian Capital Territory']
    df_person.columns = columns
    df_rate.columns = columns

    # Convert 'Date' column to datetime format for both dataframes
    df_person['Date'] = pd.to_datetime(df_person['Date'], format='%Y-%m-%d %H:%M:%S')
    df_rate['Date'] = pd.to_datetime(df_rate['Date'], format='%Y-%m-%d %H:%M:%S')

    # Convert the rest of the columns to numeric, coercing errors
    for col in columns[1:]:
        df_person[col] = pd.to_numeric(df_person[col], errors='coerce')
        df_rate[col] = pd.to_numeric(df_rate[col], errors='coerce')

    return df_person, df_rate

def plot_unemployment_bar_graph(df, title, yaxis_title, key, value_vars, range_y):
    """Function to create and display unemployment bar graphs with animation."""
    with st.expander(f"View {title}", expanded=True):
        # Extract year from Date and add as a separate column
        df['Year'] = df['Date'].dt.year

        # Melt the dataframe to create a long format suitable for animation
        melted_df = df.melt(id_vars=['Year'], value_vars=value_vars, var_name='State', value_name=yaxis_title)

        # Create a bar plot with animation for each state
        fig = px.bar(melted_df, x='State', y=yaxis_title, color='State',
                     animation_frame='Year', animation_group='State', range_y=range_y,
                     title=title,
                     labels={yaxis_title: yaxis_title})

        # Customize layout for better UX
        fig.update_layout(
            title={
                'text': title,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            hovermode="x unified",  # Displays hover info for all states at the same x value
            legend_title="State",
            legend=dict(
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.05
            ),
            margin=dict(t=100, b=150)  # Add more space between the graph and the slider bar
        )

        # Remove the x-axis title
        fig.update_xaxes(title=None)

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
