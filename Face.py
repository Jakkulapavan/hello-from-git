import tkinter as tk
from tkinter import Message, Text
import cv2
import os
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from pymongo import MongoClient

# MongoDB Connection Setup
client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB connection string
db = client['FaceRecognitionDB']  # Database name
collection = db['AttendanceImages']  # Collection name

window = tk.Tk()
window.title("Face_Recogniser attendance system")
window.geometry('1366x768')

# Initial Camera Launch
def open_camera():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        message.configure(text="Error: Camera not accessible.")
        return
    ret, frame = cam.read()
    if ret:
        cv2.imshow('Camera Preview', frame)
    cam.release()

# Function to capture and store image in MongoDB
def capture_picture():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        message.configure(text="Error: Camera not accessible.")
        return

    ret, frame = cam.read()
    if ret:
        cv2.imshow('Captured Image', frame)
        file_name = f"Captured_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(file_name, frame)

        # Save image binary to MongoDB
        with open(file_name, 'rb') as image_file:
            image_data = image_file.read()
            collection.insert_one({
                "image_name": file_name,
                "student_id": txt.get(),
                "student_name": txt2.get(),
                "image_data": image_data,
                "timestamp": datetime.datetime.now()
            })
        message.configure(text=f"Image {file_name} saved to MongoDB.")
    else:
        message.configure(text="Error: Failed to capture image.")

    cam.release()
    cv2.destroyAllWindows()

# UI Setup
message = tk.Label(window, text="Face-Recognition-Attendance-System", bg="grey", fg="black", 
                   width=50, height=3, font=('arial', 30, 'italic bold underline'))
message.place(x=80, y=20)

lbl = tk.Label(window, text="Student ID", width=20, height=2, fg="white", bg="green", font=('times', 15, ' bold '))
lbl.place(x=400, y=200)

lbl2 = tk.Label(window, text="Student Name", width=20, height=2, fg="white", bg="green", font=('times', 15, ' bold '))
lbl2.place(x=400, y=300)

txt = tk.Entry(window, width=20, bg="green", fg="white", font=('times', 15, ' bold '))
txt.place(x=700, y=215)

txt2 = tk.Entry(window, width=20, bg="green", fg="white", font=('times', 15, ' bold '))
txt2.place(x=700, y=315)

capture_img_button = tk.Button(window, text="Click the Picture", command=capture_picture, fg="blue", bg="white",
                               width=20, height=2, activebackground="LightBlue", font=('times', 15, 'bold'))
capture_img_button.place(x=500, y=500)

quitWindow = tk.Button(window, text="Quit", command=quit, fg="red", bg="yellow", width=20, height=3,
                       activebackground="Red", font=('times', 15, ' bold '))
quitWindow.place(x=500, y=600)

open_camera()  # Automatically opens camera on startup

window.mainloop()
