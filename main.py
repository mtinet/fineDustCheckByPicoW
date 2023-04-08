# This code was written by Juhyun Kim.

import time
from neopixel import Neopixel
import network
import urequests
from timezoneChange import timeOfSeoul # timezoneChange.py 파일이 같은 폴더에 있어야 동작함 
import machine


# 와이파이 정보 
SSID = 'U+Net454C'
password = 'DDAE014478'

# 와이파이 연결하기
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    # 와이파이 연결하기
    wlan.connect(SSID, password)  # 12, 13번 줄에 입력한 SSID와 password가 입력됨
    print("Waiting for Wi-Fi connection", end="...")
    print()
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
else:
    print(wlan.ifconfig())
    print("WiFi is Connected")
    print()
    
    
# 자기 정보 넣기(Open Wether Map API Key, 측정하고자 하는 곳의 위도, 경도 정보, 자신이 사용하는 WiFi정보) 
# https://openweathermap.org/appid 에서 로그인 하고 https://home.openweathermap.org/api_keys 로 이동해서 API Key를 발급받음
API_KEY = '24109ddecb29a5405afe2a8df42c5e34'

# 확인하고 싶은 위치 정보 입력 
locations = [
    ('Seoul', '37.566', '126.9784'),
    ('San Francisco', '37.77493', '-122.41942'),
    ('Sevilla', '37.38283', '-5.97317')
]


# 네오픽셀의 셀 갯수, PIO상태, 핀번호 정의 
numpix = 4
PIO = 0
Pin = 0

# 네오픽셀이 RGB타입일 때 네오픽셀 수, PIO상태, 핀번호, 네오픽셀 타입 순으로 선택, 밝기 지정 
strip = Neopixel(numpix, PIO, Pin, "RGB")

# 밝기 설정(0~255)
strip.brightness(150)


# 버튼 핀 설정 
button_pin = 29
button = machine.Pin(button_pin, machine.Pin.IN, machine.Pin.PULL_UP)
current_location_index = 0
previous_button_state = button.value()
debounce_time = 50
last_debounce_time = time.ticks_ms()


# 위치에 따른 공기질 정보 가져오기  
def get_air_quality_index(lat, lon, api_key):
    # 아래의 날씨 정보나 공기 오염도 조회 주소를 복사하여 브라우저의 주소창에 넣고 엔터를 누르면 JSON의 형태로 데이터를 받아볼 수 있음 
    # 날씨 정보 조회
    # http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}
    urlWeather = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    response = urequests.get(urlWeather)
    dataWeather = response.json()
    
    # 공기 오염도 조회
    # http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}
    urlAQI = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
    response = urequests.get(urlAQI)
    dataAQI = response.json()

    # weather는 설명이 직접 넘어옴
    # WeatherID 참고 링크: https://injunech.tistory.com/178
    weatherID = dataWeather['weather'][0]['id']
    weather = dataWeather['weather'][0]['description']
    location = dataWeather['name']
    print(f'Location: {location}')
    print(f'WeatherID: {weatherID}')
    print(f'Weather: {weather}')

    # aqi는 Air Quality Index
    # aqi = 1 # 1~5까지의 인덱스로 아래의 실제 데이터 대신 테스트 해볼 수 있음 
    aqi = dataAQI['list'][0]['main']['aqi']
    print("AQI: " + str(aqi) + "[Good(1)~Bad(5)]")

    return aqi

# 공기질에 따라 네오픽셀 색깔 지정하기  
def set_neopixel_color(aqi):
    # Green, Red, Blue의 순서로 되어 있음
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

# 버튼 입력을 확인하고 입력되면 도시를 바꾸기  
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

# 초기 설정(locations 중 첫번째 도시)
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
        # 시간 정보 보여주기  
        updatedTime = timeOfSeoul()
        print(updatedTime)
        
        # 위치 정보 보여주기
        location, lat, lon = locations[current_location_index]
        print(location, lat, lon)

        try:
            # 다음 도시의 공기질 정보 보여주기  
            air_quality_index = get_air_quality_index(lat, lon, API_KEY)
            set_neopixel_color(air_quality_index)
            print()
        except Exception as e:
            print("Error:", e)
            color = (0, 0, 0)  # Black
            strip.show()

    time.sleep(0.1)  # Check the button state more frequently

