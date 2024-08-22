import cv2
import numpy as np
import pyautogui
import time
import win32gui
import win32con
from os import mkdir
import threading
import tkinter as tk

# Create directory if not available
try:
    mkdir("recordings")
except FileExistsError:
    pass

# Method to minimize window
def minimizeWindow():
    window = win32gui.FindWindow(None, "Screen recorder")
    win32gui.ShowWindow(window, win32con.SW_MINIMIZE)

# Initialize screen resolution (adjust to your screen size)
SCREEN_SIZE = (1366, 768)

# Define the video codec
fourcc = cv2.VideoWriter_fourcc(*"XVID")

# Create the video writer object
output = None

# Variable to control the recording state
recording = False

# Method to start recording
def start_recording():
    global recording, output
    output = cv2.VideoWriter(
        "recordings/ScreenRecording_" + time.strftime("%H-%M-%S_%d-%m-%y") + ".mp4",
        fourcc,
        20.0,
        SCREEN_SIZE
    )
    recording = True
    recording_label.config(text="Recording started.... \nWindow minimized in taskbar.\nPress 'q' to exit.")
    record_screen()

# Method to stop recording
def stop_recording():
    global recording
    recording = False
    recording_label.config(text="Recording stopped.")
    output.release()
    cv2.destroyAllWindows()

# Method to record the screen
def record_screen():
    global minimized
    minimized = False
    while recording:
        # Make a screenshot
        img = pyautogui.screenshot()

        # Convert these pixels to a proper numpy array to work with OpenCV
        frame = np.array(img)

        # Convert colors from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Show the frame (you may want to comment this out to save resources)
        cv2.imshow("Screen recorder", frame)

        if not minimized:
            minimized = True
            minimizeWindow()

        # Write the frame
        output.write(frame)

        # If the user clicks 'q', it exits
        if cv2.waitKey(1) == ord("q"):
            stop_recording()
            break

# Tkinter GUI setup
root = tk.Tk()
root.title("Screen Recorder")

# Create and place start button
start_button = tk.Button(root, text="Start Recording", command=start_recording)
start_button.pack(pady=10)

# Create and place stop button
stop_button = tk.Button(root, text="Stop Recording", command=stop_recording)
stop_button.pack(pady=10)

# Create and place label to display recording status
recording_label = tk.Label(root, text="Press 'Start Recording' to begin.")
recording_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
