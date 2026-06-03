from django.shortcuts import render
import requests

def index(request):

    BASE_URL = 'http://api.weatherapi.com/v1'
    API_KEY = '6e2b74fe3a5845909f7132848262705'  # Your API Key

    if request.method == 'POST':
        city = request.POST.get('city').lower()
        print(f"Searching for: {city}")

        if not city or city == '':
            print('Empty city')
            return render(request, 'index.html', {'checker': 'Please enter a city name!'})

        request_url = f"{BASE_URL}/current.json?key={API_KEY}&q={city}&aqi=no"
        response = requests.get(request_url)

        if response.status_code == 200:
            data = response.json()
            location = data['location']
            weather = data['current']
            
            context = {
                'weather': weather['temp_c'],
                'city_name': location['name'],
                'region': location['region'],
                'country': location['country'],
                'lat': location['lat'],
                'lon': location['lon'],
                'localtime': location['localtime'],
                'continent': location['tz_id'],
                'static_city': city,
                'checker': None,
            }
            
            print(f" Success: {location['name']} - {weather['temp_c']}°C")
            return render(request, 'index.html', context)

        else:
            print(f" Error {response.status_code}: City '{city}' not found")
            return render(request, 'index.html', {
                'static_city': city, 
                'checker': f'City "{city}" not found. Please enter a valid city name.'
            })

    return render(request, 'index.html', {})