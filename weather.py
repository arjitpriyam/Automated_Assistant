import requests
api_address = 'https://api.openweathermap.org/data/2.5/weather?appid=afa3ebada3c264c1ca0e9c048462837f&q='
city = "Delhi"

url = api_address+city
json_data = requests.get(url).json()
formatted_data = (json_data['main']['temp']) - 273.15
print(formatted_data)