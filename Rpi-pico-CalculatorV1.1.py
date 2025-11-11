#https://github.com/SAMSBSIREX/Rpi-pico-Calculator
#Rpi-pico-Calculato
#V1.1 (1px frame)

#Monitor >>> Rpi Pico
#GND >>> 38 GND
#VCC >>> 36 3V3(OUT)
#SCK >>> 7  GP4
#SDA >>> 6  GP5

#Keypad 4x4 Matrix >>> Rpi Pico
#R1 >>> 14 GP10
#R2 >>> 15 GP11
#R3 >>> 16 GP12
#R4 >>> 17 GP13
#C1 >>> 27 GP21
#C2 >>> 26 GP20
#C3 >>> 25 GP19
#C4 >>> 24 GP18

from machine import Pin, I2C
import OLED
import utime

i2c = I2C(0, scl=Pin(5), sda=Pin(4))
oled = OLED.SSD1306_I2C(128, 32, i2c)

matrix_keys = [['1','2','3','A'],
               ['4','5','6','B'],
               ['7','8','9','C'],
               ['*','0','#','D']]

rows = [10,11,12,13]
cols = [21,20,19,18]

row_pins = [Pin(r, Pin.OUT) for r in rows]
col_pins = [Pin(c, Pin.IN, Pin.PULL_DOWN) for c in cols]

oled.fill(0)
oled.text("@SAMSBSIREX",5,6)
oled.text("Press any Key",5,18)
oled.show()
utime.sleep(0.5)

def scankeys():
    for i, row in enumerate(row_pins):
        row.high()
        for j, col in enumerate(col_pins):
            if col.value():
                key = matrix_keys[i][j]
                utime.sleep(0.3)
                row.low()
                return key
        row.low()
    return None

def aniton():
    for x in range(0,128):
        oled.pixel(x, 0, 1)
    for y in range(0,32):
        oled.pixel(127, y, 1)
    for x in range(127 ,0 ,-1):
        oled.pixel(x, 31, 1)
    for y in range(31, 0, -1):
        oled.pixel(0, y, 1)
    oled.show()

expr = ""

while True:
    aniton()
    key = scankeys()
    if key:
        if key == "*":
            expr = ""
        elif key == "#":
            try:
                result = str(eval(expr))
                expr = result
            except:
                expr = "Error"
        elif key in "ABCD":
            if key == "A": expr += "+"
            if key == "B": expr += "-"
            if key == "C": expr += "*"
            if key == "D": expr += "/"
        else:
            expr += key

        oled.fill(0)
        oled.text(expr, 5, 13)
        oled.show()
