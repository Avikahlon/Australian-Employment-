import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Define base directory and data paths
base_dir = os.path.dirname(__file__)  # Gets the directory of the current script
au_path = os.path.join(base_dir, "../../datatset/au_employment_data.csv")
wa_path = os.path.join(base_dir, "../../datatset/wa_employment_data.csv")

# Load data
def load_employment_data():
    au_data = pd.read_csv(au_path) 
    wa_data = pd.read_csv(wa_path)
    # Rename the "Unnamed: 0" column to "Date" if it exists
    if "Unnamed: 0" in au_data.columns:
        au_data = au_data.rename(columns={"Unnamed: 0": "Date"})
    if "Unnamed: 0" in wa_data.columns:
        wa_data = wa_data.rename(columns={"Unnamed: 0": "Date"})
    
    return au_data, wa_data
#TODO: Add employement to population graph
def plot_stacked_bar_chart(title, au_data, wa_data):
    au_data = au_data.iloc[10:]
    wa_data = wa_data.iloc[10:]
    

    # Convert Date columns to datetime and filter for relevant periods
    au_data["Date"] = pd.to_datetime(au_data["Date"]).dt.date
    wa_data["Date"] = pd.to_datetime(wa_data["Date"]).dt.date

    # Convert Date columns to datetime and filter for relevant periods
    au_data["Date"] = pd.to_datetime(au_data["Date"]).dt.date
    wa_data["Date"] = pd.to_datetime(wa_data["Date"]).dt.date

    if title == "Industry Sector Employment Rate During GFC (2010)": 
        au_data = au_data[au_data["Date"] == pd.to_datetime("2010-02-01").date()]
        wa_data = wa_data[wa_data["Date"] == pd.to_datetime("2010-02-01").date()]

    elif title == "Industry Sector Employment Rate During COVID-19 (2021)": 
        au_data = au_data[au_data["Date"] == pd.to_datetime("2021-02-01").date()]
        wa_data = wa_data[wa_data["Date"] == pd.to_datetime("2021-02-01").date()]

    # Rename columns for both datasets to have consistent, clean names
    au_data.columns = ["Date", "Agriculture", "Mining", "Manufacturing", "Electricity, Gas, Water and Waste Services",
                       "Construction", "Wholesale Trade", "Retail Trade", "Accommodation and Food Services",
                       "Transport, Postal and Warehousing", "Information Media and Telecommunications",
                       "Financial and Insurance Services", "Rental, Hiring and Real Estate Services",
                       "Professional, Scientific and Technical Services", "Administrative and Support Services",
                       "Public Administration and Safety", "Education and Training", "Health Care and Social Assistance",
                       "Arts and Recreation Services", "Other Services", "Employed total"]

    wa_data.columns = ["Date", "Agriculture", "Mining", "Manufacturing", "Electricity, Gas, Water and Waste Services",
                       "Construction", "Wholesale Trade", "Retail Trade", "Accommodation and Food Services",
                       "Transport, Postal and Warehousing", "Information Media and Telecommunications",
                       "Financial and Insurance Services", "Rental, Hiring and Real Estate Services",
                       "Professional, Scientific and Technical Services", "Administrative and Support Services",
                       "Public Administration and Safety", "Education and Training", "Health Care and Social Assistance",
                       "Arts and Recreation Services", "Other Services", "Employed total"]

    # Convert all columns except 'Date' to numeric, coercing errors
    for col in au_data.columns[1:]:
        au_data[col] = pd.to_numeric(au_data[col], errors='coerce')
        wa_data[col] = pd.to_numeric(wa_data[col], errors='coerce')

    # Fill NaN values with 0
    au_data = au_data.fillna(0)
    wa_data = wa_data.fillna(0)

    # Calculate employment rate for each industry
    au_data_rate = au_data.copy()
    wa_data_rate = wa_data.copy()
    for col in au_data.columns[1:-1]:  # Exclude 'Date' and 'Employed total'
        au_data_rate[col] = (au_data[col] / au_data["Employed total"]) * 100
        wa_data_rate[col] = (wa_data[col] / wa_data["Employed total"]) * 100

    # Drop the total column as it's no longer needed
    au_data_rate = au_data_rate.drop(columns="Employed total")
    wa_data_rate = wa_data_rate.drop(columns="Employed total")

    # Melt data to have a tidy format suitable for grouped bars
    au_melted = au_data_rate.melt(id_vars="Date", var_name="Industry", value_name="Australia Rate")
    wa_melted = wa_data_rate.melt(id_vars="Date", var_name="Industry", value_name="Western Australia Rate")

    # Merge melted data for easier plotting
    merged_melted = pd.merge(au_melted, wa_melted, on=["Date", "Industry"])

    # Plot stacked bar chart
    with st.expander(title, expanded=True):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=merged_melted["Industry"],
            x=merged_melted["Australia Rate"],
            name="Australia",
            orientation='h',
            marker_color='gray'
        ))
        fig.add_trace(go.Bar(
            y=merged_melted["Industry"],
            x=merged_melted["Western Australia Rate"],
            name="Western Australia",
            orientation='h',
            marker_color='red'
        ))
        fig.update_layout(
            barmode='group',
            title=title,
            yaxis=dict(title='Industry', tickangle=0),
            xaxis=dict(title='% of Employed Persons Aged 15+', showticklabels=False),
            legend=dict(title='Region'),
            hovermode='y unified'
        )
        st.plotly_chart(fig, use_container_width=True)