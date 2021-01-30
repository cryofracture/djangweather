from django.shortcuts import render
import requests
import os
from dotenv import load_dotenv
load_dotenv()
from .models import City
import logging
from .forms import CityForm
# Create your views here.
def index(request):
    return render(request, 'weather/index.html') #returns the index.html template



def index(request):
    #cities = City.objects.all() #return all the cities in the database

    #url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=YOUR_APP_KEY'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate

    form = CityForm()
    
    cities = City.objects.all()
    API_KEY = os.environ['API_KEY']
    weather_data = []

    for city in cities:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city.name}&units=imperial&appid={API_KEY}"
        city_weather = requests.get(url).json()
        logging.debug(url)
        #city_weather = requests.get(url.format(city, API_KEY)).json() #request the API data and convert the JSON to Python data types
        #print(city_weather)
        weather = {
            'city' : city.name,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather) #add the data for the current city into our list

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/index.html', context) #returns the index.html template