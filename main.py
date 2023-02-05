import requests
from twilio.rest import Client

from data import API_KEY, MY_LAT, MY_LON, ACCOUNT_SID, AUTH_TOKEN, MY_NUMBER, MESSAGE_SERVICE_NUMBER


OWM_endpoint = "https://api.openweathermap.org/data/2.5/onecall"

weather_parameters = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "appid": API_KEY,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_endpoint, params=weather_parameters)
response.raise_for_status()
weather_data = response.json()
twelve_hour_forecast = weather_data["hourly"][:12]

will_rain = False

for hour_data in twelve_hour_forecast:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        from_=f"whatsapp:+{MESSAGE_SERVICE_NUMBER}",
        body="Będzie padać w ciągu najbliższych 12 godzin. Zabierz ze sobą parasol! ☔",
        to=F"whatsapp:+{MY_NUMBER}"
    )
