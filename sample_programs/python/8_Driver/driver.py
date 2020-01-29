# This program demonstrates usage of the servos.
# Keep the robot in a safe location before running this program,
# as it will immediately begin moving.
# See https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/ for more details.

import curses
from motorControl import MotorControl
import signal

# This function is called when Ctrl+C is pressed.
# It's intended for properly exiting the program.


def main(win):
    def ctrlC(signum, frame):
        # Clean up servos
        motorControl.cleanup()

        print("Exiting")
        exit()

    # Attach the Ctrl+C signal interrupt
    signal.signal(signal.SIGINT, ctrlC)

    # Setup motor control
    motorControl = MotorControl()

    win.nodelay(True)
    key = ""
    win.clear()
    win.addstr("Detected key:")
    while 1:
        try:
            key = win.getkey()

            if (str(key) == "KEY_UP"):
                motorControl.setSpeedsPWM(1.7, 1.3)

            if (str(key) == "KEY_DOWN"):
                motorControl.setSpeedsPWM(1.3, 1.7)

            if (str(key) == "KEY_LEFT"):
                motorControl.setSpeedsPWM(1.5, 1.3)

            if (str(key) == "KEY_RIGHT"):
                motorControl.setSpeedsPWM(1.7, 1.5)

        except Exception as e:
            # No input
            pass


curses.wrapper(main)
