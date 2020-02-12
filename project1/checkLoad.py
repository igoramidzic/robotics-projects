# This program demonstrates usage of the servos.
# Keep the robot in a safe location before running this program,
# as it will immediately begin moving.
# See https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/ for more details.

from encoders import Encoder
from motorControl import MotorControl
import signal

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

motorControl.checkLoad()

while True:
    pass