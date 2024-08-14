import cv2
import numpy as np
from tkinter import Tk, filedialog

# Function to get the file path using Tkinter
def get_image_path():
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_path = filedialog.askopenfilename(title='Select an image file', 
                                           filetypes=[('Image files', '*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.tif')])
    return file_path

# Get the image path
image_path = get_image_path()

# Read the image
image = cv2.imread(image_path)
if image is None:
    raise ValueError("Image not found or unable to read the image file.")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply median blur
background = cv2.medianBlur(gray, 21)

# Foreground extraction
foreground = cv2.absdiff(gray, background)

# Thresholding
_, thresh = cv2.threshold(foreground, 30, 255, cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter small contours
contours = [contour for contour in contours if cv2.contourArea(contour) > 100]

# Draw bounding rectangles
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display the image
cv2.imshow('Detected Trash', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
