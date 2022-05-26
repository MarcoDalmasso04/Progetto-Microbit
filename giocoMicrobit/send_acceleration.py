import time
from microbit import *
import time
while True:
    a = accelerometer.get_values()
    print(a)
    time.sleep(1)
    