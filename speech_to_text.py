import speech_recognition as sr
import streamlit as st
st.header("HearMe")
st.subheader("Where your words are heared ")
with st.sidebar:
    st.image("https://i.pinimg.com/564x/0c/78/06/0c7806349ca7fc25c6596968f5c214c9.jpg")
    #st.camera_input("open your cam ??")
    choice= st.radio("Navigation",["record voice","upload voice file","about IVA JO","contact us"])
    recognizer = sr.Recognizer()

if choice == "record voice":
    st.title("Start Record")
    lang= st.selectbox("select your language", ["arabic","english"])
    if lang == "arabic":
        with sr.Microphone() as source:
            print("Speak something in Arabic...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source)
        
            try:
                recognized_text = recognizer.recognize_google(audio, language="ar-SA")  # Recognize Arabic (Saudi Arabia)
                st.write("You said",recognized_text)
            except:
                if recognized_text =="توقف":
                    print("exiting...") 
    else:
        with sr.Microphone() as source:
            print("Speak something in English...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source)
        
            try:
                recognized_text = recognizer.recognize_google(audio, language="en")  # Recognize english
                st.write("You said",recognized_text)
            except:
                if recognized_text =="stop":
                    print("exiting...") 

if choice == "upload voice file":
    st.title("select files to transpect")
    file = st.file_uploader(" ")
    if file:
        st.audio(file)
        recognized_text1 = recognizer.recognize_google(file, language="ar-SA")
        st.write(recognized_text1)
