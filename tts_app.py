import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pyttsx3
from gtts import gTTS
import os


class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Application")

        # Text input
        self.text_input = tk.Text(root, height=10, width=50)
        self.text_input.pack(pady=10)

        # Language selection
        self.language_var = tk.StringVar()
        self.language_dropdown = ttk.Combobox(root, textvariable=self.language_var)
        self.language_dropdown['values'] = ('en', 'es', 'fr')  # Add more languages as needed
        self.language_dropdown.current(0)
        self.language_dropdown.pack(pady=5)

        # Voice selection (for pyttsx3)
        self.voice_var = tk.StringVar()
        self.voice_dropdown = ttk.Combobox(root, textvariable=self.voice_var)
        self.voice_dropdown['values'] = self.get_voices()
        self.voice_dropdown.current(0)
        self.voice_dropdown.pack(pady=5)

        # Speech rate slider
        self.rate_slider = tk.Scale(root, from_=50, to=300, label="Rate", orient=tk.HORIZONTAL)
        self.rate_slider.set(200)
        self.rate_slider.pack(pady=5)

        # Volume slider
        self.volume_slider = tk.Scale(root, from_=0.5, to=1.0, resolution=0.1, label="Volume", orient=tk.HORIZONTAL)
        self.volume_slider.set(1.0)
        self.volume_slider.pack(pady=5)

        # Buttons
        self.play_button = tk.Button(root, text="Play", command=self.play_speech)
        self.play_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save", command=self.save_speech)
        self.save_button.pack(pady=5)

    def get_voices(self):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        return [voice.name for voice in voices]

    def play_speech(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if text:
            rate = self.rate_slider.get()
            volume = self.volume_slider.get()
            voice = self.voice_dropdown.get()
            self.speak_text(text, rate, volume, voice)
        else:
            tk.messagebox.showwarning("Input Error", "Please enter some text to convert to speech.")

    def speak_text(self, text, rate, volume, voice):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        selected_voice = next((v for v in voices if v.name == voice), None)
        if selected_voice:
            engine.setProperty('voice', selected_voice.id)
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        engine.say(text)
        engine.runAndWait()

    def save_speech(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if text:
            lang = self.language_var.get()
            filename = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
            if filename:
                self.save_as_mp3(text, lang, filename)
        else:
            tk.messagebox.showwarning("Input Error", "Please enter some text to convert to speech.")

    def save_as_mp3(self, text, lang, filename):
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        tk.messagebox.showinfo("Success", f"Audio saved as {filename}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()
