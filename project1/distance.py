import math
import time

LSERVO = 0
RSERVO = 1

WHEEL_DIAMETER = 2.61
WHEEL_CIRCUMFERENCE = math.pi * WHEEL_DIAMETER
MAX_RPS = 0.8
MAX_IPS = MAX_RPS * WHEEL_CIRCUMFERENCE


class Distance:
    def __init__(self, encoder, motorControl):
        self.encoder = encoder
        self.motorControl = motorControl

    def moveDistanceInSeconds(self):
        self.encoder.resetCounts()
        inchesAndSeconds = self.getInchesAndSecondsFromUser()
        inches = float(inchesAndSeconds[0])
        seconds = float(inchesAndSeconds[1])
        ips = self.getIPS(inches, seconds)

        while not self.checkIfDistanceAndSecondsCombinationIsFeasible(ips):
            inchesAndSeconds = self.getInchesAndSecondsFromUser()
            inches = float(inchesAndSeconds[0])
            seconds = float(inchesAndSeconds[1])
            ips = self.getIPS(inches, seconds)

        self.motorControl.setSpeedsIPS(ips, ips)

        # Print speeds for ~10 seconds
        for i in range(333):
            timer = time.monotonic()
            while time.monotonic() - timer < 0.03:
                pass

            if self.traveledDesiredDistance(self.encoder.getCounts(), inches):
                self.motorControl.setSpeedsPWM(0, 0)

            print(self.encoder.getSpeeds())

        while not self.traveledDesiredDistance(self.encoder.getCounts(), inches):
            pass

        print("helllo")

        self.motorControl.setSpeedsPWM(0, 0)

    def traveledDesiredDistance(self, tickCounts, desiredDistanceInInches):
        lWheelDistance = tickCounts[LSERVO] / 32 * WHEEL_CIRCUMFERENCE
        rWheelDistance = tickCounts[RSERVO] / 32 * WHEEL_CIRCUMFERENCE

        if lWheelDistance > abs(desiredDistanceInInches) and rWheelDistance > abs(desiredDistanceInInches):
            return True

        return False

    def traveledDesiredDistance(self, tickCounts, desiredDistanceInInches):
        lWheelDistance = tickCounts[LSERVO] / 32 * WHEEL_CIRCUMFERENCE
        rWheelDistance = tickCounts[RSERVO] / 32 * WHEEL_CIRCUMFERENCE

        if lWheelDistance > abs(desiredDistanceInInches) and rWheelDistance > abs(desiredDistanceInInches):
            return True

        return False

    def checkIfDistanceAndSecondsCombinationIsFeasible(self, ips):
        if abs(ips) > MAX_IPS:
            print("The distance/seconds combination is not feasible.")
            return False
        return True

    def getInchesAndSecondsFromUser(self):
        # Collect arguments from user
        inches = input("Distance in inches: ")
        seconds = input("Seconds: ")

        return (inches, seconds)

    def getIPS(self, inches, seconds):
        return float(inches) / float(seconds)
