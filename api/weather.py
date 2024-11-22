from datetime import datetime
import requests

API_TOKEN = "a9520c4fbc4ae75a66b86e6bc5b87896"


def get_weather_data(city_name: str) -> str:
    URL = f"https://api.openweathermap.org/data/2.5/weather"
    PARAMS = {
        "appid": API_TOKEN,
        "q": city_name,
        "units": "metric",
    }
    weather_data = requests.get(url=URL, params=PARAMS)
    data = weather_data.json()

    if data["cod"] == 200:
        sunrise = str(datetime.fromtimestamp(data['sys']['sunrise']))[-8:]
        sunset = str(datetime.fromtimestamp(data['sys']['sunset']))[-8:]

        text = f"🌆  ðŸ™ï¸ <b>{data['name']}</b> da\n\n"

        text += f"🌡 Harorat: <b>{data['main']['temp']} Â°C</b>\n"
        text += f"🔺 Maks. harorat: <b>{data['main']['temp_max']} Â°C</b>\n\n"
        text += f"🔻 Min. harorat: <b>{data['main']['temp_min']} Â°C</b>\n"
        text += f"❗️ Bosim: <b>{data['main']['pressure']} Pa</b>\n"
        text += f"💧 Namlik: <b>{data['main']['humidity']} %</b>\n"
        text += f"🌬 Shamol tezligi: <b>{data['wind']['speed']} m/s</b>\n\n"
        text += f"☀️Quyosh chiqish vaqti: <b>{sunrise}</b>\n"
        text += f"🌥  Quyosh botish vaqti: <b>{sunset}</b>\n"

        return text
    else:
        return None
