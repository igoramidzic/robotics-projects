import Adafruit_PCA9685
import signal
import math
import time
from encoders import Encoder
import json


# The servo hat uses its own numbering scheme within the Adafruit library.
# 0 represents the first servo, 1 for the second, and so on.
LSERVO = 0
RSERVO = 1


class MotorControl:
    def __init__(self, encoder):
        self.encoder = encoder

        # Initialize the servo hat library.
        self.pwm = Adafruit_PCA9685.PCA9685()

        # 50Hz is used for the frequency of the servos.
        self.pwm.set_pwm_freq(50)

        self.pwm.set_pwm(LSERVO, 0, 0)
        self.pwm.set_pwm(RSERVO, 0, 0)

        self.speedMap = {}

    def calibrateSpeeds(self):
        print("Calibrating speeds...")
        pwm = 1.3
        # For every 0.01 pwm from 1.30 - 1.70
        while pwm <= 1.7:
            lWheelSpeeds = [0]
            rWheelSpeeds = [0]

            # Set speed
            self.setSpeedsPWM(pwm, 1.5 + (1.5 - pwm) if pwm != 0 else 0)

            # Get 5 speeds for each wheel
            for i in range(5):
                timer = time.monotonic()
                while time.monotonic() - timer < 0.5:
                    pass

                speeds = self.encoder.getSpeeds()
                if pwm >= 1.5:
                    lWheelSpeeds.append(-1 * speeds[LSERVO])
                    rWheelSpeeds.append(speeds[RSERVO])
                else:
                    lWheelSpeeds.append(speeds[LSERVO])
                    rWheelSpeeds.append(-1 * speeds[RSERVO])

            # Get average of wheel speeds
            lSpeedMedian = sorted(lWheelSpeeds)[int(len(lWheelSpeeds) / 2)]
            rSpeedMedian = sorted(rWheelSpeeds)[int(len(rWheelSpeeds) / 2)]

            # Update map of speeds
            self.speedMap[pwm] = [lSpeedMedian, rSpeedMedian]
            # Increment pwm by 0.01
            pwm = (round((pwm + .01) * 100) / 100)

        self.setSpeedsPWM(0, 0)

        jj = json.dumps(self.speedMap)
        f = open("calibratedSpeeds.json", "w")
        f.write(jj)
        f.close()

        print("Done calibrating.")

    def checkLoad(self):
        self.setSpeedsPWM(1.6, 1.6)

        lWheelSpeeds = []
        rWheelSpeeds = []

        # Wait 1 second so motors spin up to desired speed
        timer1 = time.monotonic()
        while time.monotonic() - timer1 < 1:
            pass

        # Take 10 measurements of speed every 30ms
        timer1 = time.monotonic()
        while time.monotonic() - timer1 < 10:
            timer2 = time.monotonic()
            while time.monotonic() - timer2 < 0.03:
                pass

            speeds = self.encoder.getSpeeds()

            lWheelSpeeds.append(speeds[LSERVO])
            rWheelSpeeds.append(speeds[RSERVO])

        print(lWheelSpeeds)
        print(rWheelSpeeds)

        f = open("lWheelSpeed.json", "w")
        f.write(str(lWheelSpeeds))
        f.close()

        f = open("rWheelSpeed.json", "w")
        f.write(str(rWheelSpeeds))
        f.close()

        self.setSpeedsPWM(0, 0)
        exit()

    def setSpeedsPWM(self, pwmLeft, pwmRight):
        lPWM = pwmLeft
        rPWM = 1.5 + (1.5 - pwmRight) if pwmRight != 0 else 0

        # Due to how servos work, and the design of the Adafruit library,
        # the value must be divided by 20 and multiplied by 4096.
        self.pwm.set_pwm(LSERVO, 0, math.floor(lPWM / 20 * 4096))
        self.pwm.set_pwm(RSERVO, 0, math.floor(rPWM / 20 * 4096))

    def setSpeedsRPS(self, rpsLeft, rpsRight):
        rpsRight *= -1
        lClosestPWM = "1.3"
        rClosestPWM = "1.3"
        for key in self.speedMap.keys():
            if abs(rpsLeft + self.speedMap[lClosestPWM][LSERVO]) > abs(rpsLeft + self.speedMap[key][LSERVO]):
                lClosestPWM = key
            if abs(rpsRight + self.speedMap[rClosestPWM][RSERVO]) > abs(rpsRight + self.speedMap[key][RSERVO]):
                rClosestPWM = key

        self.setSpeedsPWM(float(lClosestPWM), float(rClosestPWM))

    def setSpeedsIPS(self, ipsLeft, ipsRight):
        ipsRight *= -1
        lClosestPWM = "1.3"
        rClosestPWM = "1.3"
        for key in self.speedMap.keys():
            if abs(ipsLeft + 8.19955 * self.speedMap[lClosestPWM][LSERVO]) > abs(ipsLeft + 8.19955 * self.speedMap[key][LSERVO]):
                lClosestPWM = key
            if abs(ipsRight + 8.19955 * self.speedMap[rClosestPWM][RSERVO]) > abs(ipsRight + 8.19955 * self.speedMap[key][RSERVO]):
                rClosestPWM = key

        print(lClosestPWM, rClosestPWM)
        self.setSpeedsPWM(float(lClosestPWM), float(rClosestPWM))

    def setSpeedsVW(self, v, w):
        radiusOfCircle = v / w

        # vR = v + (w * self.encoder.DIST_BETWEEN_WHEELS) / 2
        # vL = 2 * v - vR
        vL = w * (radiusOfCircle + (self.encoder.DIST_BETWEEN_WHEELS / 2))
        vR = w * (radiusOfCircle - (self.encoder.DIST_BETWEEN_WHEELS / 2))

        print("vR: ", vR, "vL: ", vL)

        self.setSpeedsIPS(vR, vL)

    def cleanup(self):
        # Stop servos
        print("Stopping servos")
        # Stop the servos
        self.pwm.set_pwm(LSERVO, 0, 0)
        self.pwm.set_pwm(RSERVO, 0, 0)
