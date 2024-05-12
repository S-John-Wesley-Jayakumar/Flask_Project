import streamlit as st
import requests
import pandas as pd


def process_and_insert_to_mongodb(data):
    import pandas as pd
    from pymongo import MongoClient

        # Connect to MongoDB
    client = MongoClient('mongodb+srv://wesleyjohnjayakumar:<password>$@employees.4ujzpwr.mongodb.net/?retryWrites=true&w=majority&appName=Employees')
    db = client['weather_data']
    collection = db['weatherDT']
  

    # Step 1: Data Transformation and Loading into MongoDB
    data['datetime_utc'] = pd.to_datetime(data['datetime_utc'], format='%Y%m%d-%H:%M')
    
    # Step 2: Data Cleansing & De-duplication
    # Replace NaN and null values with 0
    data.replace(-9999, 19879, inplace=True)
    data.fillna(0, inplace=True)
    data.drop_duplicates(inplace=True)
    
    # Convert DataFrame to dictionary
    data_dict = data.to_dict(orient='records')
    
    # Insert data into MongoDB collection
    collection.delete_many({})
    collection.insert_many(data_dict)
    print("Data inserted into MongoDB successfully.")
    st.write("Data inserted into MongoDB successfully.")





# Define the base URL for your Flask API
BASE_URL = "http://127.0.0.1:5000"

# Define a function to fetch weather data from the Flask API based on date
def get_weather_by_date(date):
    response = requests.get(f"{BASE_URL}/date/{date}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Define a function to fetch weather data from the Flask API based on year
def get_weather_by_year(year):
    response = requests.get(f"{BASE_URL}/year/{year}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Main Streamlit app
def main():
    st.title("Weather Data Retrieval")

    # Sidebar for user input
    st.sidebar.header("Data Loaded and transformed , -Removed Null , NAN Values , - Dropped duplicates")

    if st.sidebar.button("Upload Transformed data"):
        # Read CSV data into DataFrame
        df = pd.read_csv(r'C:\Users\programms\Desktop\WEATHER TASK\Weather Data.csv')
        # Call the function to process DataFrame and insert into MongoDB
        process_and_insert_to_mongodb(df)
    
    st.sidebar.header("Input Parameters for Flask API ")

    year = st.sidebar.number_input("Enter Year", min_value=1800, max_value=2100, step=1)
    date = st.sidebar.date_input("Enter Date")

    
    # Button to trigger API call for year
    if st.sidebar.button("Submit for Year"):
        if year:
            data = get_weather_by_year(year)
            if data:
                st.write("Weather Data for Year", year)
                st.write(data)
            else:
                st.write("No data available for the specified year.")

    # Button to trigger API call for date
    if st.sidebar.button(" Submit for Date"):
        if date:
            data = get_weather_by_date(date.strftime("%Y-%m-%d"))
            
            if data:
                st.write("Weather Data for Date in JSON", date)
                st.write(data)
         
            else:
                st.write("No data available for the specified date.")

if __name__ == "__main__":
    main()
