import pyttsx3
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
from pyaudio import PyAudio, paInt16
import json
from eventhook import Event_hook
from threading import Thread, Lock


class AI():
    __name = ''
    __skill = []
    lock = Lock()

    def __init__(self, name=None) -> None:
        self.engine = pyttsx3.init()

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[11].id)

        model = Model('./model')
        self.r = KaldiRecognizer(model, 16000)
        self.m = PyAudio()

        if name is not None:
            self.__name = name

        self.audio = self.m.open(
            format=paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        self.audio.start_stream()

        self.before_speaking = Event_hook()
        self.after_speaking = Event_hook()
        self.before_listening = Event_hook()
        self.after_listening = Event_hook()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        sentence = "Hello, I am is" + self.__name
        self.__name = value
        self.engine.say(sentence)
        self.engine.runAndWait()

    def speak(self, sentence):
        self.lock.acquire()
        print(sentence)
        self.before_speaking.trigger(sentence)
        self.engine.say(sentence)
        self.engine.iterate()
        self.after_speaking.trigger(sentence)
        self.lock.release()

    def say(self, sentence):
        self.engine.startLoop(False)
        t = Thread(target=self.speak, args=(sentence,))
        t.start()
        self.engine.endLoop()

    def listen(self):
        def remove_prefix(text, prefix):
            if text.startswith(prefix):
                return text[len(prefix):]
            return text
        phrase = ""
        if self.r.AcceptWaveform(self.audio.read(4096, exception_on_overflow=False)):
            self.before_listening.trigger()
            phrase = self.r.Result()
            phrase = remove_prefix(phrase, 'the ')
            phrase = str(json.loads(phrase)["text"])

            if phrase:
                self.after_listening.trigger(phrase)
            return phrase

        return None
