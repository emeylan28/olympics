# Summary: Connecting to our SQL database and viewing the Team GB 2024 Sports from our own server API.

import mysql.connector
from mysql.connector import Error
from flask import Flask, jsonify
from config import USER, PASSWORD, HOST

app = Flask(__name__)

try:
    # Establishing connection to the database
    conn = mysql.connector.connect(
        host=HOST,
        user=USER,
        password = PASSWORD,
        database='olympics'
    )

    # Create a cursor object using the connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM medal_events")

    # Fetch all results from the executed query

    data = cur.fetchall()

    # Get the column names from the cursor description
    columns = [col[0] for col in cur.description]

    # Initialising an empty list to hold the data dictionaries.

    data_dict = []

    # Looping through each row in the data
    for row in data:
        row_dict = {} # creates a dictionary for each row
        # Loop through each column and corresponding value in the row
        for i in range(len(columns)):
            row_dict[columns[i]] = row[i] # Mapping the column name to the relevant row 
        # Add the dictionary to the list
        data_dict.append(row_dict)

except mysql.connector.Error as err:
    print(f"Error: {err}") # Provides us any errors that we run into.

# Once we are done, we close the cursor and connection for security purposes
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()

#Creates our landing page
@app.route('/')
def get_landing_page():
    res = {"2024 Olympic Games": "CFG Group Project"}
    return jsonify(res)

# New URL endpoint for Team GB won events.
@app.route('/teamgb/')
def get_data():
    return jsonify(data_dict) # Returns the data in JSON dictionary format.

if __name__ == '__main__':
    app.run(debug=True)


