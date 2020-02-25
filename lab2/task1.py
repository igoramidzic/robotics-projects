import json
import time


def moveForwardUntilCloseToWall(inchesAwayFromWall, motorControl, tof):
    motorControl.setSpeedsPWM(1.7, 1.7)
    chart = {'front': []}
    timer = time.monotonic()
    while tof.getLeftDistance() > inchesAwayFromWall:
        if time.monotonic() - timer > 0.1:
            chart['front'].append(tof.getLeftDistance())
    motorControl.setSpeedsPWM(0, 0)
    jj = json.dumps(chart)
    f = open("task1Chart.json", "w")
    f.write(jj)
    f.close()
