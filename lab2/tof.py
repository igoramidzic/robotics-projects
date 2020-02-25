# This program demonstrates the usage of the time of flight sensors.
# After running the program, move your hand in front of each sensor to verify that it's working.
# See https://learn.adafruit.com/adafruit-vl53l0x-micro-lidar-distance-sensor-breakout/overview for more details.

import time
import sys
sys.path.append('/home/pi/VL53L0X_rasp_python/python')
import VL53L0X
import RPi.GPIO as GPIO
import constants

# # Pins that the sensors are connected to
LSHDN = 27
FSHDN = 22
RSHDN = 23

DEFAULTADDR = 0x29  # All sensors use this address by default, don't change this
LADDR = 0x2a
RADDR = 0x2b

MMINCH = 0.03937008


class TOF:
    def __init__(self):
        # Set the pin numbering scheme to the numbering shown on the robot itself.
        GPIO.setmode(GPIO.BCM)

        # Setup pins
        GPIO.setup(LSHDN, GPIO.OUT)
        GPIO.setup(FSHDN, GPIO.OUT)
        GPIO.setup(RSHDN, GPIO.OUT)

        # Shutdown all sensors
        GPIO.output(LSHDN, GPIO.LOW)
        GPIO.output(FSHDN, GPIO.LOW)
        GPIO.output(RSHDN, GPIO.LOW)

        time.sleep(0.01)

        # Initialize all sensors
        self.lSensor = VL53L0X.VL53L0X(address=LADDR)
        self.fSensor = VL53L0X.VL53L0X(address=DEFAULTADDR)
        self.rSensor = VL53L0X.VL53L0X(address=RADDR)

        # Connect the left sensor and start measurement
        GPIO.output(LSHDN, GPIO.HIGH)
        time.sleep(0.01)
        self.lSensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)

        # Connect the right sensor and start measurement
        GPIO.output(RSHDN, GPIO.HIGH)
        time.sleep(0.01)
        self.rSensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)

        # Connect the front sensor and start measurement
        GPIO.output(FSHDN, GPIO.HIGH)
        time.sleep(0.01)
        self.fSensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)

    def cleanup(self):
        print("Cleaning up distance sensors")
        GPIO.cleanup()

        # Stop measurement for all sensors
        self.lSensor.stop_ranging()
        self.fSensor.stop_ranging()
        self.rSensor.stop_ranging()

    def getLeftDistance(self):
        return self.getInchesFromMM(self.lSensor.get_distance())

    def getFrontDistance(self):
        return self.getInchesFromMM(self.fSensor.get_distance())

    def getRightDistance(self):
        return self.getInchesFromMM(self.rSensor.get_distance())

    def testDistanceSensors(self):
        for i in range(1, 100):
            self.printDistances()

    def printDistances(self):
        # Get a measurement from each sensor
        lDistance = self.getLeftDistance()
        fDistance = self.getFrontDistance()
        rDistance = self.getRightDistance()

        # Print each measurement
        print("Left: {}\tFront: {}\tRight: {}".format(
            lDistance, fDistance, rDistance))

    def getInchesFromMM(self, mm):
        return mm * MMINCH

    def getMMFromInches(self, inches):
        return inches / MMINCH
