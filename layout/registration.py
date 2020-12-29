from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout

from session import session, url

class RegistrationLayout(MDBoxLayout):
    notification = ObjectProperty()
    login_input = ObjectProperty()
    password1_input = ObjectProperty()
    password2_input = ObjectProperty()

    def user_registration(self):
        self.notification.text = ""
        login = self.login_input.text
        password2 = self.password2_input.text
        password1 = self.password1_input.text

        if not login:
            self.notification.text = "Enter Login"
            return
        elif not password1 or not password2:
            self.notification.text = "Enter password"
            return
        elif password1 != password2:
            self.notification.text = "Passwords do not match"
        else:
            post_request = session.session.post(url+"/registration", {
                "username": login,
                "password": password1
            })
            self.notification.text = post_request.text

