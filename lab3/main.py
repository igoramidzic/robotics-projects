import signal
import json
import time
import math
from encoders import Encoder
from motorControl import MotorControl
from orientation import Orientation
from tof import TOF
from pid_control import PID
from ThreadedWebcam import ThreadedWebcam
from UnthreadedWebcam import UnthreadedWebcam
import testCamera
import faceGoal as task1
import motionToGoal as task2

# This function is called when Ctrl+C is pressed.
# It's intended for properly exiting the program.


def ctrlC(signum, frame):
    # Clean up servos
    motorControl.cleanup()

    # Clean up encoders
    encoder.cleanup()

    # Clean up distance sensors
    tof.cleanup()

    # Clean up camera
    camera.stop()

    print("Exiting")
    exit()


# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)

# Setup encoder
encoder = Encoder()
encoder.initEncoders()

# Setup motor control
motorControl = MotorControl(encoder)

orientation = Orientation(encoder, motorControl)

tof = TOF()

camera = UnthreadedWebcam()

try:
    with open('calibratedSpeeds.json') as json_file:
        motorControl.speedMap = json.load(json_file)

except IOError:
    input("You must calibrate speeds first. Press enter to continue")
    motorControl.calibrateSpeeds()

while True:
    print("\n(1) Calibrate speeds")
    print("\n(2) Test Camera")
    print("\n(3) Task 1: Goal Facing")
    print("\n(4) Task 2: Motion To Goal")
    taskOption = int(input("Which action you do you want perform? (1 - 4): "))

    if taskOption == 1:
        motorControl.calibrateSpeeds()
    if taskOption == 2:
        testCamera.testCamera(camera)
    if taskOption == 3:
        task1.run(motorControl, camera)
    if taskOption == 4:
        task2.run(motorControl, tof, camera)
