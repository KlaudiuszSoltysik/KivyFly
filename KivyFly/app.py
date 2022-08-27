from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window

import requests
import random
import webbrowser
from dotenv import load_dotenv
import os

load_dotenv()

#ENVIORMENTAL VARIABLES NEEDED TO CONNECT WITH SPREADSHEET API'S 
AIRPORTS_ENDPOINT = os.getenv("AIRPORTS_ENDPOINT")
WISHLIST_ENDPOINT = os.getenv("WISHLIST_ENDPOINT")


class KivyFlyApp(App):
    pass


#DEFINING HEADER OF THE WINDOW   
class Header(BoxLayout):
    pass


#NOTIFICATION POPUP
class PopupContent(BoxLayout):
    pass


#CONTENT OF AN APP
class Panel(BoxLayout):
    airports_data = {}
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        #GETTING AIRPORTS DATA
        data = requests.get(url = AIRPORTS_ENDPOINT).json()

        for item in data:
            name = item["city"].strip()
            self.airports_data[name] = item

    
    #SWITCHING FROM AND TO LOCATIONS WITH EACH OTHER
    def switch_locations(self, from_input, to_input):
        tmp = from_input.text
        from_input.text = to_input.text
        to_input.text = tmp
        
    
    #RANDOMIZING DESTINATION 
    def random_location(self, text_input):
        text_input.text = random.choice(list(self.airports_data))
    

    #PROCESSING USER'S CONSENT
    def unlock(self, button, text_input):        
        if button.state == "normal":
            text_input.disabled = True
            text_input.text = ""
        else:
            text_input.disabled = False
            
    
    #CHECKING IF EMAIL IS VALID
    def email_validation(self, email):
        if not "@" in email.text:
            email.foreground_color = (1, 0, 0)
        elif email.text == "" or "@" in email.text:
            email.foreground_color = (0, 0, 0)
            
    
    #CHCKING IF PHONE NUMBER IS VALID
    def phone_validation(self, phone):
        if  len(phone.text) != 9:
            phone.foreground_color = (1, 0, 0)
        else:
            phone.foreground_color = (0, 0, 0)
            
    
    #CHECKING IF USER'S FLIGHT IS CORRECT ADDING FLIGHT TO WISHLIST      
    def add_flight(self, button, from_city, to_city, days, price, email, phone):
        #RESETING BUTTONS AND TEXT BOXES
        button.text = "Add flight"
        button.color = (1, 1, 1)
        from_city.foreground_color = (0, 0, 0)
        to_city.foreground_color = (0, 0, 0)
        days.foreground_color = (0, 0, 0)
        price.foreground_color = (0, 0, 0)
        email.foreground_color = (0, 0, 0)
        phone.foreground_color = (0, 0, 0)
        
        self.email_validation(email)
        self.phone_validation(phone)
        
        #CHECKING IF USER'S FLIGHT IS CORRECT
        if (from_city.text.capitalize()).strip() == (to_city.text.capitalize()).strip():
            button.text = "Invalid value - refill and try again"
            button.color = (1, 0, 0)
            from_city.foreground_color = (1, 0, 0)
            to_city.foreground_color = (1, 0, 0)
            return False
        
        if email.text == "" and phone.text == "" or days.text == "":
            button.text = "Missing value - refill and try again"
            button.color = (1, 0, 0)
            return False
            
        if int(days.text) < 1:
            button.text = "Invalid value - refill and try again"
            button.color = (1, 0, 0)
            days.foreground_color = (1, 0, 0)
            return False
            
        if int(price.text) < 0:
            button.text = "Invalid value - refill and try again"
            button.color = (1, 0, 0)
            price.foreground_color = (1, 0, 0)
            return False
        
        if (from_city.text.capitalize()).strip() not in self.airports_data:
            button.text = "Invalid value - refill and try again"
            button.color = (1, 0, 0)
            from_city.foreground_color = (1, 0, 0)
            return False

        if (to_city.text.capitalize()).strip() not in self.airports_data:
            button.text = "Invalid value - refill and try again"
            button.color = (1, 0, 0)
            to_city.foreground_color = (1, 0, 0)
            return False
        
        #ADDING FLIGHT TO THE WISHLIST
        record = {"from": (from_city.text.capitalize()).strip(),
                  "to": (to_city.text.capitalize()).strip(),
                  "days": str(days.text), 
                  "price": str(price.text),
                  "email": email.text,
                  "phone": phone.text}
        
        requests.post(url = WISHLIST_ENDPOINT, json = record)
        
        #RESETING TEXTBOXES
        from_city.text = ""
        to_city.text = ""
        days.text = ""
        price.text = ""
        button.text = "Add flight"
        button.color = (1, 1, 1)
        from_city.foreground_color = (0, 0, 0)
        to_city.foreground_color = (0, 0, 0)
        days.foreground_color = (0, 0, 0)
        price.foreground_color = (0, 0, 0)
        email.foreground_color = (0, 0, 0)
        phone.foreground_color = (0, 0, 0)
        
        #SUCCESS POPUP
        content = Button(text = "OK")
        popup = Popup(title = "Flight added",
                      content = content, 
                      auto_dismiss = False)
        content.bind(on_press = popup.dismiss)
        popup.open()
    
    
    #OPENING SPREADSHEET WITH USER WISHLIST
    def show_wishlist(self):
        webbrowser.open("https://docs.google.com/spreadsheets/d/1K9qop8wJkf-SEo4aPtqC2krZm9AyBaSa9MJPODCbAgc/edit#gid=107795421")
    
    
    #CLEARING WISHLIST
    def clear_wishlist(self):
        response = requests.delete(url = WISHLIST_ENDPOINT + "/all")
        
        content = Button(text = "OK")
        popup = Popup(title = "WISHLIST CLEARED",
                      content = content, 
                      auto_dismiss = False)
        content.bind(on_press = popup.dismiss)
        popup.open()
    

#DEFINING WINDOW
class App(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.orientation = "vertical"
        
        Window.size = (500, 700)
        
        self.header = Header(size_hint = (1, None),
                             height = self.width * 2)
        self.panel = Panel()
        
        self.add_widget(self.header)
        self.add_widget(self.panel)


#CREATING WINDOW AND RUNNING THE PROGRAM  
KivyFlyApp().run()