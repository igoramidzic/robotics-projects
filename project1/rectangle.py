import sys
import math
from encoders import Encoder
from motorControl import MotorControl
import signal
import json
import time

LSERVO = 0
RSERVO = 1

WHEEL_DIAMETER = 2.61
WHEEL_CIRCUMFERENCE = math.pi * WHEEL_DIAMETER
MAX_RPS = 0.8
MAX_IPS = MAX_RPS * WHEEL_CIRCUMFERENCE
ROTATION_TIME_IN_SECONDS = 0.6


def ctrlC(signum, frame):
    # Clean up servos
    motorControl.cleanup()

    # Clean up encoders
    encoder.cleanup()

    print("Exiting")
    exit()


# def rotatedDesiredDegrees(tickCounts, desiredDegreesToRotate):
#     return False


def getPerimeter(H, W):
    return 2 * H + 2 * W


# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)

# Collect arguments from user
H = float(sys.argv[1])
W = float(sys.argv[2])
seconds = float(sys.argv[3])


encoder = Encoder()
encoder.initEncoders()

motorControl = MotorControl(encoder)

with open('calibratedSpeeds.json') as json_file:
    motorControl.speedMap = json.load(json_file)

try:
    IPS = getPerimeter(H, W)/(seconds - 3 * ROTATION_TIME_IN_SECONDS)
    if IPS > MAX_IPS:
        throw()
except:
    print("The distance/seconds combination is not feasible.")
    exit()

print("IPS:", IPS)


def traveledDesiredDistance(tickCounts, desiredDistanceInInches):
    lWheelDistance = tickCounts[LSERVO] / 32 * WHEEL_CIRCUMFERENCE
    rWheelDistance = tickCounts[RSERVO] / 32 * WHEEL_CIRCUMFERENCE

    if lWheelDistance > desiredDistanceInInches and rWheelDistance > desiredDistanceInInches:
        return True

    return False


def moveForwardForDistance(distance):
    motorControl.setSpeedsIPS(IPS, IPS)
    timer = time.monotonic()
    while not traveledDesiredDistance(encoder.getCounts(), distance):
        pass

    encoder.resetCounts()


def rotateRight():
    motorControl.setSpeedsPWM(1.7, 1.3)
    timer = time.monotonic()
    while time.monotonic() - timer < ROTATION_TIME_IN_SECONDS:
        pass


moveForwardForDistance(H)

rotateRight()

moveForwardForDistance(W)

rotateRight()

moveForwardForDistance(H)

rotateRight()

moveForwardForDistance(W)

motorControl.setSpeedsPWM(0, 0)
