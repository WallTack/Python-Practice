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
class MainWindow(Screen):
    total = 0
    tax_rate = 1.093

    current_item = None
    current_time = None
    order_list = []
    order_count = 1
    order_list_details = {}
    order_list_times = []
    order_list_times_past = []
    live_orders_timed = []
    time = []
    order_database = {}
    order_database_dates = {}
    vendor = False

    menu_dict = {'All-Veg Sampler': 9.25, 'Alumutter': 8}
    menu_dict_vendor = {'All-Veg Sampler': 7, 'Alumutter': 6}

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        self.background = FloatLayout()

        self.callDatabase()

        with self.canvas:
            Color(0.2, 0.2, 0.28)
            Rectangle(size=(Window.width ** 2, Window.height ** 2))
            # Color(1, 0, 0, .5, mode='rgba')
            # Rectangle(pos=self.pos, size=(210,210))
            # Color(0.2, 0.2, 0.28)
            # Rectangle(pos=self.pos, size=(200,200))

        # Food labels
        self.lbl_curry = Label(pos_hint={"x": 0.11, "y": 0.92}, size_hint=[0.1, 0.08], font_size=20,
                               color=[1, 0.5, 0, 1], text="[b]Curry[/b]",
                               markup=True)

        # Menu food item buttons

        self.btn_allveg = Button(pos_hint={"x": 0.01, "y": 0.85}, size_hint=[0.15, 0.08], text="Chicken",
                                 background_color=[1.6, 0.7, 0, 3], on_release=self.pressed)

        self.btn_allveg = Button(pos_hint={"x": 0.01, "y": 0.85}, size_hint=[0.15, 0.08], text="All-Veg Sampler",
                                 background_color=[1.6, 0.7, 0, 3], on_release=self.pressed)

        self.btn_allveg = Button(pos_hint={"x": 0.01, "y": 0.85}, size_hint=[0.15, 0.08], text="All-Veg Sampler",
                                 background_color=[1.6, 0.7, 0, 3], on_release=self.pressed)

        self.btn_allveg = Button(pos_hint={"x": 0.01, "y": 0.85}, size_hint=[0.15, 0.08], text="All-Veg Sampler",
                                 background_color=[1.6, 0.7, 0, 3], on_release=self.pressed)

        self.btn_allveg = Button(pos_hint={"x": 0.01, "y": 0.85}, size_hint=[0.15, 0.08], text="All-Veg Sampler",
                                 background_color=[1.6, 0.7, 0, 3], on_release=self.pressed)

        self.btn_allveg = Button(pos_hint={"x": 0.01, "y": 0.85}, size_hint=[0.15, 0.08], text="All-Veg Sampler",
                                 background_color=[1.6, 0.7, 0, 3], on_release=self.pressed)

        self.btn_allveg = Button(pos_hint={"x": 0.01, "y": 0.85}, size_hint=[0.15, 0.08], text="All-Veg Sampler",
                                 background_color=[1.6, 0.7, 0, 3], on_release=self.pressed)

        self.btn_allveg = Button(pos_hint={"x": 0.01, "y": 0.85}, size_hint=[0.15, 0.08], text="All-Veg Sampler",
                                 background_color=[1.6, 0.7, 0, 3], on_release=self.pressed)

        self.btn_alumutter = Button(pos_hint={"x": 0.16, "y": 0.85}, size_hint=[0.15, 0.08], text="Alumutter",
                                    background_color=[1.6, 0.7, 0, 3], on_release=self.pressed)

        # Other non-food panels of GUI

        self.lbl_subtotal = Label(pos_hint={"x": 0.48, "y": 0.3}, size_hint=[0.8, 0.2], font_size=15,
                                  color=[0.4, 0.4, 0.6], text=f"Subtotal: ${self.total}", markup=True)

        self.lbl_tax = Label(pos_hint={"x": 0.48, "y": 0.27}, size_hint=[0.8, 0.2], font_size=15, color=[0.4, 0.4, 0.6],
                             text=f"Tax: ${self.total}", markup=True)

        self.lbl_total = Label(pos_hint={"x": 0.48, "y": 0.23}, size_hint=[0.8, 0.2], font_size=25,
                               color=[0.6, 0.6, 0.8],
                               text=f"Total: ${self.total}", markup=True)

        self.btn_complete = Button(pos_hint={"x": 0.78, "y": 0.2}, size_hint=[0.2, 0.1], text="Complete Order",
                                   background_color=[0.6, 0.5, 0.9, 3], on_release=self.submitOrder)

        self.btn_cancel = Button(pos_hint={"x": 0.914, "y": 0.118}, size_hint=[0.0666, 0.08], text="Cancel\n Order",
                                 background_color=[1.3, 0.3, 0.3, 3], font_size=14, on_release=self.cancelOrderPopup)

        self.btn_vendor = Button(pos_hint={"x": 0.847, "y": 0.118}, size_hint=[0.0666, 0.08], text="Vendor",
                                 background_color=[0.2, 0.5, 0.9, 3], font_size=14, on_release=self.vendorCheck)

        self.btn_to_go = Button(pos_hint={"x": 0.78, "y": 0.118}, size_hint=[0.0666, 0.08], text="To-Go",
                                background_color=[0.4, 0.8, 0.4, 3], font_size=14, on_release=self.toGo)

        self.txt_name = TextInput(pos_hint={"x": 0.7805, "y": 0.062}, size_hint=[0.2, 0.055], text='',
                                  background_color=[0.1, 0.45, 0.45, 3], multiline=False, halign='center',
                                  hint_text='Customer Name', hint_text_color=[0.8, 0.8, 0.8, 1])

        self.btn_orders = Button(pos_hint={"right": 1, "top": 1}, size_hint=[0.03, 1], text="",
                                 background_color=[0.8, 0.8, 1, 0.02], on_release=self.changeWindow, markup=True)

        # Instantiate the GUI

        self.addWidgets(self.btn_orders, self.lbl_curry, self.btn_allveg, self.btn_alumutter, self.lbl_subtotal,
                        self.lbl_tax, self.btn_to_go, self.txt_name, self.lbl_total, self.btn_cancel, self.btn_complete,
                        self.btn_vendor)

        self.add_widget(self.background)

        # Popup for order cancellation confirmation

        self.popup_cancel_grid = GridLayout(cols=1, spacing=20, size_hint=(1, 0.95), size=(Window.width, Window.height))

        self.popup_cancel = Popup(title='Confirmation', title_align='center',
                                  content=self.popup_cancel_grid, pos_hint={'x': 0.75, 'y': 0.03},
                                  size_hint=(0.23, 0.33), size=(Window.width, Window.height))

        self.popup_cancel_grid.add_widget(Label(text='Are you sure you want \nto cancel this order?'))

        self.popup_cancel_grid.add_widget(
            Button(text='No', size=(100, 100), text_size=(Window.width / 5.5, Window.height),
                   halign='center', valign='center', on_release=self.popup_cancel.dismiss,
                   background_color=[0, 1.4, 1.45, 3]))

        self.popup_cancel_grid.add_widget(
            Button(text='Yes', size=(100, 100), text_size=(Window.width / 5.5, Window.height),
                   halign='center', valign='center', on_release=self.popup_cancel.dismiss,
                   on_press=self.resetOrder, background_color=[1.3, 0.2, 0.2, 3]))

        # Scroll window to list the current items

        self.scroll_grid = GridLayout(cols=1, spacing=0, size_hint_y=None,
                                      size_hint_x=self.background.height / self.background.width)
        self.scroll_grid.bind(minimum_height=self.scroll_grid.setter('height'))

        self.scroll = ScrollView(size_hint=[0.159, 0.525], pos_hint={'x': 0.82, 'y': 0.45})
        self.scroll_btn = None

        # Popup window shown when an item in the scroll view is indicated

        self.popup_grid = GridLayout(cols=1, spacing=20, size_hint=(1, 0.95), pos_hint={'bottom': 0.2},
                                     size=(Window.width, Window.height))
        self.popup_grid_top = GridLayout(cols=2, spacing=20, size_hint=(1, 1), pos_hint={'top': 0.95},
                                         size=(Window.width, Window.height))

        self.popup_btn_delete = Button(text='Text', size=(100, 100), text_size=(Window.width / 5.5, Window.height),
                                       halign='center', valign='center', on_release=self.removeItem,
                                       background_color=[0.9, 0.2, 0.2, 3])

        self.popup_btn_to_go = Button(text='Text', size=(100, 100), text_size=(Window.width / 5.5, Window.height),
                                      halign='center', valign='center', on_release=self.toGo,
                                      background_color=[0.4, 0.8, 0.4, 3])

        self.popup_btn_no_cilantro = Button(text='No Cilantro', size=(100, 100),
                                            text_size=(Window.width / 5.5, Window.height),
                                            halign='center', valign='center', on_release=self.cilantroMod,
                                            background_color=[0.3, 1.4, 1.4, 3])

        self.popup_btn_extra_cilantro = Button(text='Extra Cilantro', size=(100, 100),
                                               text_size=(Window.width / 5.5, Window.height),
                                               halign='center', valign='center', on_release=self.cilantroMod,
                                               background_color=[0.3, 1.4, 1.4, 3])

        self.popup_txt = TextInput(size_hint=[1, 0.4], text='', background_color=[0.4, 0.3, 0.6, 3],
                                   multiline=False, halign='center', font_size=18, padding_y=33,
                                   hint_text='Enter Order Details', hint_text_color=[0.8, 0.8, 0.8, 1])

        self.popup_grid_top.add_widget(self.popup_btn_delete)
        self.popup_grid_top.add_widget(self.popup_btn_to_go)
        self.popup_grid_top.add_widget(self.popup_btn_no_cilantro)
        self.popup_grid_top.add_widget(self.popup_btn_extra_cilantro)
        self.popup_grid.add_widget(self.popup_grid_top)
        self.popup_grid.add_widget(self.popup_txt)

        self.popup = Popup(title='Title', title_align='center', content=self.popup_grid, on_dismiss=self.addDetails,
                           size_hint=(0.45, 0.7), size=(Window.width, Window.height))
        self.button_id = None
        self.data = None
        self.data_backups = []
        self.client_socket = None
        try:
            threading.Thread(target=self.connectSocket).start()
        except Exception as e:
            print(f'Error: {e}')

    def connectSocket(self, instance=None):

        host = '0.0.0.0'
        port = 8912
        address = (host, port)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(address)
        server.listen(5)
        print(f'Listening on {socket.gethostbyname(socket.gethostname())}:{port}')

        while True:
            conn, addr = server.accept()
            print(f"Connection from {address} has been established.")
            self.client_socket = conn
            while True:
                time.sleep(0.5)
                try:
                    conn.send('B=G#J4>m$p'.encode())
                except ConnectionResetError:
                    print('Connection with client lost.')
                    break

    def generateCurOrder(self):

        self.scroll_btn = Button(text=f"{self.order_list[-1].food}", font_size=11, size_hint_y=None, height=33,
                                 background_color=[0.7, 0.7, 1, 1], on_release=self.popupItem)
        self.scroll_grid.add_widget(self.scroll_btn)

        if len(self.scroll.children) == 0:
            self.scroll.add_widget(self.scroll_grid)
            self.background.add_widget(self.scroll)

    # def duplicateItem(self, instance):                    //-- Decided not to use this stuff but I'll keep it here
    #                                                      //--        in case I change my mind later.
    #     for i in range(self.popup_slider.value):
    #         self.scroll_btn = Button(text=f"{self.order_list[self.order_list.index(self.button_id.text)]}",
    #                                  font_size=12, size_hint_y=None, height=33,
    #                                  background_color=[0.7, 0.7, 1, 1], on_release=self.popupItem)
    #         self.scroll_grid.add_widget(self.scroll_btn)
    #         self.order_list.append(self.button_id.text)
    #         self.addTotal(self.menu_dict[self.button_id.text])
    #
    # def updateSlider(self, instance, touch):
    #     if self.popup_slider.value == 1:
    #         self.popup_slider_btn.text = f"Duplicate this item {int(self.popup_slider.value)} time"
    #     else:
    #         self.popup_slider_btn.text = f"Duplicate this item {int(self.popup_slider.value)} times"
    #
    # self.popup_slider = Slider(min=1, max=10, value=1, step=1, value_track=True,
    #                            value_track_color=[0.4, 0.4, 0.6, 1],
    #                            on_touch_move=self.updateSlider)
    #
    # self.popup_slider_btn = Button(font_size=20, background_color=[0.7, 0.7, 1, 1], on_release=self.duplicateItem,
    #                                text=f"Duplicate this item {int(self.popup_slider.value)} time", markup=True)
    #
    # self.popup_grid.add_widget(self.popup_slider)
    # self.popup_grid.add_widget(self.popup_slider_btn)

    def addTotal(self, x):

        self.total += x

        subtotal = format(self.total, '.2f')
        tax = format((self.total * self.tax_rate) - self.total, '.2f')
        total = format(float(subtotal) + float(tax), '.2f')

        self.lbl_subtotal.text = f"Subtotal: ${subtotal}"
        self.lbl_tax.text = f"Tax: ${tax}"

        self.lbl_total.text = f"Total: ${total}"

    def addList(self):

        self.current_item.time = str(datetime.datetime.now())[:19][11:-3]
        self.order_list.append(self.current_item)

        screen_third.generateCurOrders()

    def addDetails(self, instance=None):

        if self.popup_txt.text != '':
            num = 1
            rev = []

            for child in self.scroll_grid.children:
                rev.append(child)
            rev.reverse()

            for i in range(len(rev)):
                if rev[i] == self.button_id:
                    break
                else:
                    num += 1

            for i in range(len(self.order_list)):
                if self.order_list[i].food == self.button_id.text:
                    if self.order_list[i].order_id == num:
                        self.order_list[i].details = f"({self.popup_txt.text}) "
                        break

        screen_third.generateCurOrders()

    def submitOrder(self, instance=None):

        if len(self.order_list) > 0:
            self.live_orders_timed = [self.order_list.copy()]
            self.order_database[len(self.order_database)] = f"{str(datetime.datetime.now())[:19]} - " \
                                                            f"{[x.food for x in self.live_orders_timed[-1]]}"
            with open('database.txt', 'a') as db:
                db.write(f"{str(datetime.datetime.now())[:19]} - {[x.food for x in self.live_orders_timed[-1]]} - "
                         f"${format((self.total * self.tax_rate), '.2f')}\n")

            self.data = [x for x in self.order_list]
            msg = pickle.dumps(self.data)
            try:
                if len(self.data_backups) > 0:
                    self.client_socket.send(pickle.dumps(self.data_backups))
                    self.data_backups.clear()
                    print('<INFO> Backups sent to client.')
                self.client_socket.send(msg)
            except Exception as e:
                if ['BACKUP'] not in self.data_backups:
                    self.data_backups.append(['BACKUP'])
                self.data_backups.append([x.food for x in self.order_list])
                print(f'<ERROR> No connection with client. Backup data created.\n{e}')

            screen_third.generatePastOrders()

            self.resetOrder()
            screen_third.scroll_grid.remove_widget(screen_third.div)

    def cancelOrderPopup(self, instance=None):

        if len(self.order_list) > 0:
            self.popup_cancel.open()

    def resetOrder(self, instance=None):

        self.total = 0
        self.current_item = OrderItem(order_id=0)
        self.order_list.clear()
        self.lbl_subtotal.text = f"Subtotal: ${self.total}"
        self.lbl_tax.text = f"Tax: ${self.total}"
        self.lbl_total.text = f"Total: ${self.total}"
        self.scroll_grid.clear_widgets()
        self.txt_name.text = ''
        self.order_count = 1

        self.background.remove_widget(self.btn_to_go)
        self.btn_to_go = Button(pos_hint={"x": 0.78, "y": 0.118}, size_hint=[0.0666, 0.08], text="To-Go",
                                background_color=[0.4, 0.8, 0.4, 3], font_size=14, on_release=self.toGo)
        self.addWidgets(self.btn_to_go)

        screen_third.cancelOrder()

    @staticmethod
    def changeWindow(instance):
        sm.current = 'tertiary'
        sm.transition.direction = 'left'

    def callDatabase(self):  # This is always called with __init__
        count = 0

        with open('database.txt', 'r') as db:
            for line in db:
                self.time.append(f"{line[:19]}")
                self.order_database[count] = line[:-1]
                self.order_database_dates[line[:10]] = None
                count += 1

        self.order_database_dates = [key for key in self.order_database_dates]

    def popupItem(self, instance):

        self.button_id = instance
        num = 1
        rev = []

        for child in self.scroll_grid.children:
            rev.append(child)
        rev.reverse()

        for i in range(len(rev)):
            if rev[i] == self.button_id:
                break
            else:
                num += 1

        for i in range(len(self.order_list)):
            if self.order_list[i].food == self.button_id.text:
                if self.order_list[i].order_id == num:
                    self.popup_txt.text = self.order_list[i].details[1:-2]
                    break

        self.popup.title = f'Options for selected item - {instance.text}'
        self.popup_btn_delete.text = f"Remove this '{instance.text}' from the order."
        if "TO-GO" not in instance.text:
            self.popup_btn_to_go.text = f"Make this order to-go."
        else:
            self.popup_btn_to_go.text = f"Make this '{instance.text[:-6]}' for here."

        self.popup.open()

    def vendorCheck(self, instance=None):

        if self.vendor:
            self.vendor = False
            instance.background_normal = 'atlas://data/images/defaulttheme/button'
            self.vendorGen()
        else:
            self.vendor = True
            instance.background_normal = 'atlas://data/images/defaulttheme/button_pressed'
            self.vendorGen()

    def vendorGen(self, instance=None):

        self.total = 0

        if self.vendor:
            for item in self.order_list:
                self.addTotal(self.menu_dict_vendor[item.food])
        else:
            for item in self.order_list:
                self.addTotal(self.menu_dict[item.food])

    def cilantroMod(self, instance=None):

        if instance.text == 'No Cilantro':
            if self.popup_txt.text != '' and 'Cilantro' not in self.popup_txt.text:
                self.popup_txt.text = f"{self.popup_txt.text}, No Cilantro"
            elif 'No Cilantro' in self.popup_txt.text:
                pass
            elif ', Extra Cilantro' in self.popup_txt.text:
                self.popup_txt.text = f"{self.popup_txt.text.split(',')[0]}, No Cilantro"
            else:
                self.popup_txt.text = 'No Cilantro'
        else:
            if self.popup_txt.text != '' and 'Cilantro' not in self.popup_txt.text:
                self.popup_txt.text = f"{self.popup_txt.text}, Extra Cilantro"
            elif 'Extra Cilantro' in self.popup_txt.text:
                pass
            elif ', No Cilantro' in self.popup_txt.text:
                self.popup_txt.text = f"{self.popup_txt.text.split(',')[0]}, Extra Cilantro"
            else:
                self.popup_txt.text = 'Extra Cilantro'

    # def toGo(self, instance=None):
    #
    #     if "TO-GO" not in self.button_id.text:
    #         i = self.order_list.index(self.button_id.text)
    #         self.button_id.text = f"{self.order_list[i]} TO-GO"
    #         self.order_list[i] = f"{self.order_list[i]} [b]|| [u]TO-GO[/u] ||[/b]"
    #         screen_third.generateCurOrders()
    #     else:
    #         self.button_id.text = self.button_id.text[:-6]
    #         screen_third.generateCurOrders()
    #         for i in range(len(self.order_list)):
    #             if "TO-GO[/u] ||[/b]" in self.order_list[i] and self.button_id.text in self.order_list[i]:
    #                 self.order_list[i] = self.order_list[i][:-26]
    #                 break
    #
    #     screen_third.generateCurOrders()
    #
    #     self.popup.dismiss()

    def toGo(self, instance=None):

        if len(self.order_list) > 0:
            for i in range(len(self.order_list)):
                self.order_list[i].to_go = ' [b][u]TO-GO[/u][/b]'

            self.background.remove_widget(self.btn_to_go)
            self.btn_to_go = Button(pos_hint={"x": 0.78, "y": 0.118}, size_hint=[0.0666, 0.08], text="To-Go",
                                    background_color=[0.4, 0.8, 0.4, 3], font_size=14, on_release=self.forHere,
                                    background_normal='atlas://data/images/defaulttheme/button_pressed')
            self.addWidgets(self.btn_to_go)
            screen_third.generateCurOrders()

    def forHere(self, instance=None):

        if len(self.order_list) > 0:
            for i in range(len(self.order_list)):
                self.order_list[i].to_go = ''

            self.background.remove_widget(self.btn_to_go)
            self.btn_to_go = Button(pos_hint={"x": 0.78, "y": 0.118}, size_hint=[0.0666, 0.08], text="To-Go",
                                    background_color=[0.4, 0.8, 0.4, 3], font_size=14, on_release=self.toGo,
                                    background_normal='atlas://data/images/defaulttheme/button')
            self.addWidgets(self.btn_to_go)
            screen_third.generateCurOrders()

    def removeItem(self, instance):

        count = 0

        for i in range(len(self.scroll_grid.children)):
            if self.scroll_grid.children[i] != self.button_id:
                count += 1
            else:
                break

        self.order_list.remove(self.order_list[count])

        if self.vendor:
            self.addTotal(-self.menu_dict_vendor[self.button_id.text])
        else:
            self.addTotal(-self.menu_dict[self.button_id.text])

        self.scroll_grid.remove_widget(self.button_id)
        self.popup.dismiss()
        self.order_count -= 1

        screen_third.generateCurOrders()

        if len(self.order_list) == 0:
            self.resetOrder()
            screen_third.scroll_grid.remove_widget(screen_third.div)

    def addWidgets(self, *args):

        for i in args:
            self.background.add_widget(i)

    def pressed(self, instance):

        self.current_item = OrderItem(order_id=self.order_count,food=instance.text)
        self.order_count += 1
        self.addList()
        self.vendorGen()
        self.generateCurOrder()


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
        self.dropDown()

    def dropDown(self):  # Always called with __init__
        for i in range(len(screen_main.order_database_dates)):
            self.drp_date_btn_dates = Button(text=f"{screen_main.order_database_dates[i]}", size_hint_y=None,
                                             height=44, background_color=[0.45, 0.45, 0.45, 3],
                                             on_release=self.checkDate)
            self.drp_date.add_widget(self.drp_date_btn_dates)

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

    def generateOrders(self, instance=None, text=None):
        self.reset()
        self.drp_date_btn.text = f"{self.drp_date_check}"
        count = 0

        for i in range(len(screen_main.order_database)):
            if self.drp_date_check == screen_main.order_database[i][:10]:
                self.scroll_btn = Button(text=f"Order #{(i + 1) - count}", size_hint_y=None, height=40,
                                         background_color=[1.8, 0.8, 0, 3], on_release=self.popupItem)
                self.scroll_grid.add_widget(self.scroll_btn)
                self.popup_db_list.append(screen_main.order_database[i])
            else:
                count += 1

        if len(self.scroll.children) == 0:
            self.scroll.add_widget(self.scroll_grid)
            self.add_widget(self.scroll)


