import signal
import json
import time
import math
from encoders import Encoder
from motorControl import MotorControl
from orientation import Orientation
from tof import TOF
from pid_control import PID
import task1
import task2
import task3

# This function is called when Ctrl+C is pressed.
# It's intended for properly exiting the program.

chart = {'left': [],
         'front': [],
         'right': []}


def ctrlC(signum, frame):
    jj = json.dumps(chart)
    f = open("task3Chart-square.json", "w")
    f.write(jj)
    f.close()

    # Clean up servos
    motorControl.cleanup()

    # Clean up encoders
    encoder.cleanup()

    # Clean up distance sensors
    tof.cleanup()

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

pid = PID(0.5, -6, 6)

try:
    with open('calibratedSpeeds.json') as json_file:
        motorControl.speedMap = json.load(json_file)

except IOError:
    input("You must calibrate speeds first. Press enter to continue")
    motorControl.calibrateSpeeds()

while True:
    print("\n(1) Calibrate speeds")
    print("(2) Test distance sensors")
    print("(3) Move forward until 12\" from wall")
    print("(4) Follow center between walls")
    print("(5) Follow wall")
    taskOption = int(input("Which task you do you want run? (1 - 5): "))

    if taskOption == 1:
        motorControl.calibrateSpeeds()
    if taskOption == 2:
        tof.testDistanceSensors()
    if taskOption == 3:
        task1.moveForwardUntilCloseToWall(12, motorControl, tof)
    if taskOption == 4:
        task2.followParallelToWalls(motorControl, tof, pid)
    if taskOption == 5:
        task3.followWall(encoder, motorControl, tof, pid, orientation, chart)
