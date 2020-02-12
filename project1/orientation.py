import math
import time

LSERVO = 0
RSERVO = 1

WHEEL_DIAMETER = 2.61
WHEEL_CIRCUMFERENCE = math.pi * WHEEL_DIAMETER
DIST_BETWEEN_WHEELS = 4.3
ROBOT_CIRCUMFERENCE = math.pi * DIST_BETWEEN_WHEELS
MAX_RPS = 0.8
MAX_IPS = MAX_RPS * WHEEL_CIRCUMFERENCE


class Orientation:
    def __init__(self, encoder, motorControl):
        self.encoder = encoder
        self.motorControl = motorControl

    def rotateDegrees(self):
        self.encoder.resetCounts()
        degreesAndSeconds = self.getDegreesAndSecondsFromUser()
        degrees = float(degreesAndSeconds[0])
        seconds = float(degreesAndSeconds[1])

        distanceToTravel = self.getDistanceToTravelFromDegrees(degrees)
        print("Distance To Travel: ", distanceToTravel)

        while not self.checkIfDegreesAndSecondsCombinationIsFeasible(distanceToTravel, seconds):
            degreesAndSeconds = self.getDegreesAndSecondsFromUser()
            degrees = float(degreesAndSeconds[0])
            seconds = float(degreesAndSeconds[1])
            distanceToTravel = self.getDistanceToTravelFromDegrees(degrees)

        print(self.getDistanceToTravelFromDegrees(degrees))
        # self.motorControl.setSpeedsVW(0, 1)
        self.motorControl.setSpeedsIPS(
            (distanceToTravel/seconds), -(distanceToTravel/seconds))

        while not self.traveledDesiredDistance(self.encoder.getCounts(), distanceToTravel):
            time.sleep(0.1)
            pass

        self.motorControl.setSpeedsPWM(0, 0)

    def getDegreesAndSecondsFromUser(self):
        degrees = input("Degrees to rotate: ")
        seconds = input("Seconds: ")
        return (degrees, seconds)

    def checkIfDegreesAndSecondsCombinationIsFeasible(self, distanceToTravel, seconds):
        ips = distanceToTravel / seconds
        if ips > MAX_IPS:
            print("The degrees/seconds combination is not feasible.")
            return False
        return True

    def getDistanceToTravelFromDegrees(self, degrees):
        return ROBOT_CIRCUMFERENCE / (360 / degrees)

    def traveledDesiredDistance(self, tickCounts, desiredDistanceInInches):
        lWheelDistance = tickCounts[LSERVO] / 32 * WHEEL_CIRCUMFERENCE
        rWheelDistance = tickCounts[RSERVO] / 32 * WHEEL_CIRCUMFERENCE

        print("Distance traveled:", lWheelDistance, rWheelDistance)

        if lWheelDistance > desiredDistanceInInches and rWheelDistance > desiredDistanceInInches:
            return True

        return False
