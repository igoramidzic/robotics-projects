import time
import cv2 as cv
import json

FPS_SMOOTHING = 0.9
CENTER_X_COORD = 300
KP = 0.05

# Window names
WINDOW1 = "Adjustable Mask - Press Esc to quit"
WINDOW2 = "Detected Blobs - Press Esc to quit"

# Default HSV ranges
# Note: the range for hue is 0-180, not 0-255
minH = 0
minS = 127
minV = 0
maxH = 180
maxS = 255
maxV = 255


def setMaskToLookForRed():
    global minH
    global minS
    global minV
    global maxH
    global maxS
    global maxV

    minH = 171
    minS = 170
    minV = 28
    maxH = 178
    maxS = 255
    maxV = 177


def setMaskToLookForBlue():
    global minH
    global minS
    global minV
    global maxH
    global maxS
    global maxV

    minH = 87
    minS = 78
    minV = 38
    maxH = 101
    maxS = 190
    maxV = 255


def setMaskToLookForGreen():
    global minH
    global minS
    global minV
    global maxH
    global maxS
    global maxV

    minH = 56
    minS = 78
    minV = 38
    maxH = 88
    maxS = 190
    maxV = 255


def setMaskToLookForColor(color):
    if color == "1":
        setMaskToLookForRed()
    if color == "2":
        setMaskToLookForGreen()
    if color == "3":
        setMaskToLookForBlue()


def faceGoal(distanceError, motorControl):
    ips = KP * distanceError
    if ips > 3:
        ips = 3
    if ips < -3:
        ips = -3

    motorControl.setSpeedsIPS(ips, -1 * ips)


def run(motorControl, camera):
    # Ask user for color here:
    color = input(
        "What color would you like? (red (1), green (2), blue (3)): ")
    print("\n")
    setMaskToLookForColor(color)

    camera.start()

    # Initialize the SimpleBlobDetector
    params = cv.SimpleBlobDetector_Params()
    detector = cv.SimpleBlobDetector_create(params)

    # Attempt to open a SimpleBlobDetector parameters file if it exists,
    # Otherwise, one will be generated.
    # These values WILL need to be adjusted for accurate and fast blob detection.
    # yaml, xml, or json
    fs = cv.FileStorage("params.yaml", cv.FILE_STORAGE_READ)
    if fs.isOpened():
        detector.read(fs.root())
    else:
        print("WARNING: params file not found! Creating default file.")

        fs2 = cv.FileStorage("params.yaml", cv.FILE_STORAGE_WRITE)
        detector.write(fs2)
        fs2.release()

    fs.release()

    # Create windows
    cv.namedWindow(WINDOW1)
    cv.namedWindow(WINDOW2)

    fps, prev = 0.0, 0.0
    while True:
        # Calculate FPS
        now = time.time()
        fps = (fps * FPS_SMOOTHING + (1 / (now - prev)) * (1.0 - FPS_SMOOTHING))
        prev = now

        # Get a frame
        frame = camera.read()

        # Blob detection works better in the HSV color space
        # (than the RGB color space) so the frame is converted to HSV.
        frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Create a mask using the given HSV range
        mask = cv.inRange(frame_hsv, (minH, minS, minV), (maxH, maxS, maxV))

        # Run the SimpleBlobDetector on the mask.
        # The results are stored in a vector of 'KeyPoint' objects,
        # which describe the location and size of the blobs.
        keypoints = detector.detect(mask)

        # For each detected blob, draw a circle on the frame
        frame_with_keypoints = cv.drawKeypoints(frame, keypoints, None, color=(
            0, 255, 0), flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # Write text onto the frame
        cv.putText(frame_with_keypoints, "FPS: {:.1f}".format(
            fps), (5, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
        cv.putText(frame_with_keypoints, "{} blobs".format(
            len(keypoints)), (5, 35), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        # Display the frame
        cv.imshow(WINDOW1, mask)
        cv.imshow(WINDOW2, frame_with_keypoints)

        # Check for user input
        c = cv.waitKey(1)
        if c == 27 or c == ord('q') or c == ord('Q'):  # Esc or Q
            camera.stop()
            break

        # Get one KeyPoint
        points = cv.KeyPoint_convert(keypoints)

        xPoint = 0
        if len(points) > 0:
            xPoint = points[0][0]

        distanceError = xPoint - CENTER_X_COORD

        if abs(distanceError) > 150:
            faceGoal(distanceError, motorControl)
        else:
            motorControl.setSpeedsPWM(0, 0)

    camera.stop()
