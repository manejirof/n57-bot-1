# import requests
#
# def weather_func(city_name: str) -> str:
#     api_key = "101d1bedc81210570288fafc328ed721"
#
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
#
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
#
#         if data.get("cod") != 200:
#             print(f"Error: {data.get('message')}")
#             return None
#
#         return data
#
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching data: {e}")
#         return None
#
#
# print(weather_func('toshkent'))