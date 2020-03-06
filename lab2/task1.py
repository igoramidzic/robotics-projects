import json
import time


def moveForwardUntilCloseToWall(inchesAwayFromWall, motorControl, tof):
    motorControl.setSpeedsIPS(5, 5)
    chart = {'front': [], 'right': [], 'left': []}
    timer = time.monotonic()
    while tof.getFrontDistance() > inchesAwayFromWall:
        print(tof.getFrontDistance())
        if time.monotonic() - timer > 0.1:
            chart['front'].append(tof.getFrontDistance())
            chart['right'].append(tof.getRightDistance())
            chart['left'].append(tof.getLeftDistance())
            timer = time.monotonic()
        pass

    motorControl.setSpeedsPWM(0, 0)
