import streamlit as st
import speech_recognition as sr

st.Header("Hi, Goood Evening!")
def arabic_speech_recognition():
    recognizer = sr.Recognizer()

    # Use the Arabic language model
    with sr.Microphone() as source:
        print("Speak something in Arabic...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio, language="ar-SA")  # Recognize Arabic (Saudi Arabia)
        print("You said:", recognized_text)
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
    except sr.RequestError as e:
        print("Error occurred: {0}".format(e))

if __name__ == "__main__":
    arabic_speech_recognition()
