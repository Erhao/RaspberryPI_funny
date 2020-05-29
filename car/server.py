from flask import Flask
from flask import request

import RPi.GPIO as GPIO
import time

app = Flask(__name__)

@app.after_request
def af_request(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp

@app.route('/hello_car', methods=['GET'])
def hello_car():
    GPIO.output(fl1, 1)
    GPIO.output(fr1, 1)
    GPIO.output(bl1, 1)
    GPIO.output(br1, 1)
    time.sleep(1)

def reset():
    for pin in pins:
        GPIO.output(pin, 0)

@app.route('/stop', methods=['GET'])
def stop():
    reset()

@app.route('/turn_left_ahead', methods=['GET'])
def turn_left_ahead():
    reset()
    GPIO.output(fr1, 1)
    GPIO.output(br1, 1)

@app.route('/turn_right_ahead', methods=['GET'])
def turn_right_ahead():
    reset()
    GPIO.output(fl1, 1)
    GPIO.output(bl1, 1)

@app.route('/turn_left_back', methods=['GET'])
def turn_left_back():
    reset()
    GPIO.output(fr2, 1)
    GPIO.output(br2, 1)

@app.route('/turn_right_back', methods=['GET'])
def turn_right_back():
    reset()
    GPIO.output(fl2, 1)
    GPIO.output(bl2, 1)

@app.route('/turn_left_in_suit', methods=['GET'])
def turn_left_in_suit():
    reset()
    GPIO.output(fr1, 1)
    GPIO.output(br1, 1)
    GPIO.output(fl2, 1)
    GPIO.output(bl2, 1)

@app.route('/turn_right_in_suit', methods=['GET'])
def turn_right_in_suit():
    reset()
    GPIO.output(fr2, 1)
    GPIO.output(br2, 1)
    GPIO.output(fl1, 1)
    GPIO.output(bl1, 1)

@app.route('/go', methods=['GET'])
def go():
    reset()
    GPIO.output(fl1, 1)
    GPIO.output(fr1, 1)
    GPIO.output(bl1, 1)
    GPIO.output(br1, 1)

@app.route('/back', methods=['GET'])
def back():
    reset()
    GPIO.output(fl2, 1)
    GPIO.output(fr2, 1)
    GPIO.output(bl2, 1)
    GPIO.output(br2, 1)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    fl1 = 36
    fl2 = 38
    fr1 = 16
    fr2 = 18
    bl1 = 37
    bl2 = 35
    br1 = 13
    br2 = 11

    pins = [fl1, fl2, fr1, fr2, bl1, bl2, br1, br2]

    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

    app.run()
