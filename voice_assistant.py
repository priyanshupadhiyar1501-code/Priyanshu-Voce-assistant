import os
import re
import sys
import time
import webbrowser
import ctypes
import subprocess

import speech_recognition as sr
import pyttsx3

WAKE_WORDS = ["assistant", "hey assistant", "okay assistant", "wake up"]


class VoiceAssistant:
    def __init__(self, wake_words=None):
        self.wake_words = wake_words or WAKE_WORDS
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 160)
        self.engine.setProperty("volume", 1.0)

    def speak(self, text: str):
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, timeout=5, phrase_time_limit=6):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        return audio

    def recognize_offline(self, audio):
        try:
            text = self.recognizer.recognize_sphinx(audio)
            print(f"Heard (offline): {text}")
            return text.lower()
        except sr.RequestError:
            self.speak("PocketSphinx is not available. Please install pocketsphinx for offline recognition.")
            return ""
        except sr.UnknownValueError:
            return ""

    def has_wake_word(self, text: str) -> bool:
        return any(wake_word in text for wake_word in self.wake_words)

    def listen_for_wake_word(self):
        self.speak("Ready. Say the wake word to begin.")
        while True:
            try:
                audio = self.listen(timeout=7, phrase_time_limit=4)
                text = self.recognize_offline(audio)
                if text and self.has_wake_word(text):
                    self.speak("Yes? How can I help?")
                    return
            except sr.WaitTimeoutError:
                continue
            except KeyboardInterrupt:
                self.speak("Goodbye.")
                sys.exit(0)

    def listen_command(self):
        try:
            audio = self.listen(timeout=5, phrase_time_limit=6)
            return self.recognize_offline(audio)
        except sr.WaitTimeoutError:
            return ""
        except KeyboardInterrupt:
            self.speak("Goodbye.")
            sys.exit(0)

    def process_command(self, command: str):
        if not command:
            self.speak("I did not catch that. Please say the command again.")
            return False

        if any(word in command for word in ["exit", "quit", "stop", "goodbye"]):
            self.speak("Shutting down. Talk soon.")
            return True

        if "time" in command:
            self.speak(time.strftime("The current time is %I:%M %p."))
            return False

        if "date" in command:
            self.speak(time.strftime("Today is %A, %B %d, %Y."))
            return False

        if "open browser" in command or "open chrome" in command or "open edge" in command:
            self.speak("Opening your web browser.")
            webbrowser.open("https://www.google.com")
            return False

        if "search for" in command:
            query = command.split("search for", 1)[1].strip()
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            self.speak(f"Searching for {query}.")
            webbrowser.open(url)
            return False

        if "go to" in command or "open website" in command:
            target = command.split("go to", 1)[1].strip() if "go to" in command else command.split("open website", 1)[1].strip()
            if not target.startswith("http"):
                target = f"https://{target}"
            self.speak(f"Navigating to {target}.")
            webbrowser.open(target)
            return False

        if "open notepad" in command:
            self.speak("Opening Notepad.")
            subprocess.Popen(["notepad.exe"])
            return False

        if "open calculator" in command or "open calc" in command:
            self.speak("Opening Calculator.")
            subprocess.Popen(["calc.exe"])
            return False

        if "open explorer" in command or "open file explorer" in command or "show files" in command:
            self.speak("Opening File Explorer.")
            os.startfile(os.path.expanduser("~"))
            return False

        if "lock" in command and "computer" in command:
            self.speak("Locking the computer.")
            ctypes.windll.user32.LockWorkStation()
            return False

        if any(phrase in command for phrase in ["volume up", "increase volume", "raise volume"]):
            self.adjust_volume(1)
            self.speak("Volume increased.")
            return False

        if any(phrase in command for phrase in ["volume down", "decrease volume", "lower volume"]):
            self.adjust_volume(-1)
            self.speak("Volume decreased.")
            return False

        if "mute" in command:
            self.send_volume_command(0x80000)
            self.speak("Volume muted.")
            return False

        if "shutdown" in command:
            self.speak("Shutting down the system.")
            subprocess.Popen(["shutdown", "/s", "/t", "10"])
            return False

        if "restart" in command or "reboot" in command:
            self.speak("Restarting the system.")
            subprocess.Popen(["shutdown", "/r", "/t", "10"])
            return False

        if "what is" in command or "who is" in command or "tell me" in command:
            self.speak("I can open apps, navigate the web, and control your system. Try commands like open browser, search for something, or open notepad.")
            return False

        self.speak("I am not sure how to do that yet. Please try another command.")
        return False

    def adjust_volume(self, direction: int):
        for _ in range(3):
            self.send_volume_command(0x0a if direction > 0 else 0x09)

    def send_volume_command(self, command):
        HWND_BROADCAST = 0xFFFF
        WM_APPCOMMAND = 0x319
        ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_APPCOMMAND, 0, command << 16)

    def run(self):
        self.speak("Offline voice assistant is ready.")
        while True:
            self.listen_for_wake_word()
            command = self.listen_command()
            finished = self.process_command(command)
            if finished:
                break


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
