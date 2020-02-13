# This program demonstrates usage of the servos.
# Keep the robot in a safe location before running this program,
# as it will immediately begin moving.
# See https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/ for more details.

import signal
import json
import time
import math
from encoders import Encoder
from motorControl import MotorControl
from distance import Distance
from orientation import Orientation
from rectangle import Rectangle
from circle import Circle

# This function is called when Ctrl+C is pressed.
# It's intended for properly exiting the program.


def ctrlC(signum, frame):
    # Clean up servos
    motorControl.cleanup()

    # Clean up encoders
    encoder.cleanup()

    print("Exiting")
    exit()


# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)

# Setup encoder
encoder = Encoder()
encoder.initEncoders()

# Setup motor control
motorControl = MotorControl(encoder)

try:
    with open('calibratedSpeeds.json') as json_file:
        motorControl.speedMap = json.load(json_file)

except IOError:
    input("You must calibrate speeds first. Press enter to continue")
    motorControl.calibrateSpeeds()

while True:
    print("\n(1) Calibrate speeds")
    print("(2) Distance")
    print("(3) Orientation")
    print("(4) Rectangle")
    print("(5) Circle")
    taskOption = int(input("Which task you do you want run? (1 - 5): "))

    if taskOption == 1:
        motorControl.calibrateSpeeds()
    elif taskOption == 2:
        distance = Distance(encoder, motorControl)
        distance.moveDistanceInSeconds()
    elif taskOption == 3:
        orientation = Orientation(encoder, motorControl)
        orientation.rotateDegrees()
    elif taskOption == 4:
        orientation = Orientation(encoder, motorControl)
        rectangle = Rectangle(encoder, motorControl, orientation)
        rectangle.travelRectangle()
    elif taskOption == 5:
        orientation = Orientation(encoder, motorControl)
        circle = Circle(encoder, motorControl, orientation)
        circle.traverseCircle()
        pass
