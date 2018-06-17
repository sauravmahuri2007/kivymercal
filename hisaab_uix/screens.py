import re

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput


class FloatInput(TextInput):

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)


def switch_screen_to(screen):
    App.get_running_app().root.current = screen


def get_color_code(color):
    COLOR_MAP = {
        'red': [x / 255.0 for x in (255, 0, 0, 255)],
        'green': [x / 255.0 for x in (0, 255, 0, 255)],
        'blue': [x / 255.0 for x in (0, 0, 255, 255)],
        'black': [x / 255.0 for x in (255, 255, 255, 255)],
    }
    default_code = [x / 255.0 for x in (0, 0, 255, 255)]  # default white
    if not color:
        color_code = default_code
    elif isinstance(color, str):
        # Get color code from our mapping for most famous colors.
        color_code = COLOR_MAP.get(color.lower()) or default_code
    elif isinstance(color, list) or isinstance(color, tuple) and len(color) in (3, 4):
        color_code = [x / 255.0 for x in color]
    else:
        color_code = default_code
    return color_code


class AppFlow(ScreenManager):

    def __init__(self, **kwargs):
        super(AppFlow, self).__init__(**kwargs)
        # self.login_screen = Screen(name='login')
        # self.login_screen.add_widget(Login())
        self.home_screen = Screen(name='home')
        self.home_screen.add_widget(Home())
        self.home_screen.add_widget(Contact())
        # self.add_widget(self.login_screen)
        self.add_widget(self.home_screen)
        # self.current = self.login_screen.name  # Very 1st screen when app will load.


class Login(GridLayout):
    """
    A simple login screen using GridLayout
    """

    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
        self.add_widget(Button(text='Login', on_press=self.authenticate))
        self.notification = Label(text='')
        self.add_widget(self.notification)

    def authenticate(self, *args):
        username = self.username.text
        password = self.password.text
        if username == 'sk' and password == 'sk':
            switch_screen_to('home')
            return True
        else:
            self.notification.text = 'Invalid Username or Password'
            return False


class Heading(GridLayout):

    def __init__(self, **kwargs):
        super(Heading, self).__init__(**kwargs)
        self.cols_list = kwargs.get('columns') or []
        self.cols = len(self.cols_list)
        for name in self.cols_list:
            self.add_widget(Label(text=name))


class DataRow(GridLayout):

    def __init__(self, **kwargs):
        super(DataRow, self).__init__(**kwargs)
        self.cols = 3
        self.entity = Label(text=kwargs.get('entity', 'Label'))
        self.readonly = kwargs.get('readonly') or []  # a list of fields which can be made as read only
        self.rate = FloatInput(input_type='number', multiline=False, readonly='rate' in self.readonly)
        self.quantity = FloatInput(input_type='number', multiline=False, readonly='quantity' in self.readonly)
        # Adding to DataRow Grid
        self.add_widget(self.entity)
        self.add_widget(self.rate)
        self.add_widget(self.quantity)


class OtherRow(GridLayout):

    def __init__(self, **kwargs):
        super(OtherRow, self).__init__(**kwargs)
        self.cols = 2
        self.entity = Label(text=kwargs.get('entity', 'Label'))
        self.readonly = kwargs.get('readonly') or []
        self.value = FloatInput(input_type='number', multiline=False, readonly='value' in self.readonly)
        self.add_widget(self.entity)
        self.add_widget(self.value)


class Contact(BoxLayout):

    def __init__(self, **kwargs):
        super(Contact, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, 0.25)
        self.add_widget(
            Label(text='''
                    Designed and Developed by:
                    Saurav Kumar
                    Sr. Software Engineer
                    saur.k10@gmail.com
                    9360014137
                    ''',
                  valign='middle',
                  halign='justify',
                  color=get_color_code('green')))


class Home(BoxLayout):

    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, 0.75)
        self.pos_hint = {'top': 1}
        self.padding = 10
        self.spacing = 10
        self.items = 5
        self.item_names = ['Item ' + str(x+1) for x in range(self.items)]
        self.total_weight = OtherRow(entity='Total Weight (KG)')
        self.wastage = OtherRow(entity='Wastage (KG)')
        self.transportation = OtherRow(entity='Transportation (Rs)')
        self.labour = OtherRow(entity='Labour/ Brokerage (Rs)')
        self.paddies = [DataRow(entity=name) for name in self.item_names]  # all 5 items name
        self.result = OtherRow(entity='Merchant Amount', readonly=['value'])
        self.add_widget(self.total_weight)
        self.add_widget(self.wastage)
        self.add_widget(self.transportation)
        self.add_widget(self.labour)
        self.add_widget(Heading(columns=['# Items', 'Rate/Quintal', '# Packets' ]))
        for paddy in self.paddies:
            self.add_widget(paddy)
        self.add_widget(self.result)
        self.add_widget(Button(text='Calculate', on_press=self.calculate))

    def calculate(self, *args):
        try:
            total_amount = total_quantity = 0.0
            labour_fee = self.labour.value.text and float(self.labour.value.text) or 0.0
            trans_fee = self.transportation.value.text and float(self.transportation.value.text) or 0.0
            total_weight = self.total_weight.value.text and float(self.total_weight.value.text) or 0.0
            wastage = self.wastage.value.text and float(self.wastage.value.text) or 0.0
            actual_weight = total_weight - wastage
            for paddy in self.paddies:
                total_quantity += paddy.quantity.text and float(paddy.quantity.text) or 0.0
            for paddy in self.paddies:
                rate = paddy.rate.text and (float(paddy.rate.text) / 100) or 0.0  # rate per kg
                quantity = paddy.quantity.text and float(paddy.quantity.text) or 0.0  # quantity of current paddy
                total_amount += rate * (actual_weight / total_quantity * quantity)
            paid_amount = total_amount - (trans_fee + labour_fee)
            self.result.value.text = '%.2f' % float(paid_amount)
            self.colorize(self.result, 'green')
        except ZeroDivisionError:
            self.colorize(self.result, 'red')
            self.result.value.text = 'Wrong Data!'
        except Exception as err:
            self.colorize(self.result, color='red')
            self.result.value.text = err.args[0]

    def colorize(self, obj=None, color=None):
        if not obj:
            obj = self
        if isinstance(obj, list) or isinstance(obj, tuple):
            for elm in obj:
                self.colorize(elm, color)
        else:
            color_code = get_color_code(color)
            for child in obj.children:
                child.color = color_code
