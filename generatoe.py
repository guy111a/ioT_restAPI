import time
import board
from adafruit_htu21d import HTU21D
import requests

i2c = board.I2C()
sensor = HTU21D(i2c)

time.sleep(1)
URL = f'http://10.0.0.21:1234temperature?key=*******&key2=magadan&act=write&temp={sensor.temperature}&humid={sensor.relative_humidity}&timeStamp={float(str(time.time()))}'
r = requests.get(url = URL)
