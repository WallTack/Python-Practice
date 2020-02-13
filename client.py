# main.py

# Imports
import datetime
import time
import socket
import pickle
import threading

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

# todo - make an input field for entering the server IP
# Every item in an order is defined as an instance of this
class OrderItem:

    def __init__(self, order_id, name='', food='', time=None, details='', detailed=False, to_go='', divider=False):
        self.order_id = order_id
        self.name = name
        self.food = food
        self.time = time
        self.details = details
        self.detailed = detailed
        self.to_go = to_go
        self.divider = divider


# GUI Layout

class SecondaryWindow(Screen):

    def __init__(self, **kwargs):
        # GUI from top to bottom, left to right
        super(SecondaryWindow, self).__init__(**kwargs)

        self.scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        self.scroll_btn = None

        self.scroll_grid = GridLayout(cols=2, spacing=1, size_hint_y=None)
        self.scroll_grid.bind(minimum_height=self.scroll_grid.setter('height'))

        with self.canvas:
            Color(0.2, 0.2, 0.28)
            Rectangle(size=(Window.width ** 2, Window.height ** 2))

        self.btn_live_orders = Button(size_hint_y=None, height=40, text="< Current Orders",
                                      background_color=[0.45, 0.45, 0.45, 3], on_release=self.changeWindow)
        self.scroll_grid.add_widget(self.btn_live_orders)

        self.btn_menu = Button(size_hint_y=None, height=40, text="Menu >",
                               background_color=[0.45, 0.45, 0.45, 3], on_release=self.changeWindow)
        self.scroll_grid.add_widget(self.btn_menu)

        self.drp_date = DropDown()
        self.drp_date_check = str(datetime.date.today())
        self.drp_date_btn = Button(size_hint_y=None, height=40, text=f"{self.drp_date_check}",
                                   background_color=[0.45, 0.45, 0.45, 3], on_release=self.drp_date.open)
        self.drp_date_btn_dates = None

        self.scroll_grid.add_widget(self.drp_date_btn)

        self.popup = Popup(title='Title', title_align='center',
                           content=Label(text='Text', size=(400, 400), text_size=[380, 380], halign='center',
                                         valign='center'), size_hint=(None, None), size=(400, 400))
        self.popup_db_list = []

    #     self.dropDown()
    #
    # def dropDown(self):  # Always called with __init__
    #     for i in range(len(screen_main.order_database_dates)):
    #         self.drp_date_btn_dates = Button(text=f"{screen_main.order_database_dates[i]}", size_hint_y=None,
    #                                          height=44, background_color=[0.45, 0.45, 0.45, 3],
    #                                          on_release=self.checkDate)
    #         self.drp_date.add_widget(self.drp_date_btn_dates)

    def connectSocket(self):

        host = '10.0.0.69'
        port = 8912
        address = (host, port)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(address)

        while True:
            msg = pickle.loads(client.recv(4096))
            print(msg)

    def checkDate(self, instance):
        self.drp_date_check = instance.text
        self.generateOrders()
        self.drp_date.dismiss()

    def changeWindow(self, instance):
        if 'Menu' in instance.text:
            sm.current = 'main'
            sm.transition.direction = 'left'
            self.reset()
        elif 'Orders' in instance.text:
            sm.current = 'tertiary'
            sm.transition.direction = 'right'
            self.reset()

    def reset(self):
        self.scroll_grid.clear_widgets()
        self.scroll_grid.add_widget(self.btn_live_orders)
        self.scroll_grid.add_widget(self.btn_menu)
        self.scroll_grid.add_widget(self.drp_date_btn)
        self.popup_db_list.clear()

    def popupItem(self, instance):
        num = int(instance.text.split('Order #')[-1])

        self.popup.content.text = f"{self.popup_db_list[num - 1]}"
        self.popup.title = f"Order #{num}"

        self.popup.open()

    # def generateOrders(self, instance=None, text=None):
    #     self.reset()
    #     self.drp_date_btn.text = f"{self.drp_date_check}"
    #     count = 0
    #
    #     for i in range(len(screen_main.order_database)):
    #         if self.drp_date_check == screen_main.order_database[i][:10]:
    #             self.scroll_btn = Button(text=f"Order #{(i + 1) - count}", size_hint_y=None, height=40,
    #                                      background_color=[1.8, 0.8, 0, 3], on_release=self.popupItem)
    #             self.scroll_grid.add_widget(self.scroll_btn)
    #             self.popup_db_list.append(screen_main.order_database[i])
    #         else:
    #             count += 1
    #
    #     if len(self.scroll.children) == 0:
    #         self.scroll.add_widget(self.scroll_grid)
    #         self.add_widget(self.scroll)


