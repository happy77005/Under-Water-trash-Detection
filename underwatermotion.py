import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def select_video_file():
    video_path = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
    )
    if video_path:
        process_video(video_path)
    else:
        messagebox.showwarning("No file selected", "Please select a video file to process.")

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # Preprocessing (color correction, noise reduction)
        # Add your techniques here

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

# Set up Tkinter window
root = tk.Tk()
root.title("Trash Detection")

# Create a button to select the video file
select_button = tk.Button(root, text="Select Video File", command=select_video_file)
select_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
