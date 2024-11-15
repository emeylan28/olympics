# API Summary: This API was getting all the sporting events in Paris 2024 Olympics API that Team GB won a medal.
# Connects with an external API, gets the API data and updates our SQL database with the date of event, the sport and medal.
# This can then be viewed on our own API server using the app.py file.

import requests
import mysql.connector
from datetime import datetime
from config import USER, PASSWORD, HOST # config file holds SQL credentials

#Database connection parameters

HOST = HOST
USER = USER
PASSWORD = PASSWORD
DATABASE = 'olympics' # connect to the olympics database

# API URL end point to get the event details: date of event, sport, medal

url = 'https://apis.codante.io/olympic-games/events' 

# Function to process and insert event data into the database
def find_insert(event, cursor):
    sport_name = event.get('discipline_name', 'Unknown') # using parameter 'unknown' and 'n/a' to avoid getting errors for missing data within the API.
    # So instead of giving an error, it will provide this parameter output as a replacement instead to continue running though the API entries.
    event_date = event.get('day', 'Unknown')

    # Have the date format as YYYY-MM-DD for SQL
    if event_date != 'Unknown':
        event_date = datetime.strptime(event_date, '%Y-%m-%d').strftime('%Y-%m-%d')

    # Checks medal event = 1 as that means it was a final where a medal was provided, whereas medal_event equalling 0 is not.
    if event.get('is_medal_event') == 1:
        for competitor in event.get('competitors',[]):
            country_id = competitor.get('country_id', 'Unknown')
            if country_id == "Grã-Bretanha": # as the API is in Portuguese, using this term which translates to Great Britain.
                result_position = competitor.get('result_position', 'N/A') # result being first, second or third placed in the event.

    #converting the winning results of 1,2,3 into relevant medals using else if statements if no medals found, continue with code.
                if result_position == '1':
                    medal = 'Gold'
                elif result_position == '2':
                    medal = 'Silver'
                elif result_position == '3':
                    medal = 'Bronze'
                else:
                    continue # skip the rest of the loop

    # Insert data into the olympics database in the medal_events table

                cursor.execute("""
                    INSERT INTO medal_events (event_date, discipline_name, medal)
                    VALUES (%s, %s, %s)
                """, (event_date, sport_name, medal))

# Function to fetch and update the data

def fetupdate(cursor):
    params = {
        'is_medal_event': 1, # confirms that only medalled events get updated.
        'limit': 100 # The API has a limit of 100 request calls.
    }

# as this API has lots of entries over multiple pages 
# start from page 1 and will go through each of them.
    page = 1 
    while True:
        params['page'] = page
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e: # raising an exception error for any pages that fail to be retrieved.
            print(f"Failed to retrieve page {page}: {e}")
            break

        data = response.json()
        if not data.get('data'):
            break

        for event in data.get('data', []): # for loop to insert the event data into sql using the find_insert function.
            find_insert(event, cursor)

        page += 1 # continue looping through each page of the API until it ends.

# function to connect to the olympics database
def main():
    try:
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        cursor = conn.cursor()

        # Fetch and update the database
        fetupdate(cursor)

        # Commit the fetched updates to the database
        conn.commit()

        #raise exception error if needed.

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    # Close the connection and cursor
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    main()


        
