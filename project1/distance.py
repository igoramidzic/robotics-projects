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


def ctrlC(signum, frame):
    # Clean up servos
    motorControl.cleanup()

    # Clean up encoders
    encoder.cleanup()

    print("Exiting")
    exit()


def traveledDesiredDistance(tickCounts, desiredDistanceInInches):
    lWheelDistance = tickCounts[LSERVO] / 32 * WHEEL_CIRCUMFERENCE
    rWheelDistance = tickCounts[RSERVO] / 32 * WHEEL_CIRCUMFERENCE

    if lWheelDistance > desiredDistanceInInches and rWheelDistance > desiredDistanceInInches:
        return True

    return False


# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)

# Collect arguments from user
inches = float(sys.argv[1])
seconds = float(sys.argv[2])

IPS = inches/seconds

# Check if distance/speed combination is feasible
if IPS > MAX_IPS:
    print("The distance/seconds combination is not feasible.")
    exit()

encoder = Encoder()
encoder.initEncoders()

motorControl = MotorControl(encoder)

with open('calibratedSpeeds.json') as json_file:
    motorControl.speedMap = json.load(json_file)

motorControl.setSpeedsIPS(IPS, IPS)

# Print speeds for ~10 seconds
for i in range(333):
    timer = time.monotonic()
    while time.monotonic() - timer < 0.03:
        pass

    if traveledDesiredDistance(encoder.getCounts(), inches):
        motorControl.setSpeedsPWM(0, 0)

    print(encoder.getSpeeds())

while not traveledDesiredDistance(encoder.getCounts(), inches):
    pass

motorControl.setSpeedsPWM(0, 0)
