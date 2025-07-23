import requests

def get_ulyanovsk_weather(api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': 'Ulyanovsk',  # Название города
        'appid': api_key,  # Ваш API-ключ
        'units': 'metric',  # Температура в °C (для 'imperial' будет в °F)
        'lang': 'ru'        # Язык ответа (опционально)
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        weather_data = response.json()
        
        # Извлекаем данные
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        description = weather_data['weather'][0]['description']
        
        print(f"Температура в Ульяновске: {temp}°C (ощущается как {feels_like}°C)")
        print(f"Погода: {description.capitalize()}")
        return temp
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return 0
    except KeyError:
        print("Ошибка в формате ответа API")
        return 0

# Ваш API-ключ от OpenWeatherMap (замените на свой)
API_KEY = "e95025e9efaeced2cd9f0f960b5b6079"  # Получите на https://home.openweathermap.org/api_keys
