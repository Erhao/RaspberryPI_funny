import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
in_pin = 3 # touch detect
out_pin = 7 # trigger
GPIO.setup(in_pin, GPIO.IN)
GPIO.setup(out_pin, GPIO.OUT)

try:
    while True:
        in_val = GPIO.input(in_pin)
        if in_val == True:
            GPIO.output(out_pin, True)
            time.sleep(35)
            GPIO.output(out_pin, False)
        if in_val == False:
            time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print('--------Exit---------')
