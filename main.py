# This code was written by Juhyun Kim.

import time
import utime
from neopixel import Neopixel
import network
import urequests
from timezoneChange import timeOfSeoul # timezoneChange.py 파일이 같은 폴더에 있어야 동작함 
from machine import I2C
import machine 
from ssd1306 import SSD1306_I2C # ssd1306.py 파일이 같은 폴더에 있어야 동작함 
import framebuf


# 와이파이 정보 
SSID = 'U+Net454C'
password = 'DDAE014478'

# Open Wether Map API Key 
# https://openweathermap.org/appid 에서 로그인 하고 https://home.openweathermap.org/api_keys 로 이동해서 API Key를 발급받음
API_KEY = '24109ddecb29a5405afe2a8df42c5e34'

# 네오픽셀의 셀 갯수, PIO상태, 핀번호 정의 
numpix = 4
PIO = 0
Pin = 0
# 네오픽셀이 RGB타입일 때 네오픽셀 수, PIO상태, 핀번호, 네오픽셀 타입 순으로 선택, 밝기 지정 
strip = Neopixel(numpix, PIO, Pin, "RGB")
# 밝기 설정(0~255)
strip.brightness(150)

# 버튼 핀 설정 
button_pin = 22
debounce_time = 50 # 채터링 현상 방지용

current_location_index = 0
button = machine.Pin(button_pin, machine.Pin.IN, machine.Pin.PULL_UP)

previous_button_state = None
last_debounce_time = 0


# 확인하고 싶은 위치 정보 입력 
locations = [
    ('Seoul', '37.566', '126.9784'),
    ('San Francisco', '37.77493', '-122.41942'),
    ('Sevilla', '37.38283', '-5.97317')
]

# OLED 기본 설정
WIDTH  = 128 # oled display width
HEIGHT = 64  # oled display height
# Raspberry Pi logo as 32x32 bytearray
buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")


# 와이파이 연결 
def init_wifi():
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


# OLED 설정 
def init_oled():
    # Init I2C using pins GP15 & GP14 (default I2C1 pins)
    i2c = I2C(1, scl=machine.Pin(15), sda=machine.Pin(14), freq=200000)       
    print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
    print("I2C Configuration: "+str(i2c))                   # Display I2C config
    oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display
    print()
    
    return oled


# OLED 초기 화면 보여주기 
def show_startup_screen(oled):
    # OLED 클리어 
    oled.fill(0)
    # 프레임버퍼로 로고 불러오기(이미지 사이즈는  32x32)
    fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
    # 프레임 버퍼에서 OLED 디스플레이로 이미지 옮기기
    oled.blit(fb, 96, 0)
    # 글자 넣기
    oled.text("Weather Station", 0, 30)
    oled.text("   powered by", 0, 40)
    oled.text("     RPi Pico W.", 0, 50)
    # 이미지와 글자가 보여지도록 하기
    oled.show()


# 버튼 입력을 확인하고 입력되면 도시를 바꾸기 
def check_button(button, locations):
    global previous_button_state, last_debounce_time

    button_state = button.value()
    if button_state != previous_button_state:
        last_debounce_time = time.ticks_ms()

    if button_state != previous_button_state:
        previous_button_state = button_state
        if not button_state:
            current_location_index = (current_location_index + 1) % len(locations)
            return True, current_location_index
    return False, current_location_index


# OLED에 출력하기
def display_on_oled(location, weather, aqi, updatedTime):
    oled.fill(0)
    fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
    oled.blit(fb, 96, 0)
    oled.text("Loc:" + location, 0, 10)
    oled.text("Wea:" + weather, 0, 25)
    oled.text("AQI:" + str(aqi) + "(1~5)", 0, 40)
    oled.text(updatedTime, 0, 55)
    oled.show()
    
  
# 위치에 따른 공기질 정보 가져오기  
def get_air_quality_index(lat, lon, api_key):
    # 아래의 날씨 정보나 공기 오염도 조회 주소를 복사하여 브라우저의 주소창에 넣고 엔터를 누르면 JSON의 형태로 데이터를 받아볼 수 있음 
    # 시간 정보 보여주기  
    updatedTime = timeOfSeoul()
    print(updatedTime)

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

    # OLED에 출력하기
    oled.fill(0)
    # 프레임버퍼로 로고 불러오기(이미지 사이즈는  32x32)
    fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
    # 프레임 버퍼에서 OLED 디스플레이로 이미지 옮기기
    oled.blit(fb, 96, 0)
    # 글자 넣기
    oled.text("Loc:" + location, 0, 10)
    oled.text("Wea:" + weather, 0, 25)
    oled.text("AQI:" + str(aqi) +"(1~5)", 0, 40)
    oled.text(updatedTime, 0, 55)
    # 이미지와 글자가 보여지도록 하기
    oled.show()

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
def check_button(button, locations):
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



# OLED 초기화 
init_wifi()
oled = init_oled()
show_startup_screen(oled)

# locations 중 첫번째 도시로 초기화 
air_quality_index = get_air_quality_index(locations[current_location_index][1], locations[current_location_index][2], API_KEY)
set_neopixel_color(air_quality_index)
print()

# 시간 업데이트를 위한 이전 시간 저장 
last_time_update = utime.time() 


while True:
    button_pressed = check_button(button, locations)
    if button_pressed:
        location, lat, lon = locations[current_location_index]
        try:
            air_quality_index = get_air_quality_index(lat, lon, API_KEY)
            set_neopixel_color(air_quality_index)
            print()
        except Exception as e:
            print("Error:", e)
            color = (0, 0, 0)  # Black
            strip.show()

    current_time = utime.time()
    if current_time - last_time_update >= 60:
        air_quality_index = get_air_quality_index(lat, lon, API_KEY)
        set_neopixel_color(air_quality_index)
        print()
        last_time_update = current_time

    time.sleep(0.1)  # Check the button state more frequently

