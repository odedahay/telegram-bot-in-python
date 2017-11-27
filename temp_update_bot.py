import requests

token ="5d81cdbe7dbfc9d973187dcd6e9f6894"

def weather_data(query):
	res=requests.get('http://api.openweathermap.org/data/2.5/weather?'+query+'&appid='+token+'&units=metric');
	return res.json();

def out_temp(result):
	temp_val = "{}'s temperature : {}°C ".format(result['name'],result['main']['temp'])
	weather_val = "Weather:{}".format(result['weather'][0]['main'])
	description_val = "Description:{}".format(result['weather'][0]['description'])

	display_result = "\n".join([temp_val, weather_val, description_val])
	return display_result

def get_temp(lat,lon):
	query = 'lat='+lat+'&lon='+lon;
	data  = weather_data(query);
	return out_temp(data)
