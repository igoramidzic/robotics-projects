import math
import time

LSERVO = 0
RSERVO = 1


class Circle:
    def __init__(self, encoder, motorControl, orientation):
        self.encoder = encoder
        self.motorControl = motorControl
        self.orientation = orientation

    def traverseCircle(self):
        self.encoder.resetCounts()
        radiusAndSeconds = self.getRadiusAndSecondsFromUser()
        radius = float(radiusAndSeconds[0])
        seconds = float(radiusAndSeconds[1])

        semiCircleDistanceToTravel = math.pi * radius
        print("Distance to travel:", semiCircleDistanceToTravel)
        v = semiCircleDistanceToTravel / seconds
        w = math.pi / seconds

        while not self.checkIfDistanceAndSecondsCombinationIsFeasible(semiCircleDistanceToTravel, seconds):
            radiusAndSeconds = self.getRadiusAndSecondsFromUser()
            radius = float(radiusAndSeconds[0])
            seconds = float(radiusAndSeconds[1])

        print("V:", v, "W:", w)

        self.motorControl.setSpeedsVW(v, -w)
        timer = time.monotonic()
        while time.monotonic() < timer + seconds:
            pass

        self.motorControl.setSpeedsPWM(0, 0)

        input("Press enter to travel backwards...")

        self.orientation.rotateDegreesAtMaxSpeed(180)

        self.motorControl.setSpeedsVW(v, w)
        timer = time.monotonic()
        while time.monotonic() < timer + seconds:
            pass

        self.motorControl.setSpeedsPWM(0, 0)

    def getRadiusAndSecondsFromUser(self):
        # Collect arguments from user
        radius = input("Radius: ")
        seconds = input("Seconds: ")

        return (radius, seconds)

    def checkIfDistanceAndSecondsCombinationIsFeasible(self, distanceToTravel, seconds):
        if (distanceToTravel / seconds) > self.encoder.MAX_IPS:
            print("The radius/seconds combination is not feasible.")
            return False
        return True

    def travelSemiCircle(self, v, w, semiCircleDistanceToTravel):
        pass
