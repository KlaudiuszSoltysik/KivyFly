import requests

TICKETS_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
TICKETS_API_KEY = "Fpvtru_uLRs-3oqwAgaGTf9XdilUCyPD"

AIRPORTS_ENDPOINT = "https://sheetsu.com/apis/v1.0su/f93d3b2189ac"

api_header = {
    "apikey": TICKETS_API_KEY 
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

response = requests.get(url = TICKETS_ENDPOINT, headers = api_header, params = flight_params)
data = response.json()
#print(data)

response2 = requests.get(url = AIRPORTS_ENDPOINT)
data2 = response2.json()
print(data2)