from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.relativelayout import RelativeLayout

from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import SwapTransition, Screen

from layout.registration import RegistrationLayout
from layout.chat import ChatLayout
from layout.login import LoginLayout


Builder.load_file("advanced.kv")
Builder.load_file("main_layout.kv")
Builder.load_file("layout/registration_layout.kv")
Builder.load_file("layout/login_layout.kv")
Builder.load_file("layout/chat_layout.kv")


Config.set('kivy', 'keyboard_mode', 'systemanddock')


class ClickableTextFieldRound(RelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    # Here specify the required parameters for MDTextFieldRound:
    # [...]
    text_field = ObjectProperty()

    def on_text_change(self):
        self.text = self.text_field.text

    
class RegistrationScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class ChatScreen(Screen):
    pass


class MainWindow(MDGridLayout):
    navbar = ObjectProperty()

    nav_registration = ObjectProperty()
    nav_login = ObjectProperty()
    nav_chat = ObjectProperty()

    screen_manager = ObjectProperty()

    registration_screen = RegistrationScreen(name='registration')
    login_screen = LoginScreen(name="login")
    chat_screen = ChatScreen(name="chat")

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        self.registration_screen.add_widget(RegistrationLayout())
        self.screen_manager.add_widget(self.registration_screen)

        self.login_screen.add_widget(LoginLayout())
        self.screen_manager.add_widget(self.login_screen)

        self.chat_screen.add_widget(ChatLayout())
        self.screen_manager.add_widget(self.chat_screen)

        self.screen_manager.transition = SwapTransition()

    def nav_registration_click(self):
        self.screen_manager.current = "registration"

    def nav_login_click(self):
        self.screen_manager.current = "login"

    def nav_chat_click(self):
        self.screen_manager.current = "chat"


class MessengerApp(MDApp):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    MessengerApp().run()

