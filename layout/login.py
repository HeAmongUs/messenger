from kivy.properties import ObjectProperty
from kivymd.uix.gridlayout import MDGridLayout

from session import session, url


class LoginLayout(MDGridLayout):
    notification = ObjectProperty()
    login_input = ObjectProperty()
    password_input = ObjectProperty()

    def user_login(self):
        login = self.login_input.text
        password = self.password_input.text

        if not login:
            self.notification.text = "Enter Login"
            return
        elif not password:
            self.notification.text = "Enter password"
            return
        else:
            try:
                post_request = session.session.post(url + "/login", {
                    "username": login,
                    "password": password
                })
                if post_request.text == "Logged in":
                    session.is_authorized = True
                self.notification.text = post_request.text
            except:
                self.notification.text = "Ошибка запроса"
