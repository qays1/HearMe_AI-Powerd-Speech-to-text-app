import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio, language="en")
    print(text)
except sr.UnknownValueError:
    text = "Sorry, I could not understand your speech"
except sr.RequestError as e:
    text = "Error occurred: {0}".format(e)