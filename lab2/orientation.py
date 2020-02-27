import math
import time

LSERVO = 0
RSERVO = 1


class Orientation:
    def __init__(self, encoder, motorControl):
        self.encoder = encoder
        self.motorControl = motorControl

    def rotateDegrees(self):
        self.encoder.resetCounts()
        degreesAndSeconds = self.getDegreesAndSecondsFromUser()
        degrees = float(degreesAndSeconds[0])
        seconds = float(degreesAndSeconds[1])

        radians = self.convertDegreesToRadians(degrees)

        distanceToTravel = self.getDistanceToTravelFromRadians(radians)

        while not self.checkIfDegreesAndSecondsCombinationIsFeasible(distanceToTravel, seconds):
            degreesAndSeconds = self.getDegreesAndSecondsFromUser()
            degrees = float(degreesAndSeconds[0])
            seconds = float(degreesAndSeconds[1])
            distanceToTravel = self.getDistanceToTravelFromRadians(degrees)

        # self.motorControl.setSpeedsVW(0, 1)
        # self.motorControl.setSpeedsIPS(
        #     (distanceToTravel/seconds), -(distanceToTravel/seconds))

        self.motorControl.setSpeedsVW(0, radians / seconds)

        while not self.traveledDesiredDistance(self.encoder.getCounts(), distanceToTravel):
            pass

        self.motorControl.setSpeedsPWM(0, 0)

    def rotateDegreesAtMaxSpeed(self, degrees):
        self.encoder.resetCounts()
        radians = self.convertDegreesToRadians(degrees)
        distanceToTravel = self.getDistanceToTravelFromRadians(radians)
        self.motorControl.setSpeedsIPS(
            self.encoder.MAX_IPS, -1 * self.encoder.MAX_IPS)

        while not self.traveledDesiredDistance(self.encoder.getCounts(), distanceToTravel):
            # time.sleep(0.1)
            pass

        self.motorControl.setSpeedsPWM(0, 0)

    def getDegreesAndSecondsFromUser(self):
        degrees = input("Degrees to rotate: ")
        seconds = input("Seconds: ")
        return (degrees, seconds)

    def checkIfDegreesAndSecondsCombinationIsFeasible(self, distanceToTravel, seconds):
        ips = distanceToTravel / seconds
        if ips > self.encoder.MAX_IPS:
            print("The degrees/seconds combination is not feasible.")
            return False
        return True

    def getDistanceToTravelFromRadians(self, radians):
        return self.encoder.ROBOT_CIRCUMFERENCE / (360 / (radians / (math.pi / 180)))

    def traveledDesiredDistance(self, tickCounts, desiredDistanceInInches):
        lWheelDistance = tickCounts[LSERVO] / \
            32 * self.encoder.WHEEL_CIRCUMFERENCE
        rWheelDistance = tickCounts[RSERVO] / \
            32 * self.encoder.WHEEL_CIRCUMFERENCE

        if lWheelDistance > desiredDistanceInInches or rWheelDistance > desiredDistanceInInches:
            return True

        return False

    def convertDegreesToRadians(self, degrees):
        return degrees * (math.pi / 180)
