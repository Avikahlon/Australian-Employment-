# helper.py
import os
import pandas as pd

# Function to load the dataset
# This function is shared by different modules to load data
# and avoid redundancy in code

def load_data():
    base_dir = os.path.dirname(__file__)  # Gets the directory of the current script
    file_path = os.path.join(base_dir, "../../datatset/unemployment_of_all_states.csv")  # Adjust relative path

    # Load the dataset
    df = pd.read_csv(file_path)

    # Select data from the 11th row onward (index 10) and reset the index
    df = df.iloc[9:].reset_index(drop=True)

    # Split the dataset into DataFrames for total number of unemployed people, unemployment rate, and including Australia
    df_people_choropleth = df.iloc[:, [0, 2, 3, 4, 5, 6, 7, 8, 9]]
    df_rate_choropleth = df.iloc[:, [0, 83, 84, 85, 86, 87, 88, 89, 90]]
    df_people_line_bar = df.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    df_rate_line_bar = df.iloc[:, [0, 82, 83, 84, 85, 86, 87, 88, 89, 90]]

    # Rename the columns for easier reference
    columns_people = ['Date', 'New South Wales', 'Victoria', 'Queensland', 'South Australia', 
                      'Western Australia', 'Tasmania', 
                      'Northern Territory', 'Australian Capital Territory']
    columns_rate = ['Date', 'New South Wales', 'Victoria', 'Queensland', 'South Australia', 
              'Western Australia', 'Tasmania', 'Northern Territory', 'Australian Capital Territory']
    columns_people_line_bar = ['Date', 'Australia', 'New South Wales', 'Victoria', 'Queensland', 'South Australia',
                               'Western Australia', 'Tasmania', 'Northern Territory', 'Australian Capital Territory']
    columns_rate_line_bar = ['Date', 'Australia', 'New South Wales Rate', 'Victoria Rate', 'Queensland Rate',
                             'South Australia Rate', 'Western Australia Rate', 'Tasmania Rate', 'Northern Territory Rate', 'Australian Capital Territory Rate']

    df_people_choropleth.columns = columns_people
    df_rate_choropleth.columns = columns_rate
    df_people_line_bar.columns = columns_people_line_bar
    df_rate_line_bar.columns = columns_rate_line_bar

    # Convert 'Date' column to datetime format
    df_people_choropleth['Date'] = pd.to_datetime(df_people_choropleth['Date'], format='%Y-%m-%d %H:%M:%S')
    df_rate_choropleth['Date'] = pd.to_datetime(df_rate_choropleth['Date'], format='%Y-%m-%d %H:%M:%S')
    df_people_line_bar['Date'] = pd.to_datetime(df_people_line_bar['Date'], format='%Y-%m-%d %H:%M:%S')
    df_rate_line_bar['Date'] = pd.to_datetime(df_rate_line_bar['Date'], format='%Y-%m-%d %H:%M:%S')

    # Convert the rest of the columns to numeric, coercing errors
    for col in columns_people[1:]:
        df_people_choropleth[col] = pd.to_numeric(df_people_choropleth[col], errors='coerce')
    for col in columns_rate[1:]:
        df_rate_choropleth[col] = pd.to_numeric(df_rate_choropleth[col], errors='coerce')
    for col in columns_people_line_bar[1:]:
        df_people_line_bar[col] = pd.to_numeric(df_people_line_bar[col], errors='coerce')
    for col in columns_rate_line_bar[1:]:
        df_rate_line_bar[col] = pd.to_numeric(df_rate_line_bar[col], errors='coerce')

    return df_people_choropleth, df_rate_choropleth, df_people_line_bar, df_rate_line_bar
