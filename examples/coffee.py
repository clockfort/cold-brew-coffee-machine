#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
import sys

mh = Adafruit_MotorHAT(addr=0x60)

def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

m1 = mh.getMotor(1)
m2 = mh.getMotor(2)

def logPrint(message):
	print "(" + str(time.time()) + ") " + message

def jogMotors(dutyCycle, timePeriod):
        m1.run(Adafruit_MotorHAT.RELEASE)
        m1.run(Adafruit_MotorHAT.FORWARD)
        m1.setSpeed(dutyCycle)
        m2.run(Adafruit_MotorHAT.RELEASE)
        m2.run(Adafruit_MotorHAT.FORWARD)
        m2.setSpeed(dutyCycle)
        time.sleep(timePeriod)
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)

def dispense(flowRate, totalFlow):
	startTime = time.time()
	currentTime = time.time()

	# the motors tend to stall at lower duty cycles than this, so we're doing a very macroscale multi-second "duty cycle"
	onPeriodSeconds = 1.5
	dutyCycle = 110 # /255
	flowRateAtDutyCycle = 0.3125 # mL/sec, measured experimentally
	offPeriodSeconds = flowRateAtDutyCycle * onPeriodSeconds / flowRate - onPeriodSeconds
	totalTimeSeconds = totalFlow / flowRate
	logPrint("offPeriodSeconds = " + str(offPeriodSeconds))

	while ((currentTime - startTime) < totalTimeSeconds):
		currentTime = time.time()
		elapsedTime = (currentTime - startTime)
		percentComplete = elapsedTime / totalTimeSeconds * 100;
		logPrint("Starting dispense cycle. Coffee is " + str(percentComplete) + "% complete")
		logPrint("~" + str(elapsedTime / totalTimeSeconds * totalFlow) + "mL dispensed so far.")
		jogMotors(dutyCycle, onPeriodSeconds)
		time.sleep(offPeriodSeconds)
	logPrint("Coffee complete.")


# (0.5 US gallon / 6 hours) in mL/sec , 0.5 US gallon in mL
dispense(0.0876252728, 1892.71)
