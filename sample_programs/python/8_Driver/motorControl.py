import Adafruit_PCA9685
import signal
import math

# The servo hat uses its own numbering scheme within the Adafruit library.
# 0 represents the first servo, 1 for the second, and so on.
LSERVO = 0
RSERVO = 1


class MotorControl:
    def __init__(self):
        # Initialize the servo hat library.
        self.pwm = Adafruit_PCA9685.PCA9685()

        # 50Hz is used for the frequency of the servos.
        self.pwm.set_pwm_freq(50)

        self.pwm.set_pwm(LSERVO, 0, 0)
        self.pwm.set_pwm(RSERVO, 0, 0)

    # def calibrateSpeeds(self):
    #     pass

    def setSpeedsPWM(self, pwmLeft, pwmRight):
        # Due to how servos work, and the design of the Adafruit library,
        # the value must be divided by 20 and multiplied by 4096.
        self.pwm.set_pwm(LSERVO, 0, math.floor(pwmLeft / 20 * 4096))
        self.pwm.set_pwm(RSERVO, 0, math.floor(pwmRight / 20 * 4096))

    # def setSpeedsIPS(self, ipsLeft, ipsRight):
    #     pass

    # def setSpeedsVW(self, v, w):
    #     pass

    def cleanup(self):
        # Stop servos
        print("Stopping servos")
        # Stop the servos
        self.pwm.set_pwm(LSERVO, 0, 0)
        self.pwm.set_pwm(RSERVO, 0, 0)
