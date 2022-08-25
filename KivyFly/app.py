from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window

import requests
import random
from sheetsu import SheetsuClient

AIRPORTS_ENDPOINT = "https://sheetsu.com/apis/v1.0su/f93d3b2189ac"
WISHLIST_ENDPOINT = "https://sheetsu.com/apis/v1.0su/80af76dd4bea"

class KivyFlyApp(App):
    pass

        
class Header(BoxLayout):
    pass


class PopupContent(BoxLayout):
    pass


class Panel(BoxLayout):
    airports_data = {}
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        data = requests.get(url = AIRPORTS_ENDPOINT).json()

        for item in data:
            name = item['city'].strip()
            self.airports_data[name] = item
            
        print(self.airports_data)

    
    def switch_locations(self, from_input, to_input):
        tmp = from_input.text
        from_input.text = to_input.text
        to_input.text = tmp
        
        
    def random_location(self, text_input):
        text_input.text = random.choice(list(self.airports_data))
    

    def unlock(self, button, text_input):        
        if button.state == "normal":
            text_input.disabled = True
            text_input.text = ""
        else:
            text_input.disabled = False
            
    
    def email_validation(self, email):
        if not "@" in email.text:
            email.foreground_color = (1, 0, 0)
        elif email.text == "" or "@" in email.text:
            email.foreground_color = (0, 0, 0)
            
    
    def phone_validation(self, phone):
        if  len(phone.text) != 9:
            phone.foreground_color = (1, 0, 0)
        else:
            phone.foreground_color = (0, 0, 0)
            
            
    def add_flight(self, button, from_city, to_city, days, price, email, phone):
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
        
        record = {"from": (from_city.text.capitalize()).strip(),
                  "to": (to_city.text.capitalize()).strip(),
                  "days": str(days.text), 
                  "price": str(price.text),
                  "email": email.text,
                  "phone": phone.text}
        
        client = SheetsuClient(WISHLIST_ENDPOINT)
        client.create_one(record)
        
        from_city.text = ""
        to_city.text = ""
        days.text = ""
        price.text = ""
        email.text = ""
        phone.text = ""
        
        content = Button(text = "OK")
        popup = Popup(title = "Flight added",
                      content = content, 
                      auto_dismiss = False)
        content.bind(on_press = popup.dismiss)
        popup.open()
    
    
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

    
KivyFlyApp().run()