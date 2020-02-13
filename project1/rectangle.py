import math
import time

LSERVO = 0
RSERVO = 1

ROTATION_TIME_IN_SECONDS = 0.6


class Rectangle:
    def __init__(self, encoder, motorControl, orientation):
        self.encoder = encoder
        self.motorControl = motorControl
        self.orientation = orientation

    def travelRectangle(self):
        self.encoder.resetCounts()
        heightWidthSeconds = self.getHeightWidthAndSecondsFromUser()
        H = float(heightWidthSeconds[0])
        W = float(heightWidthSeconds[1])
        seconds = float(heightWidthSeconds[2])

        ips = self.getPerimeter(H, W)/(seconds - 3 * ROTATION_TIME_IN_SECONDS)

        while not self.checkIfDistanceAndSecondsCombinationIsFeasible(ips):
            heightWidthSeconds = self.getHeightWidthAndSecondsFromUser()
            H = float(heightWidthSeconds[0])
            W = float(heightWidthSeconds[1])
            seconds = float(heightWidthSeconds[2])
            ips = self.getPerimeter(
                H, W)/(seconds - 3 * ROTATION_TIME_IN_SECONDS)

        # Pattern to move in rectangle
        self.moveForwardForDistance(H, ips)
        self.orientation.rotateDegreesAtMaxSpeed(90)
        self.moveForwardForDistance(W, ips)
        self.orientation.rotateDegreesAtMaxSpeed(90)
        self.moveForwardForDistance(H, ips)
        self.orientation.rotateDegreesAtMaxSpeed(90)
        self.moveForwardForDistance(W, ips)
        self.orientation.rotateDegreesAtMaxSpeed(90)

        self.motorControl.setSpeedsPWM(0, 0)

    def traveledDesiredDistance(self, tickCounts, desiredDistanceInInches):
        lWheelDistance = tickCounts[LSERVO] / \
            32 * self.encoder.WHEEL_CIRCUMFERENCE
        rWheelDistance = tickCounts[RSERVO] / \
            32 * self.encoder.WHEEL_CIRCUMFERENCE

        if lWheelDistance > desiredDistanceInInches and rWheelDistance > desiredDistanceInInches:
            return True

        return False

    def getHeightWidthAndSecondsFromUser(self):
        # Collect arguments from user
        h = input("Height: ")
        w = input("Width: ")
        seconds = input("Seconds: ")

        return (h, w, seconds)

    def getIPS(self, inches, seconds):
        return float(inches) / float(seconds)

    def getPerimeter(self, H, W):
        return 2 * H + 2 * W

    def checkIfDistanceAndSecondsCombinationIsFeasible(self, ips):
        if abs(ips) > self.encoder.MAX_IPS:
            print("The height/width/seconds combination is not feasible.")
            return False
        return True

    def moveForwardForDistance(self, distance, ips):
        self.encoder.resetCounts()
        self.motorControl.setSpeedsIPS(ips, ips)
        while not self.traveledDesiredDistance(self.encoder.getCounts(), distance):
            pass

    def rotateRight(self):
        self.motorControl.setSpeedsPWM(1.7, 1.3)
        timer = time.monotonic()
        while time.monotonic() - timer < ROTATION_TIME_IN_SECONDS:
            pass
