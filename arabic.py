import speech_recognition as sr
import streamlit as st
from email.message import EmailMessage
import smtplib
from langdetect import detect
import os
import json

img="https://i.pinimg.com/564x/f5/10/e0/f510e03bb0e529ef33a5479940b70aab.jpg"
st.image(img,width=720)

st.title("_Hear_:blue[Me]:star:")
st.subheader("Where your words are heared ")
with st.sidebar:
    #st.image("https://i.pinimg.com/564x/0c/78/06/0c7806349ca7fc25c6596968f5c214c9.jpg")
    #st.camera_input("open your cam ??")
    choice= st.radio("",["record voice","upload voice file","contact us"])
    recognizer = sr.Recognizer()

if choice == "record voice":
    is_recording = False


    st.title("Voice Recording")
    def record_audio(language):
        recognizer = sr.Recognizer()
        is_recording = True

        with sr.Microphone() as source:
            st.write(f"Speak something in {language}...")
            audio = recognizer.listen(source)

            try:
                if language == "arabic":
                    recognized_text = recognizer.recognize_google(audio, language="ar-SA")
                    st.write("لقد قلت: ", recognized_text)
                else:
                    recognized_text = recognizer.recognize_google(audio, language="en")
                    st.write("You said: ", recognized_text)
            except sr.UnknownValueError:
                st.write("Speech recognition could not understand audio")
            except sr.RequestError as e:
                st.write(f"Could not request results from Google Speech Recognition service; {e}")

        is_recording = False
   
    
    # User interface
    language = st.selectbox("Select your language", ["arabic", "English"])

    if not is_recording:
        if st.button("Start Recording"):
            record_audio(language)
    else:
        st.write("Recording in progress...")

if choice == "upload voice file":
    st.title("Select File Language: ")
    language = st.selectbox("Select your language", ["arabic", "English"])

    st.title(f"Select a WAV audio file to transcribe in {language}")
    file = st.file_uploader("Upload a WAV audio file", type=["wav"])  # Only accept WAV files
    
    if file:
        st.audio(file)

        # Read the uploaded audio file as binary data
        audio_data = sr.AudioFile(file)

        # Initialize the recognizer
        recognizer = sr.Recognizer()

        # Perform speech recognition on the audio file based on the selected language
        try:
            with audio_data as source:
                audio = recognizer.record(source)
                if language == "arabic":
                    recognized_text = recognizer.recognize_google(audio, language="ar-SA")  # Recognize Arabic
                elif language == "English":
                    recognized_text = recognizer.recognize_google(audio, language="en")  # Recognize English
                
                st.write(f"Recognized Text ({language}): ", recognized_text)
        except sr.UnknownValueError:
            st.write("Speech recognition could not understand audio")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")

if choice == "contact us":
    st.header("Feedback Form")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email (optional)")
    feedback = st.text_area("Feedback", height=200)

    
    if st.button('send feedback'):
        subject = "Streamlit App Feedback "
        message = f"Name: {name}\nEmail: {email}\n\nFeedback:\n{feedback}"
        
        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)

            # Access sensitive information
            email_sender = config_data["email"]
            email_password = config_data["password"]
        
        email_receiver= "qaysmahfouz@outlook.com"
        


        em= EmailMessage()
        em['From']=name
        em['To']=email_receiver
        em['subject']= subject
        em.set_content(message)

        with smtplib.SMTP("smtp-mail.outlook.com", port=587) as connection:
            connection.starttls()
            connection.login(user=email_sender, password=email_password)
            connection.sendmail(
            from_addr=email_sender,
            to_addrs=email_receiver,
            msg=f"Subject:{subject} \n\n from: {name}\n\nemail: {email}\n\nfeedback:  {feedback}")



        st.success("Thank you for your feedback! It has been sent.")
        
