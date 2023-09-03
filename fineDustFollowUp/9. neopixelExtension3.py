# chatGPT 링크: https://chat.openai.com/share/ee53f767-f887-4d6c-ab87-dd897e94a93e

import time
from neopixel import Neopixel
import math

# 네오픽셀의 셀 갯수, PIO상태, 핀번호 정의 
numpix = 4
PIO = 0
Pin = 22

# 네오픽셀이 RGB타입일 때 네오픽셀 수, PIO상태, 핀번호, 네오픽셀 타입 순으로 선택, 밝기 지정 
strip = Neopixel(numpix, PIO, Pin, "RGB")

# 밝기 설정(0~255)
strip.brightness(150)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(numpix):
            rc_index = (i * 256 // numpix) + j
            strip.set_pixel(i, wheel(rc_index & 255))
        strip.show()
        time.sleep(wait)

while True:
    rainbow_cycle(0.01)
