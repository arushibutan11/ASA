from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
def mess():
	lcd = Adafruit_CharLCD()
	lcd.begin(16, 2)
	lcd.clear()
	lcd.message("I am Lost. Contact 9986521450")