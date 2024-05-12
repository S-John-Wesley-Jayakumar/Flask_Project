from flask import Flask, jsonify
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from bson import json_util


app = Flask(__name__)

client = MongoClient('mongodb+srv://wesleyjohnjayakumar:<password>$@employees.4ujzpwr.mongodb.net/?retryWrites=true&w=majority&appName=Employees')
db = client['weather_data']
collection = db['weatherDT']

@app.route('/')
def hello():
    return 'Hello, welcome to Flask Backend!'


@app.route('/date/<date>', methods=['GET'])
def get_weather_by_date(date):
    try:
        start_date = pd.to_datetime(date)
        end_date = start_date + pd.Timedelta(days=1)  # Next day
        data = list(collection.find({'datetime_utc': {'$gte': start_date, '$lt': end_date}}))
        data_json = json_util.dumps(data)
        return jsonify(data_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/year/<int:year>', methods=['GET'])
def get_weather_by_year(year):
    try:
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1)
        
        # Retrieve data for the specified year
        data = list(collection.find({'datetime_utc': {'$gte': start_date, '$lt': end_date}}))     
        # Create DataFrame
        a = pd.DataFrame(data)
        col = a.columns.to_list()
        if (len(col) > 0):
            # Convert datetime_utc to datetime type
            a['month'] = pd.to_datetime(a[col[1]])
            t = col[13] # getting temperature column
            
            # Group by month and calculate min, max, and average temperature
            monthly_stats = a.groupby(a['month'].dt.month).agg(
                min_temp=(t, 'min'),
                max_temp=(t, 'max'),
                avg_temp=(t, 'mean')
            ).reset_index()
            
            # Add year to the result
            monthly_stats['year'] = year
            # Convert DataFrame to dictionary
            result = monthly_stats.to_dict(orient='records')
            return jsonify(result)
        else:
            return jsonify({})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
