import time
import json


def followParallelToWalls(motorControl, tof, pid):
    timer = time.monotonic()
    chart = {'left': [],
             'front': [],
             'right': []}

    alreadySavedChart = False
    while True:
        leftActualDistance = tof.getLeftDistance()
        rightActualDistance = tof.getRightDistance()

        desiredDistance = (leftActualDistance + rightActualDistance) / 2

        lIPS = pid.getDesiredSpeed(
            desiredDistance, leftActualDistance)
        rIPS = pid.getDesiredSpeed(
            desiredDistance, rightActualDistance)

        # motorControl.setSpeedsIPS(6 - lIPS, 6 - rIPS)

        if time.monotonic() - timer > 0.1:
            timer = time.monotonic()
            chart['left'].append(leftActualDistance)
            chart['right'].append(rightActualDistance)

        if not alreadySavedChart and leftActualDistance < 12:
            jj = json.dumps(chart)
            f = open("distanceChart.json", "w")
            f.write(jj)
            f.close()
            alreadySavedChart = True
