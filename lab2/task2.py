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
        frontActualDistance = tof.getFrontDistance()
        rightActualDistance = tof.getRightDistance()

        desiredDistanceForFront = 12
        desiredDistanceForSides = (
            leftActualDistance + rightActualDistance) / 2

        forwardIPS = pid.getDesiredSpeed(
            desiredDistanceForFront, frontActualDistance)

        lIPS = forwardIPS
        rIPS = forwardIPS

        # lIPS = lIPS - pid.getDesiredSpeed(
        #     desiredDistanceForSides, leftActualDistance)
        # rIPS = rIPS - pid.getDesiredSpeed(
        #     desiredDistanceForSides, rightActualDistance)

        motorControl.setSpeedsIPS(lIPS, rIPS)

        if time.monotonic() - timer > 0.1:
            timer = time.monotonic()
            chart['left'].append(leftActualDistance)
            chart['right'].append(rightActualDistance)

        if not alreadySavedChart and frontActualDistance < 12:
            jj = json.dumps(chart)
            f = open("distanceChart.json", "w")
            f.write(jj)
            f.close()
            alreadySavedChart = True
