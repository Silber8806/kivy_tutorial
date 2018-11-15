from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout 
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest

import json

class AddLocationForm(BoxLayout):
	search_input = ObjectProperty()
	search_results = ObjectProperty()

	def search_location(self):
		print("starting search...")
		search_domain="http://api.openweathermap.org/data/2.5/find?q={}&type=like&APPID=f57ecb9a1d30725e5b652cad7e9c5a1e"
		search_url = search_domain.format(self.search_input.text)
		print("search url: {}".format(search_url))
		request = UrlRequest(search_url, self.found_location)

	def found_location(self,request,data):
		data = json.loads(data.decode()) if not isinstance(data,dict) else data
		cities = ["{} ({})".format(d['name'], d['sys']['country'])
			for d in data['list']]
		self.search_results.item_strings = cities

class WeatherApp(App):
	pass 

if __name__ == '__main__':
	WeatherApp().run()

