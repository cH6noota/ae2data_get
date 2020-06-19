import wiringpi as w
import time
w.wiringPiSetup()
w.pinMode(0, 0)
w.pinMode(1, 1)
 
while 1:
    switch = w.digitalRead(0)
    print(switch)
    time.sleep(1)
