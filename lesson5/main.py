from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout 
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.listview import ListItemButton
from kivy.factory import Factory

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
		del self.search_results.adapter.data[:]
		self.search_results.adapter.data.extend(cities)

class LocationButton(ListItemButton):
	pass

class WeatherRoot(BoxLayout):
	def show_current_weather(self,location):
		self.clear_widgets()
		current_weather = Factory.CurrentWeather()
		current_weather.location = location 
		self.add_widget(current_weather)

	def show_add_location_form(self):
		self.clear_widgets()
		self.add_widget(AddLocationForm())

class WeatherApp(App):
	pass 

if __name__ == '__main__':
	WeatherApp().run()

