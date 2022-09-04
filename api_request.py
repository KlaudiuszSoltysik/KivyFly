import smtplib
import requests
import datetime
from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()

#ENVIORMENTAL VARIABLES NEEDED TO CONNECT WITH API WITH FLIGHTS DATA
TICKETS_ENDPOINT = os.getenv("TICKETS_ENDPOINT")
TICKETS_API_KEY = os.getenv("TICKETS_API_KEY")

#ENVIORMENTAL VARIABLES NEEDED TO CONNECT WITH SPREADSHEET API'S 
AIRPORTS_ENDPOINT = os.getenv("AIRPORTS_ENDPOINT")
WISHLIST_ENDPOINT = os.getenv("WISHLIST_ENDPOINT")

#ENVIORMENTAL VARIABLES - EMAIL AND PASSWORD TO AN EMAIL ACCOUNT
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

#ENVIORMENTAL VARIABLES - FOR SMS SENDING
SID = os.getenv("SID")
TOKEN = os.getenv("TOKEN")
NUMBER = os.getenv("NUMBER")

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
    
    for flight in flights_data['data']:
        #MESSAGE BODY
        to_send = f"We found a flight you may be interested in 🥳\n\nFly from {flight['cityFrom']}-{flight['cityCodeFrom']} to {flight['cityTo']}-{flight['cityCodeTo']}.\n\nDetails:\nUTC departue: {flight['utc_departure']}\nNights in destination: {flight['nightsInDest']}\nYou can book flight at: {flight['deep_link']}"

        print(to_send)
        
        #SENDING AN EMAIL NOTIFICATION
        if row["email"] != "":
            try:
                with smtplib.SMTP("smtp.gmail.com") as connection :
                    connection.starttls()
                    connection.login (EMAIL, PASSWORD)
                    connection.sendmail(from_addr = EMAIL,
                                        to_addrs = EMAIL,
                                        msg = to_send)
                print("Email sent")
            except:
                print("Email error")
            finally:
                pass

        #SENDING A SMS NOTIFICATION
        if row["phone"] != "":
            try:
                client = Client(SID, TOKEN)
                message = client.messages.create(body = to_send, 
                                                from_ = NUMBER, 
                                                to = "+48" + row["phone"])
                print("SMS sent")
            except:
                print("SMS error")
            finally:
                pass