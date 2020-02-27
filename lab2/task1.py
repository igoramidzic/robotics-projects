import json
import time


def moveForwardUntilCloseToWall(inchesAwayFromWall, motorControl, tof):
    motorControl.setSpeedsIPS(5, 5)
    chart = {'front': []}
    timer = time.monotonic()
    while tof.getFrontDistance() > inchesAwayFromWall:
        print(tof.getFrontDistance())
        # if time.monotonic() - timer > 0.1:
        #     chart['front'].append(tof.getFrontDistance())
        #     timer = time.monotonic()
        pass

    motorControl.setSpeedsPWM(0, 0)
    time.sleep(1)
    print(tof.getFrontDistance())
    jj = json.dumps(chart)
    f = open("task1Chart.json", "w")
    f.write(jj)
    f.close()
