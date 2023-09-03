import network
import urequests
from timezoneChange import timeOfSeoul # timezoneChange.py 파일이 같은 폴더에 있어야 동작함 

# 와이파이 정보 
SSID = 'U+Net454C'
password = 'DDAE014478'

# 자기 정보 넣기(Open Wether Map API Key, 측정하고자 하는 곳의 위도, 경도 정보, 자신이 사용하는 WiFi정보) 
# https://openweathermap.org/appid 에서 로그인 하고 https://home.openweathermap.org/api_keys 로 이동해서 API Key를 발급받음
api_key = '24109ddecb29a5405afe2a8df42c5e34'

# GPS 좌표 설정
lat='37.566'
lon='126.9784'

# 와이파이 연결하기
def wifiConnect():
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

# 와이파이 함수 실행
wifiConnect()

# 날씨 정보 조회
# http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}
urlWeather = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
response = urequests.get(urlWeather)
dataWeather = response.json()
print(dataWeather)
print()


# weather는 설명이 직접 넘어옴
# WeatherID 참고 링크: https://injunech.tistory.com/178
weatherID = dataWeather['weather'][0]['id']
weather = dataWeather['weather'][0]['description']
location = dataWeather['name']
print(f'Location: {location}')
print(f'WeatherID: {weatherID}')
print(f'Weather: {weather}')

