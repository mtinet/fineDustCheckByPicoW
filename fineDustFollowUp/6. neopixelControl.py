# chatGPT 링크: https://chat.openai.com/share/ee53f767-f887-4d6c-ab87-dd897e94a93e

import time
from neopixel import Neopixel

# 네오픽셀의 셀 갯수, PIO상태, 핀번호 정의 
numpix = 4
PIO = 0
Pin = 22

# 네오픽셀이 RGB타입일 때 네오픽셀 수, PIO상태, 핀번호, 네오픽셀 타입 순으로 선택, 밝기 지정 
strip = Neopixel(numpix, PIO, Pin, "RGB")

# 밝기 설정(0~255)
strip.brightness(150)

def light():
    for i in range(numpix):
        strip.set_pixel(i, color)
        time.sleep(0.01)
        strip.show()
        
# Green, Red, Blue의 순서로 되어 있음
color = (0, 0, 255)  # Blue
light()
time.sleep(1)

color = (255, 0, 0)  # Green
light()
time.sleep(1)

color = (255, 255, 0)  # Yellow
light()
time.sleep(1)

color = (100, 255, 0)  # Orange
light()
time.sleep(1)

color = (0, 255, 0)  # Red
light()
time.sleep(1)

color = (0, 128, 128)  # Purple (unknown)
light()
time.sleep(1)