#!/usr/bin/env python2

import time
import RPi.GPIO as GPIO

def read_sensor():
    """
    Reads the echo sensor and returns a distance value.
    """
    
    # Turn off GPIO warnings 
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
        
    # GPIO output = the pin that's connected to "Trig" on the sensor
    # GPIO input = the pin that's connected to "Echo" on the sensor
    GPIO.setup(24,GPIO.OUT)
    GPIO.setup(25,GPIO.IN)
    GPIO.output(24, GPIO.LOW)
    
    time.sleep(0.3)
    
    # sensor manual says a pulse ength of 10Us will trigger the 
    # sensor to transmit 8 cycles of ultrasonic burst at 40kHz and 
    # wait for the reflected ultrasonic burst to be received
    
    # to get a pulse length of 10Us we need to start the pulse, then
    # wait for 10 microseconds, then stop the pulse. This will 
    # result in the pulse length being 10Us.
    
    # start the pulse on the GPIO pin 
    # change this value to the pin you are using
    # GPIO output = the pin that's connected to "Trig" on the sensor
    GPIO.output(24, True)
    
    # wait 10 micro seconds (0.00001 seconds)
    time.sleep(0.00001)
    
    # stop the pulse after the time above has passed
    # GPIO output = the pin that's connected to "Trig" on the sensor
    GPIO.output(24, False)

    # listen to the input pin. 0 means nothing is happening.
    while GPIO.input(25) == 0:
        signaloff = time.time()
    
    # listen to the input pin. Once a signal is received, record the
    # time the signal came through
    # change this value to the pin you are using
    # GPIO input = the pin that's connected to "Echo" on the sensor
    while GPIO.input(25) == 1:
        signalon = time.time()
    
    timepassed = signalon - signaloff
    
    # convert this distance into centimeters
    distance = timepassed * 17000
    
    # return the distance of an object in front of the sensor in cm
    return distance
    
    # no longer using the GPIO, so tell software we're done
    # GPIO.cleanup() # DANGEROUS MIGHT KILL MOTOR CONTROLLER

if __name__ == '__main__':
    while True:
        time.sleep(0.2)
        dis = round(read_sensor())
        if dis < 25:
            print '\033[1;31m'
        elif dis < 50:
            print '\033[1;33m'
        else:
            print '\033[1;32m'

        print str(round(read_sensor(), 1)) + " cm\033[1;m"
