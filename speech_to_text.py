import speech_recognition as sr

def stt():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak Anything")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            text=r.recognize_google(audio)
        except:
            print("Sorry Could not get you")