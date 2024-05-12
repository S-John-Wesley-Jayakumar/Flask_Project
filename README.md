#Flask Weather App Backend
This is a Flask backend application API that provides weather data retrieved from a MongoDB database. It allows users to query weather information based on date or year.

#Streamlit Front end UI for Data Retrieval
This Streamlit application provides a user interface to interact with a Flask API for retrieving weather data. It allows users to upload transformed weather data, query weather data based on specific years or dates, and displays the results.

Prerequisites Python 3.x Flask Pandas PyMongo Requests

#Access the following endpoints:

/: Returns a welcome message. /date/: Retrieves weather data for a specific date. /year/: Retrieves weather data for a specific year, aggregated by month.

Error Handling If an error occurs during the retrieval of weather data, the API returns an error message along with a 500 status code.

Update the MongoDB URI in the process_and_insert_to_mongodb function in the app.py file to connect to your MongoDB database.

#Run the Streamlit application:

streamlit run app.py

Upload transformed weather data: Click on the "Upload Transformed data" button. Select the CSV file containing transformed weather data.

Query weather data based on year or date: Enter the year or date in the sidebar. Click on the respective "Submit for Year" or "Submit for Date" button. View the weather data displayed in the main panel.

#Features
Upload transformed weather data. Query weather data based on year or date. Display weather data in JSON format.
