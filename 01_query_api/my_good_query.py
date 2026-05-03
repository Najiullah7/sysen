from dotenv import load_dotenv
import requests
import os

load_dotenv()  # loads .env into environment

api_key = os.getenv("CENSUS_API_KEY") # gets the census api key from .env

url = "https://api.census.gov/data/2022/ecnbasic" # base url

params = {
    "get": "NAICS2022,NAICS2022_LABEL,NAME,GEO_ID,ESTAB,RCPTOT,EMP",
    "for": "us:*",
    "key": api_key
} # Parameters

response = requests.get(url, params=params) # request for the data
print("Status code:", response.status_code) 
response.raise_for_status() # print any error message

data = response.json()

headers = data[0]
rows = data[1:11]   # first 10 rows only

filtered = [dict(zip(headers, row)) for row in rows]

for row in filtered:
    print(row)