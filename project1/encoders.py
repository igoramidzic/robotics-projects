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

        self.LStartTime = time.monotonic()
        self.RStartTime = time.monotonic()

    def resetCounts(self):
        self.LTickCount = 0
        self.RTickCount = 0

    def getCounts(self):
        return self.LTickCount, self.RTickCount

    def getSpeeds(self):
        lSpeed = self.LWheelSpeed
        rSpeed = self.RWheelSpeed

        if (time.monotonic() - self.LStartTime > 0.5):
            lSpeed = 0
        if (time.monotonic() - self.RStartTime > 0.5):
            rSpeed = 0

        return lSpeed, rSpeed

    # This function is called when the left encoder detects a rising edge signal.
    def onLeftEncode(self, pin):
        self.LTickCount += 1
        elapsedTime = time.monotonic() - self.LStartTime
        self.LWheelSpeed = (1/32) / elapsedTime
        self.LStartTime = time.monotonic()

    # This function is called when the right encoder detects a rising edge signal.
    def onRightEncode(self, pin):
        self.RTickCount += 1
        elapsedTime = time.monotonic() - self.RStartTime
        self.RWheelSpeed = (1/32) / elapsedTime
        self.RStartTime = time.monotonic()

    # This function is called when Ctrl+C is pressed.
    # It's intended for properly exiting the program.
    def cleanup(self):
        print("Cleaning up Encoders")
        GPIO.cleanup()

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
