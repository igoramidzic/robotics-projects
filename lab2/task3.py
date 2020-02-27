def followWall(motorControl, tof, pid):
    wallSide = 0
    while (wallSide != "left" and wallSide != "right"):
        wallSide = input('Which wall should I follow? (left, right): ')

    print(wallSide)
    pass
