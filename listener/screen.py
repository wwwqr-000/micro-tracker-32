from machine import I2C, Pin
import ssd1306

i2c = I2C(0, scl=Pin(26), sda=Pin(25))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def cls(): oled.fill(0)
def drawPixel(x, y, stat): oled.pixel(x, y, stat)
def drawTxt(txt, x, y): oled.text(txt, x, y)
def refresh(): oled.show()