class TertiaryWindow(Screen):

    order_list = []
    order_list_past = []

    def __init__(self, **kwargs):
        # GUI from top to bottom, left to right
        super(TertiaryWindow, self).__init__(**kwargs)

        with self.canvas:
            Color(0.2, 0.2, 0.28)
            Rectangle(size=(Window.width ** 2, Window.height ** 2))

        self.scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        self.scroll_btn = None

        self.scroll_grid = GridLayout(cols=1, spacing=1, size_hint_y=None)
        self.scroll_grid.bind(minimum_height=self.scroll_grid.setter('height'))

        self.btn_menu = Button(size_hint_y=None, height=40, text="Order Database >",
                               background_color=[0.45, 0.45, 0.45, 3], on_release=self.changeWindow)
        self.scroll_grid.add_widget(self.btn_menu)
        self.btn_menu.set_disabled(1)

        self.btn_connecting = Button(size_hint_y=None, height=80, text="Connecting to server . . .",
                                     background_color=[1.3, 0.2, 0.2, 3],
                                     background_down='atlas://data/images/defaulttheme/button')
        self.scroll_grid.add_widget(self.btn_connecting)

        self.button_id = None
        self.div = Button(text=f"[b]----------[/b]", markup=True, size_hint_y=None, height=20,
                          background_color=[0.4, 0.4, 0.4, 3],
                          background_down='atlas://data/images/defaulttheme/button')

        self.popup = Popup(title='Notice', title_align='center',
                           content=Label(text='This order has not been submitted by the cashier yet. Please wait until'
                                              ' the order has been submitted to finish it.', size=(400, 400),
                                         text_size=[380, 380], halign='center',
                                         valign='center'), size_hint=(None, None), size=(400, 400))

        threading.Thread(target=self.connectSocket).start()

        if len(self.scroll.children) == 0:
            self.scroll.add_widget(self.scroll_grid)
            self.add_widget(self.scroll)

    def connectSocket(self):

        host = '10.0.0.69'
        port = 8912
        address = (host, port)
        header_len = 19

        while True:
            time.sleep(0.5)
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(address)
                self.scroll_grid.remove_widget(self.btn_connecting)
                self.btn_connecting.text = 'Lost connection with server. Trying to reconnect. . .'
                self.btn_menu.set_disabled(0)
                while True:
                    time.sleep(0.5)
                    header = '0'.encode()
                    try:
                        header = client.recv(10)
                        if header.decode() == 'B=G#J3>m$p':
                            print('<Connection alive>')
                    except UnicodeDecodeError:
                        msg = pickle.loads(header + client.recv(4096))
                        self.order_list_past.append(msg)
                        self.generatePastOrders()
                    except ConnectionResetError:
                        print('<Connection to server lost>')
                        self.scroll_grid.add_widget(self.btn_connecting)
                        break
            except ConnectionRefusedError:
                continue

    def changeWindow(self, instance):
        if 'Order Database' in instance.text:
            sm.current = 'secondary'
            sm.transition.direction = 'left'
            screen_second.generateOrders()

    def reset(self):
        self.scroll_grid.clear_widgets()
        self.scroll_grid.add_widget(self.btn_menu)

    def cancelOrder(self):

        temp_list = []
        temp_num = 0
        temp_total = 0
        rev = []

        for child in self.scroll_grid.children:
            rev.append(child)
        rev.reverse()

        for child in rev:
            if 'Order' not in child.text and '^ ^ ^' not in child.text and '- - -' not in child.text and '----------' not in child.text:
                temp_list.append(child)
                temp_total += 1
                continue
            elif '----------' in child.text:
                for items in temp_list:
                    temp_num += 1
                if temp_total == temp_num and temp_num > 0:
                    for item in temp_list:
                        self.scroll_grid.remove_widget(item)
                    self.scroll_grid.remove_widget(self.div)
                    temp_list.clear()
                    temp_num = 0
                    temp_total = 0
                    break
                else:
                    temp_list.clear()
                    temp_num = 0
                    temp_total = 0
            else:
                temp_list.clear()
                temp_num = 0
                temp_total = 0

    def itemFinished(self, instance=None):
        self.button_id = instance

        if "[s]" not in instance.text:
            instance.text = f"[s]{instance.text}[/s]"
            instance.background_color = [0.6, 0.6, 0.6, 3]
        else:
            instance.text = f"{instance.text[3:-4]}"
            instance.background_color = [1.8, 0.8, 0, 3]

        temp_list = []
        temp_num = 0
        temp_total = 0
        rev = []

        for child in self.scroll_grid.children:
            rev.append(child)
        rev.reverse()

        for child in rev:
            if 'Order' not in child.text and '^ ^ ^' not in child.text and '- - -' not in child.text and '----------' not in child.text:
                temp_list.append(child)
                temp_total += 1
                continue
            else:
                div = child
                for items in temp_list:
                    if '[/s]' in items.text:
                        temp_num += 1
                if temp_total == temp_num and temp_num > 0:
                    if "----------" in div.text:
                        self.popup.open()
                        instance.text = f"{instance.text[3:-4]}"
                        instance.background_color = [1.8, 0.8, 0, 3]
                        break
                    for item in temp_list:
                        self.scroll_grid.remove_widget(item)
                    self.scroll_grid.remove_widget(div)
                    temp_list.clear()
                    temp_num = 0
                    temp_total = 0
                    break
                else:
                    temp_list.clear()
                    temp_num = 0
                    temp_total = 0

    # def generateCurOrders(self, instance=None, text=None):
    #     self.cancelOrder()
    #
    #     for i in range(len(screen_main.order_list)):
    #         t = screen_main.order_list[i].time
    #         if int(t.split(':')[0]) > 12 and 'PM' not in t:
    #             hour = int(t.split(':')[0]) - 12
    #             screen_main.order_list[i].time = f"{hour}{t[-3:]} PM"
    #         else:
    #             if 'AM' not in t and 'PM' not in t:
    #                 screen_main.order_list[i].time = f"{t} AM"
    #
    #         self.scroll_grid.add_widget(
    #             Button(
    #                 text=f"{screen_main.order_list[i].details}{screen_main.order_list[i].food}"
    #                      f"{screen_main.order_list[i].to_go}   |    [b]{screen_main.order_list[i].time}[/b]",
    #                 size_hint_y=None, height=40, background_color=[1.8, 0.8, 0, 3],
    #                 markup=True, on_release=self.itemFinished))
    #
    #     if len(screen_main.order_list) > 0:
    #         self.scroll_grid.add_widget(self.div)
    #
    def generatePastOrders(self, instance=None, text=None):
        self.cancelOrder()

        for i in range(len(self.order_list_past[-1])):
            t = self.order_list_past[-1][i].time
            if int(t.split(':')[0]) > 12 and 'PM' not in t:
                hour = int(t.split(':')[0]) - 12
                self.order_list_past[-1][i].time = f"{hour}{t[-3:]} PM"
            else:
                if 'AM' not in t and 'PM' not in t:
                    self.order_list_past[-1][i].time = f"{t} AM"

            self.scroll_grid.add_widget(
                Button(
                    text=f"{self.order_list_past[-1][i].details}{self.order_list_past[-1][i].food}"
                         f"{self.order_list_past[-1][i].to_go}    |    [b]{self.order_list_past[-1][i].time}[/b]",
                    markup=True, size_hint_y=None, height=40, background_color=[1.8, 0.8, 0, 3],
                    on_release=self.itemFinished))

        # if len(screen_main.txt_name.text) == 0:
        self.scroll_grid.add_widget(
            Button(text=f"[b]- - -[/b]", markup=True, size_hint_y=None,
                   height=20, background_color=[0.4, 0.4, 0.4, 3],
                   background_down='atlas://data/images/defaulttheme/button'))
        # else:
        #     self.scroll_grid.add_widget(
        #         Button(text=f"[b]^ ^ ^ {screen_main.txt_name.text.capitalize()} ^ ^ ^[/b]", markup=True, size_hint_y=None,
        #                height=20, background_color=[0.4, 0.4, 0.4, 3],
        #                background_down='atlas://data/images/defaulttheme/button'))


class WindowManager(ScreenManager):
    pass


# Setting up the windows and window management
sm = WindowManager(transition=SlideTransition())

screen_second = SecondaryWindow(name='secondary')
screen_third = TertiaryWindow(name='tertiary')

screens = [screen_second, screen_third]
for screen in screens:
    sm.add_widget(screen)

sm.current = "tertiary"


class MyMainApp(App):

    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
