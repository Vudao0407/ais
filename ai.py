import pyttsx3
import speech_recognition as sr


class AI():
    __name = ''
    __skill = []

    def __init__(self, name=None) -> None:
        self.engine = pyttsx3.init("espeak")
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[11].id)
        self.r = sr.Recognizer()
        self.m = sr.Microphone()

        if name is not None:
            self.__name = name

        print('Listening')

        with self.m as source:
            self.r.adjust_for_ambient_noise(source)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        sentence = "Hello, i am i" + self.__name
        self.__name = value
        self.engine.say(sentence)
        self.engine.runAndWait()

    def say(self, sentence):
        self.engine.say(sentence)
        self.engine.runAndWait()

    def listen(self):
        print('say something')
        with self.m as source:
            audio = self.r.listen(source)
        print('got it')

        try:
            phrase = self.r.recognize_google(
                audio, show_all=False, language='en-bg')
            sentence = "Got it, you said" + phrase
            self.engine.say(sentence)
            self.engine.runAndWait()

        except Exception as exception:
            sentence = "I do not get it"
            self.engine.say(sentence)
            self.engine.runAndWait()
            print(exception)

        print('You said', phrase)
        return phrase
