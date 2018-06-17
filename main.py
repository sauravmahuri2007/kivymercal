import kivy
kivy.require('1.0.6')

from kivy.app import App
from hisaab_uix.screens import AppFlow


__author__ = 'Saurav Kumar'
__version__ = '1.0'


class MainApp(App):
	title = 'Merchant Calculator'

	def build(self):
		return AppFlow()

	def on_pause(self):
		return True


if __name__ in ('__main__', '__android__'):
	MainApp().run()
