import requests

def get_weather_data():
    """Iegūst laiku un laikapstākļus Kuldīgai."""
    try:
        # Šis ir publisks API, kas neprasa sarežģītu autorizāciju demonstrācijai
        url = "https://wttr.in/Kuldiga?format=j1"
        response = requests.get(url, timeout=5)
        data = response.json()
        temp = data['current_condition'][0]['temp_C']
        desc = data['current_condition'][0]['weatherDesc'][0]['value']
        return f"Kuldīgā: {temp}°C, {desc}"
    except:
        return "Laikapstākļu dati nav pieejami"
