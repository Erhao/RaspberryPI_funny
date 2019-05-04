import RPi.GPIO as GPIO
import time

PIN_FAN = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_FAN, GPIO.OUT)

# get cpu temperature
def cpu_temp():
	with open("/sys/class/thermal/thermal_zone0/temp", 'r') as f:
		cpu_temperature = int(int(f.read()) / 1000)
	return cpu_temperature

delay = 3
is_close = True
try:
	while True:
		cpu_temperature = cpu_temp()
		if is_close:
			if cpu_temperature > 38:
				GPIO.output(PIN_FAN, GPIO.HIGH)
				is_close = False
		else:
			if cpu_temperature <= 36:
				GPIO.output(PIN_FAN, GPIO.LOW)
				is_close = True
		print(cpu_temperature, ' -- ', time.ctime())
		time.sleep(delay)
except KeyboardInterrupt:
	print('STOP BY USER')
	GPIO.cleanup()
