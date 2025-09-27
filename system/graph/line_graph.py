# line_graph.py (new file to be created)
import os
import pandas as pd
import plotly.express as px
import streamlit as st

def load_data():
    # Construct the path to the CSV file relative to the directory of line_graph.py
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

#TODO: Add unemployement to population graph
def plot_unemployment_graph(df, title, yaxis_title, key):
    """Function to create and display unemployment graphs with smoothing options."""
    with st.expander(f"View {title}", expanded=True):
        st.write(f"## Select Smoothing for {title}")
        smoothing = st.selectbox("Choose Smoothing Option:", ["Default", "6 Months", "1 Year", "4 Years"], key=key)

        # Apply smoothing based on selection
        df_plot = df.copy()
        smoothing_options = {"Default": None, "6 Months": 6, "1 Year": 12, "4 Years": 48}

        if smoothing_options[smoothing]:
            df_plot.iloc[:, 1:] = df_plot.iloc[:, 1:].rolling(window=smoothing_options[smoothing], min_periods=1).mean()
        df_plot = df_plot.dropna()

        # Create the interactive line plot
        fig = px.line(df_plot, x='Date', y=df.columns[1:],
                      labels={'value': yaxis_title, 'variable': 'State'},
                      title=title)

        # Customize layout for better UX
        fig.update_layout(
            title={
                'text': title,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Date",
            yaxis_title=yaxis_title,
            xaxis=dict(
                rangeslider=dict(visible=True),
                type="date"
            ),
            hovermode="x unified",  # Displays hover info for all states at the same x value
            legend_title="State",
            legend=dict(
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.05
            )
        )

        # Update trace appearance and modify the hover template to only display year and month
        fig.update_traces(mode='lines+markers', hovertemplate='%{x|%Y-%m}: %{y:.2f}')

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
