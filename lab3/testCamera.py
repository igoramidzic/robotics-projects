import cv2
import time

FPS_SMOOTHING = 0.9


def testCamera(camera):
    camera.start()

    fps, prev = 0.0, 0.0
    while True:
        # Calculate FPS
        now = time.time()
        fps = (fps * FPS_SMOOTHING + (1 / (now - prev)) * (1.0 - FPS_SMOOTHING))
        prev = now

        # Get a frame
        frame = camera.read()

        # Write text onto the frame
        cv2.putText(frame, "FPS: {:.1f}".format(
            fps), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        # Display the frame
        cv2.imshow("Preview - Press Esc to exit", frame)

        # Check for user input
        c = cv2.waitKey(1)
        if c == 27 or c == ord('q') or c == ord('Q'):  # Esc or Q
            break

    camera.stop()
