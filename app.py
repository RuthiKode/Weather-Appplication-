from flask import Flask, render_template, request
import requests
import os  # Import os to read environment variables

app = Flask(__name__)

# Use environment variable for API_KEY
API_KEY = os.getenv('API_KEY')  # This will fetch the API_KEY from environment variables

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    country = request.form['country']
    weather_data = fetch_weather(city, country)
    return render_template('result.html', data=weather_data)

def fetch_weather(city, country):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    query = f"{city},{country}"
    params = {
        "q": query,
        "appid": API_KEY,  # API key is fetched from environment
        "units": "metric"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "city": data['name'],
            "country": data['sys']['country'],
            "description": data['weather'][0]['description'],
            "temperature": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "wind_speed": data['wind']['speed'],
            "error": None
        }
    except requests.exceptions.HTTPError:
        return {"error": f"City '{city}' not found in country '{country}'."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}

if __name__ == '__main__':
    app.run(debug=True)
