import smtplib
import requests
import datetime

#ENVIORMENTAL VARIABLES NEEDED TO CONNECT WITH API WITH FLIGHTS DATA
TICKETS_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
TICKETS_API_KEY = "Fpvtru_uLRs-3oqwAgaGTf9XdilUCyPD"

#ENVIORMENTAL VARIABLES NEEDED TO CONNECT WITH SPREADSHEET API'S 
AIRPORTS_ENDPOINT = "https://sheetdb.io/api/v1/86e83n2e9x2ti"
WISHLIST_ENDPOINT = "https://sheetdb.io/api/v1/a2o9bu5hqn0hf"

#ENVIORMENTAL VARIABLES - EMAIL AND PASSWORD WCHIH SENDS YOU AN EMAIL
EMAIL = "czekolada668@gmail.com"
PASSWORD = "Krajobraz1"

#API KEY REQUARIED TO DOWNLOAD FLIGHTS DATA
api_header = {
    "apikey": TICKETS_API_KEY 
}

#DOWNLOADING AIRPORTS DATA 
airports_data = {}

data = requests.get(url = AIRPORTS_ENDPOINT).json()

for item in data:
    name = item["city"].strip()
    airports_data[name] = item

#DOWNLOADING WISHLIST
data = requests.get(url = WISHLIST_ENDPOINT).json()

#GETTING CURRENT TIME
today = (datetime.date.today()).strftime("%d/%m/%Y")
after_180days = datetime.date.today() + datetime.timedelta(days = 180)
    
#SEARCHING FOR FLIGHTS MATCHING USER PREFERENCES
for row in data:
    #SAVING USER PREFERENCES TO SEND TO AN API
    flight_params = {"fly_from": airports_data[row["from"]]["IATA"],
                     "fly_to": airports_data[row["to"]]["IATA"],
                     "date_from": today,
                     "date_to": after_180days,
                     "nights_in_dst_from": str(int(row["days"]) - 1),
                     "nights_in_dst_to": str(int(row["days"]) + 1),
                     "curr": "EUR",
                     "price_to": int(row["price"]),
                     "sort": "price",
                     "limit": 3}

    #REQUEST TO A FLIGHTS API
    flights_data = requests.get(url = TICKETS_ENDPOINT, headers = api_header, params = flight_params).json()
    
    #SENDING AN EMAIL NOTIFICATION
    with smtplib.SMTP("smtp.gmail.com") as connection :
        connection.starttls()
        connection.login (EMAIL, PASSWORD)
        connection.sendmail(from_addr = EMAIL,
                            to_addrs = row["email"],
                            msg = f"Subject: We found an interesting flight you may be interested in 🥳\n\nFly from {flights_data['data'][0]['cityFrom']}-{flights_data['data'][0]['cityCodeFrom']} to {flights_data['data'][0]['cityTo']}-{flights_data['data'][0]['cityCodeTo']}.\n\nDetails:\nUTC departue: {flights_data['data'][0]['utc_departure']}\nNights in destination: {flights_data['data'][0]['nightsInDest']}\nYou can book flight at: {flights_data['data'][0]['deep_link']}")

        print(f"Subject: We found an interesting flight you may be interested in 🥳\n\nFly from {flights_data['data'][0]['cityFrom']}-{flights_data['data'][0]['cityCodeFrom']} to {flights_data['data'][0]['cityTo']}-{flights_data['data'][0]['cityCodeTo']}.\n\nDetails:\nUTC departue: {flights_data['data'][0]['utc_departure']}\nNights in destination: {flights_data['data'][0]['nightsInDest']}\nYou can book flight at: {flights_data['data'][0]['deep_link']}"))
    #SENDING A SMS NOTIFICATION
    
print("sent")