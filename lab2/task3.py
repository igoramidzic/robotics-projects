def followWall(motorControl, tof, pid, orientation):
    wallSide = 0
    desiredDistanceForFront = 12
    while (wallSide != "left" and wallSide != "right"):
        wallSide = input('Which wall should I follow? (left, right): ')

    print(wallSide)

    sideActualDistance = 0

    while True:
        frontActualDistance = tof.getFrontDistance()
        print(frontActualDistance)

        if (wallSide == "right"):
            sideActualDistance = tof.getRightDistance()
        else:
            sideActualDistance = tof.getLeftDistance()

        forwardIPS = pid.getDesiredSpeed(
            desiredDistanceForFront, frontActualDistance)

        desiredDistanceForSide = 3

        lIPS = forwardIPS
        rIPS = forwardIPS

        lIPS = lIPS - pid.getDesiredSpeed(
            desiredDistanceForSide, sideActualDistance - ())
        rIPS = rIPS - pid.getDesiredSpeed(
            desiredDistanceForSide, sideActualDistance)

        print(lIPS, rIPS)

        motorControl.setSpeedsIPS(lIPS, rIPS)

        if (wallSide == "right"):
            checkRight(tof)
            # if (tof.getRightDistance() > 7):
            #     pass
        else:
            checkLeft(tof)

        if (tof.getRightDistance() < 7 and tof.getLeftDistance() < 7 and tof.getFrontDistance() < 14):
            orientation.rotateDegreesAtMaxSpeed(180)


def checkRight(tof):
    if (tof.getRightDistance() > 12):
        print("Found right opening!")


def checkLeft(tof):
    if (tof.getLeftDistance() > 12):
        print("Found left opening!")
