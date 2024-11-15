#API Summary: To get the top 10 ranked countries with medal counts in Paris 2024 Olympics.

from googletrans import Translator

import requests
import json

translator = Translator()

rename_dict = "Great Britain" # When using the translator, this only outputs 'Briton' so as a workaround I use a variable replacement instead shown later in the code.


url = "https://apis.codante.io/olympic-games/countries" # Base URL for the API.
response = requests.get(url)

if response.status_code == 200: # Status code 200 is that it is able to connect successfully to the API and can collect the API data.
  data = response.json()

  countries = data['data'] #accessing API data dictionary.


  for i, country in enumerate(countries[:10]): # Loop through the top 10 ranked countries of 2014 Olympics and print the medal information
    original_name = country['name']
    translated_name = translator.translate(original_name, src='pt', dest='en').text # I am using a translator as the API end points are in Portuguese, this takes in the original name on the API, the source language is Portuguese and the destination output is returned in English.
#Getting the medal information for gold, silver, bronze and total medals alongside where they ranked in the 2024 olympic games.
    gold_medals = country['gold_medals']
    silver_medals = country['silver_medals']
    bronze_medals = country['bronze_medals']
    total_medals = country['total_medals']
    rank = country['rank']
    print(f"Rank: {rank}")
    if country['name'] == "Grã-Bretanha": #As commented earlier in the code; using a if statement to replace this to Great Britain, otherwise portuguese output is 'Briton' without this.
      print(f"Country: {rename_dict}")
    else:
      print(f"Country: {translated_name}") # goes back to using the translated data.
    print(f"Gold Medals: {gold_medals}")
    print(f"Silver Medals: {silver_medals}")
    print(f"Bronze Medals: {bronze_medals}")
    print(f"Total Medals: {total_medals}")
    print("-" * 10)  # used a separator for better readability
else:
  print(f"Failed to retrieve data. Status code: {response.status_code}")

