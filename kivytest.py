# Imports
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


# GUI Layout
class MyGrid(GridLayout):

    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="First Name: "))
        self.firstName = TextInput(multiline=False)
        self.inside.add_widget(self.firstName)

        self.inside.add_widget(Label(text="Last Name: "))
        self.lastName = TextInput(multiline=False)
        self.inside.add_widget(self.lastName)

        self.inside.add_widget(Label(text="Email: "))
        self.email = TextInput(multiline=False)
        self.inside.add_widget(self.email)

        self.add_widget(self.inside)
        self.cols = 1

        self.submit = Button(text="Submit", font_size=40, color=[1, 0.5, 0, 1])
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)

    def pressed(self, instance):

        name = self.firstName.text
        last = self.lastName.text
        email = self.email.text

        print(f"Name: {name.capitalize()} {last.capitalize()}\nEmail: {email.lower()}")

        self.firstName.text = ""
        self.lastName.text = ""
        self.email.text = ""


class MyApp(App):

    def build(self):
        return MyGrid()


# Run this file
if __name__ == "__main__":
    MyApp().run()
