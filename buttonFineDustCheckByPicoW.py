import time
from neopixel import Neopixel
import network
import urequests
from timezoneChange import timeOfSeoul
import machine

API_KEY = '24109ddecb29a5405afe2a8df42c5e34'

locations = [
    ('Seoul', '37.566', '126.9784'),
    ('San Francisco', '37.77493', '-122.41942'),
    ('Sevilla', '37.38283', '-5.97317')
]


SSID = 'U+Net454C'
password = 'DDAE014478'

numpix = 4
PIO = 0
Pin = 0

strip = Neopixel(numpix, PIO, Pin, "RGB")
strip.brightness(150)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect(SSID, password)
    print("Waiting for Wi-Fi connection", end="...")
    print()
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
else:
    print(wlan.ifconfig())
    print("WiFi is Connected")
    print()

button_pin = 16
button = machine.Pin(button_pin, machine.Pin.IN, machine.Pin.PULL_UP)
current_location_index = 0
previous_button_state = button.value()
debounce_time = 50
last_debounce_time = time.ticks_ms()

def get_air_quality_index(lat, lon, api_key):
    urlWeather = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    response = urequests.get(urlWeather)
    dataWeather = response.json()
    urlAQI = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
    response = urequests.get(urlAQI)
    dataAQI = response.json()

    weatherID = dataWeather['weather'][0]['id']
    weather = dataWeather['weather'][0]['description']
    location = dataWeather['name']
    print(f'Location: {location}')
    print(f'WeatherID: {weatherID}')
    print(f'Weather: {weather}')

    aqi = dataAQI['list'][0]['main']['aqi']
    print("AQI: " + str(aqi) + "[Good(1)~Bad(5)]")

    return aqi

def set_neopixel_color(aqi):
    if aqi == 1:
        color = (0, 0, 255)  # Blue
    elif aqi == 2:
        color = (255, 0, 0)  # Green
    elif aqi == 3:
        color = (255, 255, 0)  # Yellow
    elif aqi == 4:
        color = (100, 255, 0)  # Orange
    elif aqi == 5:
        color = (0, 255, 0)  # Red
    else:
        color = (0, 128, 128)  # Purple (unknown)

    for i in range(numpix):
        strip.set_pixel(i, color)
        time.sleep(0.01)
        strip.show()

def check_button():
    global current_location_index, previous_button_state, last_debounce_time

    button_state = button.value()
    if button_state != previous_button_state:
        last_debounce_time = time.ticks_ms()
    
    if button_state != previous_button_state:
        previous_button_state = button_state
        if not button_state:
            current_location_index += 1
            if current_location_index >= len(locations):
                current_location_index = 0
            return True
    return False

urlWeather = f'http://api.openweathermap.org/data/2.5/weather?lat={locations[0][1]}&lon={locations[0][2]}&appid={API_KEY}'
response = urequests.get(urlWeather)
dataWeather = response.json()
urlAQI = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={locations[0][1]}&lon=locations[0][2]&appid={API_KEY}'
response = urequests.get(urlAQI)
dataAQI = response.json()
air_quality_index = get_air_quality_index(locations[0][1], locations[0][2], API_KEY)
set_neopixel_color(air_quality_index)
print()
    
while True:
    if check_button():
        updatedTime = timeOfSeoul()
        print(updatedTime)
        
        location, lat, lon = locations[current_location_index]
        print(location, lat, lon)

        try:
            air_quality_index = get_air_quality_index(lat, lon, API_KEY)
            set_neopixel_color(air_quality_index)
            print()
        except Exception as e:
            print("Error:", e)
            color = (0, 0, 0)  # Black
            strip.show()

    time.sleep(0.1)  # Check the button state more frequently

