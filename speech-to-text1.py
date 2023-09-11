import cv2
import threading
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pydub import AudioSegment  # Import AudioSegment from pydub
import numpy as np
import pyaudio
# Initialize the recognizer and microphone
r = sr.Recognizer()

# Define a function to capture audio and perform speech recognition
def capture_noise_profile():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    print("Capturing noise profile... (please remain silent)")

    # Capture audio data for 3 seconds to obtain the noise profile
    audio_data = b""
    for _ in range(0, int(16000 / 1024 * 3)):
        audio_data += stream.read(1024)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Convert audio data to numpy array
    audio_data = np.frombuffer(audio_data, dtype=np.int16)

    # Create an AudioSegment from the numpy array
    noise_sample = AudioSegment(
        audio_data.tobytes(),
        frame_rate=16000,
        sample_width=2,
        channels=1
    )

    return noise_sample

# Capture the noise profile
noise_profile = capture_noise_profile()

def recognize_speech():
    global recognized_text
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Say something!")

            try:
                audio = r.listen(source)

                # Apply noise reduction to the audio
                reduced_audio = audio - noise_profile
                
                text = r.recognize_google(reduced_audio, language="en")
            except sr.UnknownValueError:
                text = "Sorry, I could not understand your speech"
            except sr.RequestError as e:
                text = "Error occurred: {0}".format(e)

            # Update the recognized text
            recognized_text.set(text)

# Function to start speech recognition in a separate thread
def start_recognition_thread():
    recognition_thread = threading.Thread(target=recognize_speech)
    recognition_thread.daemon = True
    recognition_thread.start()

# Create a Tkinter window
root = tk.Tk()
root.title("Deaf Assistance App")

# Create a label to display recognized text
recognized_text = tk.StringVar()
text_label = ttk.Label(root, textvariable=recognized_text, font=("Arial", 16))
text_label.pack(pady=20)

# Initialize the camera
cap = cv2.VideoCapture(0)

# Function to update the video feed
def update_video_feed():
    ret, frame = cap.read()
    if ret:
        # Convert frame to PhotoImage using PIL
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (400, 300))
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=img)

        # Update the label with the new frame
        video_label.config(image=photo)
        video_label.image = photo

    # Call this function again after a delay
    root.after(10, update_video_feed)

# Create a label to display the video feed
video_label = ttk.Label(root)
video_label.pack()

# Create a button to start speech recognition
start_button = ttk.Button(root, text="Start Recognition", command=start_recognition_thread)
start_button.pack(pady=10)

# Start updating the video feed
update_video_feed()

# Start the Tkinter main loop
root.mainloop()

# Release the camera
cap.release()
