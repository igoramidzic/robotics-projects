import time


def followWall(encoder, motorControl, tof, pid, orientation, chart):
    wallSide = 0
    desiredDistanceForFront = 10
    desiredDistanceForSides = 8
    while (wallSide != "left" and wallSide != "right"):
        wallSide = input('Which wall should I follow? (left, right): ')

    counter = 0

    timer = time.monotonic()

    encoder.resetCounts()
    leftWheelTickCount = 0
    rightWheelTickCount = 0

    while True:
        time.sleep(0.05)

        frontActualDistance = tof.getFrontDistance()
        sideActualDistances = getSaturatedSideDistances(
            tof, desiredDistanceForSides, wallSide)
        leftActualDistance = sideActualDistances[0]
        rightActualDistance = sideActualDistances[1]

        if time.monotonic() - timer > 0.1:
            timer = time.monotonic()
            chart['left'].append(leftActualDistance)
            chart['front'].append(frontActualDistance)
            chart['right'].append(rightActualDistance)

        forwardIPS = 5

        lIPS = forwardIPS
        rIPS = forwardIPS

        leftStraightenIPS = pid.getDesiredSpeed(
            desiredDistanceForSides, leftActualDistance)

        rightStraightenIPS = pid.getDesiredSpeed(
            desiredDistanceForSides, rightActualDistance)

        lIPS = lIPS - leftStraightenIPS
        rIPS = rIPS - rightStraightenIPS

        motorControl.setSpeedsIPS(lIPS, rIPS)

        if (frontActualDistance >= desiredDistanceForFront):
            counter = 0

        if (frontActualDistance <= desiredDistanceForFront):
            counter = counter + 1
            if (counter < 5):
                continue

            leftWheelTickCount = leftWheelTickCount + encoder.getCounts()[0]
            rightWheelTickCount = rightWheelTickCount + encoder.getCounts()[1]
            counter = 0
            motorControl.setSpeedsPWM(0, 0)
            time.sleep(1)
            decideToRotateLeftRightOrUTurn(tof, orientation, wallSide)
            time.sleep(1)


def decideToRotateLeftRightOrUTurn(tof, orientation, wallSide):
    if wallSide == 'left':
        if leftSideAvailable(tof):
            print("Turning left")
            orientation.rotateDegreesAtMaxSpeed(-90)
        elif rightSideAvailable(tof):
            print("Turning right")
            orientation.rotateDegreesAtMaxSpeed(90)
        else:
            print("U-turn")
            orientation.rotateDegreesAtMaxSpeed(180)
    else:
        if rightSideAvailable(tof):
            print("Turning right")
            orientation.rotateDegreesAtMaxSpeed(90)
        elif leftSideAvailable(tof):
            print("Turning left")
            orientation.rotateDegreesAtMaxSpeed(-90)
        else:
            print("U-turn")
            orientation.rotateDegreesAtMaxSpeed(180)

        print("Going straight")


def rightSideAvailable(tof):
    return tof.getRightDistance() > 12


def leftSideAvailable(tof):
    return tof.getLeftDistance() > 12


def getSaturatedSideDistances(tof, desiredDistance, wallSide):
    if wallSide == 'right':
        rightActualDistance = tof.getRightDistance()
        leftActualDistance = desiredDistance + \
            (desiredDistance - rightActualDistance)
    else:
        leftActualDistance = tof.getLeftDistance()
        rightActualDistance = desiredDistance + \
            (desiredDistance - leftActualDistance)

    if leftActualDistance < 0:
        leftActualDistance = 0
    if rightActualDistance < 0:
        rightActualDistance = 0

    # print(leftActualDistance, rightActualDistance)

    return (leftActualDistance, rightActualDistance)