class TertiaryWindow(Screen):

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

        self.button_id = None
        self.div = Button(text=f"[b]----------[/b]", markup=True, size_hint_y=None, height=20,
                          background_color=[0.4, 0.4, 0.4, 3],
                          background_down='atlas://data/images/defaulttheme/button')

        self.popup = Popup(title='Notice', title_align='center',
                           content=Label(text='This order has not been submitted by the cashier yet. Please wait until'
                                              ' the order has been submitted to finish it.', size=(400, 400),
                                         text_size=[380, 380], halign='center',
                                         valign='center'), size_hint=(None, None), size=(400, 400))

        if len(self.scroll.children) == 0:
            self.scroll.add_widget(self.scroll_grid)
            self.add_widget(self.scroll)

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

    def generateCurOrders(self, instance=None, text=None):
        self.cancelOrder()

        for i in range(len(screen_main.order_list)):
            t = screen_main.order_list[i].time
            if int(t.split(':')[0]) > 12 and 'PM' not in t:
                hour = int(t.split(':')[0]) - 12
                screen_main.order_list[i].time = f"{hour}{t[-3:]} PM"
            else:
                if 'AM' not in t and 'PM' not in t:
                    screen_main.order_list[i].time = f"{t} AM"

            self.scroll_grid.add_widget(
                Button(
                    text=f"{screen_main.order_list[i].details}{screen_main.order_list[i].food}"
                         f"{screen_main.order_list[i].to_go}   |    [b]{screen_main.order_list[i].time}[/b]",
                    size_hint_y=None, height=40, background_color=[1.8, 0.8, 0, 3],
                    markup=True, on_release=self.itemFinished))

        if len(screen_main.order_list) > 0:
            self.scroll_grid.add_widget(self.div)

    def generatePastOrders(self, instance=None, text=None):
        self.cancelOrder()

        for i in range(len(screen_main.live_orders_timed[-1])):
            t = screen_main.live_orders_timed[-1][i].time
            if int(t.split(':')[0]) > 12 and 'PM' not in t:
                hour = int(t.split(':')[0]) - 12
                screen_main.live_orders_timed[-1][i].time = f"{hour}{t[-3:]} PM"
            else:
                if 'AM' not in t and 'PM' not in t:
                    screen_main.live_orders_timed[-1][i].time = f"{t} AM"

            self.scroll_grid.add_widget(
                Button(
                    text=f"{screen_main.live_orders_timed[-1][i].details}{screen_main.live_orders_timed[-1][i].food}"
                         f"{screen_main.live_orders_timed[-1][i].to_go}    |    [b]{screen_main.live_orders_timed[-1][i].time}[/b]",
                    markup=True, size_hint_y=None, height=40, background_color=[1.8, 0.8, 0, 3],
                    on_release=self.itemFinished))

        if len(screen_main.txt_name.text) == 0:
            self.scroll_grid.add_widget(
                Button(text=f"[b]- - -[/b]", markup=True, size_hint_y=None,
                       height=20, background_color=[0.4, 0.4, 0.4, 3],
                       background_down='atlas://data/images/defaulttheme/button'))
        else:
            self.scroll_grid.add_widget(
                Button(text=f"[b]^ ^ ^ {screen_main.txt_name.text.capitalize()} ^ ^ ^[/b]", markup=True, size_hint_y=None,
                       height=20, background_color=[0.4, 0.4, 0.4, 3],
                       background_down='atlas://data/images/defaulttheme/button'))


class WindowManager(ScreenManager):
    pass


# Setting up the windows and window management
sm = WindowManager(transition=SlideTransition())

screen_main = MainWindow(name='main')
screen_second = SecondaryWindow(name='secondary')
screen_third = TertiaryWindow(name='tertiary')

screens = [screen_main, screen_second, screen_third]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"


class MyMainApp(App):

    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
