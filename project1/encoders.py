import signal
import RPi.GPIO as GPIO
import time

LENCODER = 17
RENCODER = 18


class Encoder:
    def __init__(self):
        self.LTickCount = 0
        self.RTickCount = 0

        self.LWheelSpeed = 0
        self.RWheelSpeed = 0

    def resetCounts(self):
        print("Reseting")
        self.LTickCount = 0
        self.RTickCount = 0

    def getCounts(self):
        return self.LTickCount, self.RTickCount

    def getSpeeds(self):
        return self.LWheelSpeed, self.RWheelSpeed

    # This function is called when the left encoder detects a rising edge signal.
    def onLeftEncode(self, pin):
        self.LTickCount += 1

    # This function is called when the right encoder detects a rising edge signal.
    def onRightEncode(self, pin):
        self.RTickCount += 1

    # This function is called when Ctrl+C is pressed.
    # It's intended for properly exiting the program.
    def cleanup(self):
        print("Cleaning up Encoders")
        GPIO.cleanup()
        exit()

    def initEncoders(self):
        # Set the pin numbering scheme to the numbering shown on the robot itself.
        GPIO.setmode(GPIO.BCM)

        # Set encoder pins as input
        # Also enable pull-up resistors on the encoder pins
        # This ensures a clean 0V and 3.3V is always outputted from the encoders.
        GPIO.setup(LENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(RENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Attach a rising edge interrupt to the encoder pins
        GPIO.add_event_detect(LENCODER, GPIO.RISING, self.onLeftEncode)
        GPIO.add_event_detect(RENCODER, GPIO.RISING, self.onRightEncode)
