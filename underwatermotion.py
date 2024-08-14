import cv2
import numpy as np

# Open a video file or capture from a camera (0 for default camera)
cap = cv2.VideoCapture(r'C:\Users\harip\OneDrive\Desktop\WhatsApp Video 2023-10-06 at 11.52.20_68a5cba6.mp4')

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Preprocessing
    # (Add your color correction and noise reduction techniques here)

    # Background Subtraction
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    background = cv2.medianBlur(gray, 21)
    foreground = cv2.absdiff(gray, background)
    _, thresh = cv2.threshold(foreground, 30, 255, cv2.THRESH_BINARY)

    # Contour Detection
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours (noise)
    contours = [contour for contour in contours if cv2.contourArea(contour) > 100]

    # Draw bounding boxes
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display results
    cv2.imshow('Detected Trash', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release the capture and close the window
cap.release()
cv2.destroyAllWindows()
