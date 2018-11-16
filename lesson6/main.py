from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout 
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.listview import ListItemButton
from kivy.factory import Factory

import json

class AddLocationForm(BoxLayout):
	search_input = ObjectProperty()
	search_results = ObjectProperty()

	def search_location(self):
		search_domain="http://api.openweathermap.org/data/2.5/find?q={}&type=like&APPID=f57ecb9a1d30725e5b652cad7e9c5a1e"
		search_url = search_domain.format(self.search_input.text)
		request = UrlRequest(search_url, self.found_location)

	def found_location(self,request,data):
		data = json.loads(data.decode()) if not isinstance(data,dict) else data
		cities = [(d['name'], d['sys']['country'])
			for d in data['list']]
		self.search_results.item_strings = cities
		del self.search_results.adapter.data[:]
		self.search_results.adapter.data.extend(cities)

	def args_converter(self, index, data_item):
		city, country = data_item
		return {'location': (city,country)}

class LocationButton(ListItemButton):
	location = ListProperty()

class WeatherRoot(BoxLayout):

	current_weather = ObjectProperty()

	def show_current_weather(self,location):
		self.clear_widgets()
		if self.current_weather is None:
			self.current_weather = CurrentWeather()
		if location is not None:
			self.current_weather.location = location
		self.current_weather.update_weather()
		self.add_widget(self.current_weather)

	def show_add_location_form(self):
		self.clear_widgets()
		self.add_widget(AddLocationForm())

class CurrentWeather(BoxLayout):
	location = ListProperty(['New York','US'])
	conditions = StringProperty()
	temp = NumericProperty()
	temp_min = NumericProperty()
	temp_max = NumericProperty()

	def update_weather(self):
		weather_domain="http://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&APPID=f57ecb9a1d30725e5b652cad7e9c5a1e"
		weather_url = weather_domain.format(*self.location)
		request = UrlRequest(weather_url, self.weather_retrieved)

	def weather_retrieved(self,request,data):
		data = json.loads(data.decode()) if not isinstance(data,dict) else data
		self.temp = data['main']['temp']
		self.conditions = data['weather'][0]['description']
		self.temp_min = data['main']['temp_min']
		self.temp_max = data['main']['temp_max']

class WeatherApp(App):
	pass 

if __name__ == '__main__':
	WeatherApp().run()

