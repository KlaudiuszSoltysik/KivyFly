import requests

ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
API_KEY = "Fpvtru_uLRs-3oqwAgaGTf9XdilUCyPD"

api_header = {
    "apikey": API_KEY 
}

flight_params = {
    "fly_from": "BSL",
    "fly_to": "AYT",
    "date_from": "25/08/2022",
    "date_to": "25/09/2023",
    "nights_in_dst_from": "4",
    "nights_in_dst_to": "6",
    "curr": "EUR",
    "sort": "date",
    "limit": 1}

response = requests.get(url = ENDPOINT, headers = api_header, params = flight_params)
data = response.json()
print(data)