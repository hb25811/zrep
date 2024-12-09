import openai
import streamlit as st
import os
import requests

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up OpenWeatherMap API key
openweathermap_api_key = os.getenv("OPENWEATHERMAP_API_KEY")  # Ensure to replace with your key

# Function to get current weather data from OpenWeatherMap
def get_weather_data(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": openweathermap_api_key,
        "units": "metric"  # Units in Celsius
    }
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        return {
            "temperature": temperature,
            "description": weather_description,
            "humidity": humidity
        }
    else:
        return f"Error: Unable to fetch weather data for {city}. {data.get('message', '')}"

# Function to recommend smart irrigation schedule based on weather data
def recommend_irrigation(weather_info, garden_size, plant_types):
    prompt = (
        f"You are a gardening expert. Based on the following weather data and garden details, provide a smart irrigation recommendation: \n"
        f"Weather: {weather_info['description']}, Temperature: {weather_info['temperature']}°C, Humidity: {weather_info['humidity']}% \n"
        f"Garden Size: {garden_size} square meters \nPlant Types: {plant_types}"
    )
    try:
        # Use OpenAI API to generate a recommendation
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful gardening assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0]['message']['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI setup
def show():
    st.title("Smart Irrigation Recommendations")

    # User inputs for garden irrigation
    city = st.text_input("Enter your city for real-time weather updates:")
    garden_size = st.number_input("Enter the size of your garden (in square meters):", min_value=1)
    plant_types = st.text_area("Enter the types of plants in your garden:")

    if st.button("Get Irrigation Recommendation"):
        if city:
            # Get real-time weather data
            weather_info = get_weather_data(city)
            if isinstance(weather_info, dict):
                st.write(f"### Current Weather in {city}")
                st.write(f"Temperature: {weather_info['temperature']}°C")
                st.write(f"Weather: {weather_info['description']}")
                st.write(f"Humidity: {weather_info['humidity']}%")

                # Get irrigation recommendation from OpenAI
                recommendation = recommend_irrigation(weather_info, garden_size, plant_types)
                st.write("### Irrigation Recommendation:")
                st.write(recommendation)
            else:
                st.warning(weather_info)  # Display error message from the weather API
        else:
            st.warning("Please enter a valid city name.")

# Main function to call the show function
if __name__ == "__main__":
    show()
