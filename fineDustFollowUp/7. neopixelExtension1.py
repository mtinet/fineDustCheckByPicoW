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

colors = [
    (0, 0, 255),      # Blue
    (255, 0, 0),      # Green
    (255, 255, 0),    # Yellow
    (100, 255, 0),    # Orange
    (0, 255, 0),      # Red
    (0, 128, 128)     # Purple (unknown)
]

def rotate_colors():
    while True:
        for color in colors:
            for i in range(numpix):
                strip.set_pixel(i, color)
                strip.show()
                time.sleep(0.5)
                # 다음 픽셀로 색을 이동
                color = (0, 0, 0) if i == numpix - 1 else colors[(colors.index(color) + 1) % len(colors)]
            time.sleep(1)

rotate_colors()
