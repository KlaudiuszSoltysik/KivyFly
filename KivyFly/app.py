from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window

class KivyFlyApp(App):
    pass

        
class Header(BoxLayout):
    pass


class PopupContent(BoxLayout):
    pass


class Panel(BoxLayout):
    def unlock(self, button, widget):        
        if button.state == "normal":
            widget.disabled = True
            widget.text = ""
        else:
            widget.disabled = False
            
    
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