import cv2
import numpy as np
from datetime import datetime

def main():
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 for default camera

    # Define codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = None

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the frame
        cv2.imshow('Video Feed', frame)

        # Initialize video recording
        if out is None and ret:
            out = cv2.VideoWriter('output.avi', fourcc, 20.0, (frame.shape[1], frame.shape[0]))

        # Record video when 'r' is pressed
        if out is not None:
            out.write(frame)

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF

        # Quit application when 'q' is pressed
        if key == ord('q'):
            break

        # Start/Stop recording when 'r' is pressed
        if key == ord('r'):
            if out is None:
                print("Recording started.")
            else:
                print("Recording stopped.")
                out.release()
                out = None

        # Take photo when 'p' is pressed
        if key == ord('p'):
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"photo_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Photo saved as {filename}")

    # Release the capture
    cap.release()

    if out is not None:
        out.release()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
