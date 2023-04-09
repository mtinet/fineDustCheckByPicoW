# fineDustCheckByPicoW

## 강의 자료  
[https://han.gl/sChAvb](https://han.gl/sChAvb)  

## Air Polution Index   
* Pico W를 활용해 Open Wether Map에서 받아온 공기 오염도의 공기질 인덱스에 따라 네오픽셀이 제어되도록 하는 코드  
* 네오픽셀을 사용하므로 neopixel.py 파일이 같은 폴더에 있어야 함  
* 시간 정보를 표시할 때는 timezoneChange.py 파일이 같은 폴더에 있어야 함  

## 파일 설명  
* autoFineDustCheckByPicoW.py: 자동으로 5초마다 지정해 놓은 지역 정보를 확인  
* base.py: 기초 코드  
* buttonFineDustCheckByPicoW.py: 버튼을 누르면 지역이 바뀌는 코드  
* main.py: 버튼 코드에 OLED 추가  
* neopixel.py: 네오픽셀 라이브러리  
* timezoneChange.py: 시간정보용 라이브러리  

## 회로도  
<table>
  <thead>
    <tr>
      <th>회로도</th>
      <th>pico W</th>
      <th>neopixel</th>
      <th>OLED</th>
      <th>button</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="8"><img src="https://user-images.githubusercontent.com/13882302/230762399-2a194240-cd07-4ee1-a5f5-311f8c8b714e.png" width="300"></td>
    </tr>
    <tr>
      <td style="text-align: center;">GPIO 16</td>
      <td></td>
      <td>SDA</td>
      <td></td>
    </tr>
    <tr>
      <td style="text-align: center;">GPIO 17</td>
      <td></td>
      <td>SCL</td>
      <td></td>
    </tr>
    <tr>
      <td style="text-align: center;">GPIO 21</td>
      <td></td>
      <td></td>
      <td>Sig</td>
    </tr>
    <tr>
      <td style="text-align: center;">GPIO 22</td>
      <td>IN</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td style="text-align: center;">VBUS</td>
      <td>VCC</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td style="text-align: center;">3.3V</td>
      <td></td>
      <td>VCC</td>
      <td></td>
    </tr>
    <tr style="text-align: center;">
      <td style="text-align: center;">GND</td>
      <td style="text-align: center;">GND</td>
      <td style="text-align: center;">GND</td>
      <td style="text-align: center;">GND</td>
    </tr>
  </tbody>
</table>


## 재료  
<table>
  <thead>
    <tr>
      <th>
        <a href="https://www.devicemart.co.kr/goods/view?no=14575953&gclid=Cj0KCQjw_r6hBhDdARIsAMIDhV-v3VZrlmb37R6pssNcH_zarbtBYylBcQEg87EjIj7Ci5817f7wSjMaAiILEALw_wcB">라즈베리파이 피코 W</a>
      </th>
      <th>
        <a href="https://ko.aliexpress.com/item/32645620129.html?gatewayAdapt=glo2kor">네오픽셀 WS2812B-4 5V 5050 RGB LED</a>
      </th>
      <th>
        <a href="https://robotscience.kr/goods/view?no=16073">OLED 1306</a>
      </th>
      <th>
        <a href="http://m.vctec.co.kr/product/%EB%8C%80%ED%98%95-%EB%B0%98%EA%B5%AC%ED%98%95-%ED%91%B8%EC%89%AC-%EB%B2%84%ED%8A%BC-%EC%8A%A4%EC%9C%84%EC%B9%98-%EB%B9%A8%EA%B0%95-led-%EB%82%B4%EC%9E%A5-12v-big-dome-push-button-red/17139/">푸시 버튼 </a>
      </th>
       <th>
        <a href="https://eduino.kr/product/detail.html?product_no=102&gclid=Cj0KCQjwxMmhBhDJARIsANFGOSsNqpma6XJuq8dfpX22MHuRTblxT6HzfVXb519ahmjo9ek3wxoWFHMaAoSTEALw_wcB">점퍼 와이어 </a>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <img src="https://user-images.githubusercontent.com/13882302/230707541-13ac0fa9-da58-4920-aa5e-0cc93dffff38.png" style="display: block; margin: 0 auto;">
      </td>
      <td>
        <img src="https://user-images.githubusercontent.com/13882302/230707501-7a17d3d6-bcad-4253-9b4d-25588d5b8f93.png" style="display: block; margin: 0 auto;">
      </td>
      <td>
        <img src="https://user-images.githubusercontent.com/13882302/230763376-d09c12a6-c16e-4d10-9f3c-6937890cfcd1.png" style="display: block; margin: 0 auto;">
      </td>
      <td>
        <img src="https://user-images.githubusercontent.com/13882302/230763453-ee7ae557-9e13-4e44-bdfa-909b2fea1851.png" style="display: block; margin: 0 auto;">
      </td>
      <td>
        <img src="https://user-images.githubusercontent.com/13882302/230707618-cb20c432-5363-4cde-9287-bc0e29b64265.png" style="display: block; margin: 0 auto;">
      </td>
    </tr>
  </tbody>
</table>


## 베이스 소스코드  
```python 
# base.py
# This code was written by Juhyun Kim.

import time
from neopixel import Neopixel
import network
import urequests 
from timezoneChange import timeOfSeoul # timezoneChange.py 파일이 같은 폴더에 있어야 동작함 

# 자기 정보 넣기(Open Wether Map API Key, 측정하고자 하는 곳의 위도, 경도 정보, 자신이 사용하는 WiFi정보) 
# https://openweathermap.org/appid 에서 로그인 하고 https://home.openweathermap.org/api_keys 로 이동해서 API Key를 발급받음
API_KEY = '24109ddecb29a5405afe2a8df42c5e34'

# 확인하고 싶은 자신의 GPS 정보
# 서울시청(37.566, 126.9784), 샌프란시스코(37.77493, -122.41942), 세비야(37.38283, -5.97317)
LATITUDE = '37.566'
LONGITUDE = '126.9784'

# 와이파이 정보 
SSID = 'U+Net454C'
password = 'DDAE014478'


# 네오픽셀의 셀 갯수, PIO상태, 핀번호 정의 
numpix = 4
PIO = 0
Pin = 22

# 네오픽셀이 RGB타입일 때 네오픽셀 수, PIO상태, 핀번호, 네오픽셀 타입 순으로 선택, 밝기 지정 
strip = Neopixel(numpix, PIO, Pin, "RGB")

# 밝기 설정(0~255)
strip.brightness(150)

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

while True:
    # 시간정보 가져오기
    updatedTime = timeOfSeoul()
    # print(type(updatedTime))
    print(updatedTime)
    
    try:
        air_quality_index = get_air_quality_index(LATITUDE, LONGITUDE, API_KEY)
        set_neopixel_color(air_quality_index)
    except Exception as e:
        print("Error:", e)
        color = (0, 0, 0)  # Black
        strip.show()

    time.sleep(60 * 15)  # 매 15분마다 업데이트 

```

