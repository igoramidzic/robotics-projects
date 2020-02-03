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


def ctrlC(signum, frame):
    # Clean up servos
    motorControl.cleanup()

    # Clean up encoders
    encoder.cleanup()

    print("Exiting")
    exit()


def rotatedDesiredDegrees(tickCounts, desiredDegreesToRotate):
    return False


# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)

# Collect arguments from user
degreesToRotate = float(sys.argv[1])
seconds = float(sys.argv[2])


encoder = Encoder()
encoder.initEncoders()

motorControl = MotorControl(encoder)

with open('calibratedSpeeds.json') as json_file:
    motorControl.speedMap = json.load(json_file)

# motorControl.setSpeedsIPS(IPS, IPS)

# Print speeds for ~10 seconds
for i in range(333):
    timer = time.monotonic()
    while time.monotonic() - timer < 0.03:
        pass

    if rotatedDesiredDegrees(encoder.getCounts(), degreesToRotate):
        motorControl.setSpeedsPWM(0, 0)

    print(encoder.getSpeeds())

# while not rotatedDesiredDegrees(encoder.getCounts(), degreesToRotate):
#     pass

motorControl.setSpeedsPWM(0, 0)
