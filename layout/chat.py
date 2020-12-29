import threading
import time

from kivy.properties import StringProperty, ListProperty, OptionProperty, NumericProperty, BooleanProperty, \
    ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivymd.font_definitions import theme_font_styles
from kivymd.material_resources import dp
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.gridlayout import MDGridLayout

from session import session, url

class MessageListItem(
    ThemableBehavior, RectangularRippleBehavior, ButtonBehavior, FloatLayout
):
    """
    Base class to all ListItems. Not supposed to be instantiated on its own.
    """

    text = StringProperty()
    """
    Text shown in the first line.

    :attr:`text` is a :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    text_color = ListProperty(None)
    """
    Text color in ``rgba`` format used if :attr:`~theme_text_color` is set
    to `'Custom'`.

    :attr:`text_color` is a :class:`~kivy.properties.ListProperty`
    and defaults to `None`.
    """

    font_style = OptionProperty("Subtitle1", options=theme_font_styles)
    """
    Text font style. See ``kivymd.font_definitions.py``.

    :attr:`font_style` is a :class:`~kivy.properties.OptionProperty`
    and defaults to `'Subtitle1'`.
    """

    theme_text_color = StringProperty("Primary", allownone=True)
    """
    Theme text color in ``rgba`` format for primary text.

    :attr:`theme_text_color` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'Primary'`.
    """

    secondary_text = StringProperty()
    """
    Text shown in the second line.

    :attr:`secondary_text` is a :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    secondary_text_color = ListProperty(None)
    """
    Text color in ``rgba`` format used for secondary text
    if :attr:`~secondary_theme_text_color` is set to `'Custom'`.

    :attr:`secondary_text_color` is a :class:`~kivy.properties.ListProperty`
    and defaults to `None`.
    """

    secondary_theme_text_color = StringProperty("Secondary", allownone=True)
    """
    Theme text color for secondary text.

    :attr:`secondary_theme_text_color` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'Secondary'`.
    """

    secondary_font_style = OptionProperty("Body1", options=theme_font_styles)
    """
    Font style for secondary line. See ``kivymd.font_definitions.py``.

    :attr:`secondary_font_style` is a :class:`~kivy.properties.OptionProperty`
    and defaults to `'Body1'`.
    """

    divider = OptionProperty(
        "Full", options=["Full", "Inset", None], allownone=True
    )
    """
    Divider mode. Available options are: `'Full'`, `'Inset'`
    and default to `'Full'`.

    :attr:`tertiary_font_style` is a :class:`~kivy.properties.OptionProperty`
    and defaults to `'Body1'`.
    """

    bg_color = ListProperty()
    """
    Background color for menu item.

    :attr:`bg_color` is a :class:`~kivy.properties.ListProperty`
    and defaults to `[]`.
    """

    _txt_left_pad = NumericProperty("16dp")
    _txt_top_pad = NumericProperty()
    _txt_bot_pad = NumericProperty()
    _txt_right_pad = NumericProperty(dp(24))
    _num_lines = 2
    _no_ripple_effect = BooleanProperty(False)


class ChatLayout(MDGridLayout):
    message_text_input = ObjectProperty()
    message_send_btn = ObjectProperty()
    message_list = ObjectProperty()
    chain = []
    current_len = len(chain)

    def send_message(self):
        text = self.message_text_input.text
        try:
            session.session.post(url+"/transactions/new", {
                "message": text
            })
            self.message_text_input.text = ""
        except:
            self.message_text_input.text = "Лшибка запроса"

    def refresh(self):
        if session.is_authorized:
            t1 = threading.Thread(target=ChatLayout.send_request_chain, args=(self, url+"/chain",))
            t1.start()

    def send_request_chain(self, url_chain):
        while session.is_authorized:
            try:
                actual_chain = session.session.get(url_chain).json()["chain"]
            except:
                self.message_text_input.text = "Лшибка запроса"
            if len(actual_chain) > len(self.chain):
                self.chain = actual_chain
                self.view_message()
            time.sleep(5)

    def view_message(self):
        for item in self.chain[self.current_len:]:
            for item2 in item["transactions"]:
                if item2["sender"] != "miner":
                    data = item2["message"]
                    message_item = MessageListItem(text=item2["sender"], secondary_text=data)
                    self.message_list.add_widget(message_item)
        self.current_len = len(self.chain)

    def mine(self):
        try:
            session.session.get(url+"/mine")
        except:
            self.message_text_input.text = "Лшибка запроса"


