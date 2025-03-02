"""from googletrans import Translator
from gtts import gTTS
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import tempfile
import os
import pyperclip  # For clipboard functionality
import speech_recognition as sr  # For voice input

# Initialize pygame for audio playback
pygame.mixer.init()

# Main application window configuration
window = Tk()
window.geometry('700x600')
window.title("Enhanced Language Translator")
window.configure(bg="#1e1e2d")  # Background color

# Title label
title_label = Label(window, text="Enhanced Language Translator", font=("Arial", 26, "bold"), bg="#1e1e2d", fg="white")
title_label.pack(pady=15)

# Entry box for text to translate
entry_frame = Frame(window, bg="#1e1e2d")
entry_frame.pack(pady=15)

e1 = Entry(entry_frame, width=50, font=("Arial", 16), bd=3, relief=FLAT)
e1.grid(row=0, column=0, padx=10)

# Dropdown for language selection
language_frame = Frame(window, bg="#1e1e2d")
language_frame.pack(pady=10)

# Add Punjabi to the list of choices
choices = ["English", "Hindi", "German", "French", "Spanish", "Russian", "Punjabi"]
click_option = StringVar()
click_option.set("Select language")

list_drop = OptionMenu(language_frame, click_option, *choices)
list_drop.configure(background="#28a745", foreground="white", font=("Arial", 12, "bold"), relief=FLAT)
list_drop.pack()

# Translated text display label
translated_text_label = Label(window, text="", bg="#1e1e2d", fg="white", font=("Arial", 14, "italic"), wraplength=500, justify="center")
translated_text_label.pack(pady=20)

# Language code dictionary
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Punjabi": "pa"
}

# Function to convert language
def convert_language():
    try:
        text_to_translate = e1.get()
        target_language = click_option.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if target_language == "Select language":
            messagebox.showwarning("Selection Error", "Please select a language.")
            return

        # Translate the text
        translator = Translator()
        target_code = language_codes.get(target_language)
        translated = translator.translate(text_to_translate, dest=target_code)
        translated_text = translated.text
        translated_text_label.config(text=translated_text)

        # Convert to speech and save as a temporary MP3 file
        speech = gTTS(text=translated_text, lang=target_code, slow=False)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_filename = temp_file.name
        temp_file.close()
        speech.save(temp_filename)

        # Stop any currently playing audio, unload, and then play new audio
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        pygame.mixer.music.unload()
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()

        def cleanup_audio_file():
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        window.bind("<<music_ended>>", lambda _: cleanup_audio_file())

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")

# Function to clear input and output fields
def clear_text():
    e1.delete(0, END)
    translated_text_label.config(text="")

# Function to copy translated text to clipboard
def copy_to_clipboard():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        pyperclip.copy(translated_text)
        messagebox.showinfo("Copy to Clipboard", "Translated text copied to clipboard.")

# Function to save translated audio as MP3 file
def save_audio():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        target_language = click_option.get()
        target_code = language_codes.get(target_language)
        speech = gTTS(text=translated_text, lang=target_code, slow=False)
        
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            speech.save(file_path)
            messagebox.showinfo("Audio Saved", f"Audio saved as {file_path}")
# Enhanced Function for voice input
def voice_input():
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Please speak the text you want to translate.")
        recognizer.adjust_for_ambient_noise(source)
        for attempt in range(3):  # Retry up to 3 times
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                e1.delete(0, END)
                e1.insert(0, text)
                break  # Exit the loop if recognition is successful
            except sr.RequestError:
                if attempt < 2:
                    messagebox.showwarning("Connection Error", "Retrying connection...")
                else:
                    messagebox.showerror("Voice Input Error", "Could not connect to the speech recognition service after several attempts.")
            except sr.UnknownValueError:
                messagebox.showerror("Voice Input Error", "Could not understand the audio.")
                break
            except Exception as e:
                messagebox.showerror("Voice Input Error", f"An unexpected error occurred: {e}")
                break

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Please speak the text you want to translate.")
        recognizer.adjust_for_ambient_noise(source)  # Handle background noise
        try:
            audio = recognizer.listen(source, timeout=5)  # Add timeout to handle silence
            text = recognizer.recognize_google(audio)
            e1.delete(0, END)
            e1.insert(0, text)
        except sr.UnknownValueError:
            messagebox.showerror("Voice Input Error", "Could not understand the audio.")
        except sr.RequestError:
            messagebox.showerror("Voice Input Error", "Could not connect to the speech recognition service.")
        except Exception as e:
            messagebox.showerror("Voice Input Error", f"An unexpected error occurred: {e}")

# Translate button
translate_button = Button(window, text="Translate", bg="#ff5733", fg="white", font=("Arial", 16, "bold"), command=convert_language, relief=FLAT, bd=0, padx=15, pady=8)
translate_button.pack(pady=10)

# Additional buttons for new functionalities
clear_button = Button(window, text="Clear Text", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=clear_text, relief=FLAT, padx=15, pady=8)
clear_button.pack(pady=5)

copy_button = Button(window, text="Copy to Clipboard", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), command=copy_to_clipboard, relief=FLAT, padx=15, pady=8)
copy_button.pack(pady=5)

save_button = Button(window, text="Save Audio", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=save_audio, relief=FLAT, padx=15, pady=8)
save_button.pack(pady=5)

voice_button = Button(window, text="Voice Input", bg="#ffc107", fg="white", font=("Arial", 12, "bold"), command=voice_input, relief=FLAT, padx=15, pady=8)
voice_button.pack(pady=5)

# Run the main application loop
window.mainloop()"""

#pragraph problem resolved
"""from googletrans import Translator
from gtts import gTTS
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import tempfile
import os
import pyperclip  # For clipboard functionality
import speech_recognition as sr  # For voice input
import textwrap

# Initialize pygame for audio playback
pygame.mixer.init()

# Main application window configuration
window = Tk()
window.geometry('700x600')
window.title("Enhanced Language Translator")
window.configure(bg="#1e1e2d")  # Background color

# Title label
title_label = Label(window, text="Enhanced Language Translator", font=("Arial", 26, "bold"), bg="#1e1e2d", fg="white")
title_label.pack(pady=15)

# Text box for paragraph input
input_text = Text(window, width=60, height=10, font=("Arial", 14), wrap=WORD, bd=3, relief=FLAT)
input_text.pack(pady=15)

# Dropdown for language selection
language_frame = Frame(window, bg="#1e1e2d")
language_frame.pack(pady=10)

# Add languages to the list of choices
choices = ["English", "Hindi", "German", "French", "Spanish", "Russian", "Punjabi"]
click_option = StringVar()
click_option.set("Select language")

list_drop = OptionMenu(language_frame, click_option, *choices)
list_drop.configure(background="#28a745", foreground="white", font=("Arial", 12, "bold"), relief=FLAT)
list_drop.pack()

# Translated text display label
translated_text_label = Label(window, text="", bg="#1e1e2d", fg="white", font=("Arial", 14, "italic"), wraplength=600, justify="center")
translated_text_label.pack(pady=20)

# Language code dictionary
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Punjabi": "pa"
}

# Function to convert language with chunking for long text
def convert_language():
    try:
        text_to_translate = input_text.get("1.0", END).strip()  # Get all text from Text widget
        target_language = click_option.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if target_language == "Select language":
            messagebox.showwarning("Selection Error", "Please select a language.")
            return

        # Translate the text
        translator = Translator()
        target_code = language_codes.get(target_language)
        translated = translator.translate(text_to_translate, dest=target_code)
        translated_text = translated.text
        translated_text_label.config(text=translated_text)

        # Break translated text into chunks to handle long inputs for gTTS
        audio_chunks = textwrap.wrap(translated_text, width=500)  # Customize chunk size as needed

        temp_files = []
        for i, chunk in enumerate(audio_chunks):
            speech = gTTS(text=chunk, lang=target_code, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_files.append(temp_file.name)
            temp_file.close()
            speech.save(temp_file.name)

        # Play the first audio chunk and queue the rest
        play_audio_chunks(temp_files)

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")

# Function to play audio chunks in sequence
def play_audio_chunks(files):
    def cleanup_files():
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    if files:
        pygame.mixer.music.load(files[0])
        pygame.mixer.music.play()
        files.pop(0)  # Remove the first item since it is being played

        def play_next_chunk():
            if files:
                pygame.mixer.music.load(files[0])
                pygame.mixer.music.play()
                files.pop(0)
            else:
                cleanup_files()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        window.bind("<<music_ended>>", lambda _: play_next_chunk())

# Function to clear input and output fields
def clear_text():
    input_text.delete("1.0", END)
    translated_text_label.config(text="")

# Function to copy translated text to clipboard
def copy_to_clipboard():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        pyperclip.copy(translated_text)
        messagebox.showinfo("Copy to Clipboard", "Translated text copied to clipboard.")

# Function to save translated audio as MP3 file
def save_audio():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        target_language = click_option.get()
        target_code = language_codes.get(target_language)
        
        audio_chunks = textwrap.wrap(translated_text, width=500)
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:
            with open(file_path, "wb") as f:
                for chunk in audio_chunks:
                    speech = gTTS(text=chunk, lang=target_code, slow=False)
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    temp_file.close()
                    speech.save(temp_file.name)
                    with open(temp_file.name, "rb") as tf:
                        f.write(tf.read())
                    os.remove(temp_file.name)
            messagebox.showinfo("Audio Saved", f"Audio saved as {file_path}")

# Function for voice input with retries
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Please speak the text you want to translate.")
        recognizer.adjust_for_ambient_noise(source)
        for attempt in range(3):  # Retry up to 3 times
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                input_text.delete("1.0", END)
                input_text.insert("1.0", text)
                break
            except sr.RequestError:
                if attempt < 2:
                    messagebox.showwarning("Connection Error", "Retrying connection...")
                else:
                    messagebox.showerror("Voice Input Error", "Could not connect to the speech recognition service.")
            except sr.UnknownValueError:
                messagebox.showerror("Voice Input Error", "Could not understand the audio.")
                break

# Buttons
translate_button = Button(window, text="Translate", bg="#ff5733", fg="white", font=("Arial", 16, "bold"), command=convert_language, relief=FLAT, bd=0, padx=15, pady=8)
translate_button.pack(pady=10)

clear_button = Button(window, text="Clear Text", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=clear_text, relief=FLAT, padx=15, pady=8)
clear_button.pack(pady=5)

copy_button = Button(window, text="Copy to Clipboard", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), command=copy_to_clipboard, relief=FLAT, padx=15, pady=8)
copy_button.pack(pady=5)

save_button = Button(window, text="Save Audio", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=save_audio, relief=FLAT, padx=15, pady=8)
save_button.pack(pady=5)

voice_button = Button(window, text="Voice Input", bg="#ffc107", fg="white", font=("Arial", 12, "bold"), command=voice_input, relief=FLAT, padx=15, pady=8)
voice_button.pack(pady=5)

# Run the main application loop
window.mainloop()"""

#scroll bar added to input box
"""from googletrans import Translator
from gtts import gTTS
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import tempfile
import os
import pyperclip  # For clipboard functionality
import speech_recognition as sr  # For voice input
import textwrap

# Initialize pygame for audio playback
pygame.mixer.init()

# Main application window configuration
window = Tk()
window.geometry('800x700')  # Increased window size for better layout
window.title("Enhanced Language Translator")
window.configure(bg="#1e1e2d")  # Background color

# Title label
title_label = Label(window, text="Enhanced Language Translator", font=("Arial", 26, "bold"), bg="#1e1e2d", fg="white")
title_label.pack(pady=15)

# Frame for input text box with scrollbar
input_frame = Frame(window, bg="#1e1e2d")
input_frame.pack(pady=15)

# Input text box for paragraph input with enhanced size and styling
input_text = Text(input_frame, width=70, height=12, font=("Arial", 14), wrap=WORD, bd=3, relief=SOLID, fg="black", bg="#f0f0f0")
input_text.grid(row=0, column=0, padx=10, pady=5)

# Adding vertical scrollbar to the input text box
scrollbar = Scrollbar(input_frame, command=input_text.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
input_text.config(yscrollcommand=scrollbar.set)

# Dropdown for language selection
language_frame = Frame(window, bg="#1e1e2d")
language_frame.pack(pady=10)

# Add languages to the list of choices
choices = ["English", "Hindi", "German", "French", "Spanish", "Russian", "Punjabi"]
click_option = StringVar()
click_option.set("Select language")

list_drop = OptionMenu(language_frame, click_option, *choices)
list_drop.configure(background="#28a745", foreground="white", font=("Arial", 12, "bold"), relief=FLAT)
list_drop.pack()

# Translated text display label
translated_text_label = Label(window, text="", bg="#1e1e2d", fg="white", font=("Arial", 14, "italic"), wraplength=700, justify="center")
translated_text_label.pack(pady=20)

# Language code dictionary
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Punjabi": "pa"
}

# Function to convert language with chunking for long text
def convert_language():
    try:
        text_to_translate = input_text.get("1.0", END).strip()  # Get all text from Text widget
        target_language = click_option.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if target_language == "Select language":
            messagebox.showwarning("Selection Error", "Please select a language.")
            return

        # Translate the text
        translator = Translator()
        target_code = language_codes.get(target_language)
        translated = translator.translate(text_to_translate, dest=target_code)
        translated_text = translated.text
        translated_text_label.config(text=translated_text)

        # Break translated text into chunks to handle long inputs for gTTS
        audio_chunks = textwrap.wrap(translated_text, width=500)  # Customize chunk size as needed

        temp_files = []
        for i, chunk in enumerate(audio_chunks):
            speech = gTTS(text=chunk, lang=target_code, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_files.append(temp_file.name)
            temp_file.close()
            speech.save(temp_file.name)

        # Play the first audio chunk and queue the rest
        play_audio_chunks(temp_files)

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")

# Function to play audio chunks in sequence
def play_audio_chunks(files):
    def cleanup_files():
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    if files:
        pygame.mixer.music.load(files[0])
        pygame.mixer.music.play()
        files.pop(0)  # Remove the first item since it is being played

        def play_next_chunk():
            if files:
                pygame.mixer.music.load(files[0])
                pygame.mixer.music.play()
                files.pop(0)
            else:
                cleanup_files()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        window.bind("<<music_ended>>", lambda _: play_next_chunk())

# Function to clear input and output fields
def clear_text():
    input_text.delete("1.0", END)
    translated_text_label.config(text="")

# Function to copy translated text to clipboard
def copy_to_clipboard():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        pyperclip.copy(translated_text)
        messagebox.showinfo("Copy to Clipboard", "Translated text copied to clipboard.")

# Function to save translated audio as MP3 file
def save_audio():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        target_language = click_option.get()
        target_code = language_codes.get(target_language)
        
        audio_chunks = textwrap.wrap(translated_text, width=500)
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:
            with open(file_path, "wb") as f:
                for chunk in audio_chunks:
                    speech = gTTS(text=chunk, lang=target_code, slow=False)
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    temp_file.close()
                    speech.save(temp_file.name)
                    with open(temp_file.name, "rb") as tf:
                        f.write(tf.read())
                    os.remove(temp_file.name)
            messagebox.showinfo("Audio Saved", f"Audio saved as {file_path}")

# Function for voice input with retries
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Please speak the text you want to translate.")
        recognizer.adjust_for_ambient_noise(source)
        for attempt in range(3):  # Retry up to 3 times
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                input_text.delete("1.0", END)
                input_text.insert("1.0", text)
                break
            except sr.RequestError:
                if attempt < 2:
                    messagebox.showwarning("Connection Error", "Retrying connection...")
                else:
                    messagebox.showerror("Voice Input Error", "Could not connect to the speech recognition service.")
            except sr.UnknownValueError:
                messagebox.showerror("Voice Input Error", "Could not understand the audio.")
                break

# Buttons
translate_button = Button(window, text="Translate", bg="#ff5733", fg="white", font=("Arial", 16, "bold"), command=convert_language, relief=FLAT, bd=0, padx=15, pady=8)
translate_button.pack(pady=10)

clear_button = Button(window, text="Clear Text", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=clear_text, relief=FLAT, padx=15, pady=8)
clear_button.pack(pady=5)

copy_button = Button(window, text="Copy to Clipboard", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), command=copy_to_clipboard, relief=FLAT, padx=15, pady=8)
copy_button.pack(pady=5)

save_button = Button(window, text="Save Audio", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=save_audio, relief=FLAT, padx=15, pady=8)
save_button.pack(pady=5)

voice_button = Button(window, text="Voice Input", bg="#ffc107", fg="white", font=("Arial", 12, "bold"), command=voice_input, relief=FLAT, padx=15, pady=8)
voice_button.pack(pady=5)

# Run the main application loop
window.mainloop()"""


"""from googletrans import Translator
from gtts import gTTS
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import tempfile
import os
import pyperclip  # For clipboard functionality
import speech_recognition as sr  # For voice input
import textwrap

# Initialize pygame for audio playback
pygame.mixer.init()

# Main application window configuration
window = Tk()
window.geometry('700x600')
window.title("Enhanced Language Translator")
window.configure(bg="#1e1e2d")  # Background color

# Title label
title_label = Label(window, text="Enhanced Language Translator", font=("Arial", 26, "bold"), bg="#1e1e2d", fg="white")
title_label.pack(pady=15)

# Text box for paragraph input
input_text = Text(window, width=60, height=10, font=("Arial", 14), wrap=WORD, bd=3, relief=FLAT)
input_text.pack(pady=15)

# Dropdown for language selection
language_frame = Frame(window, bg="#1e1e2d")
language_frame.pack(pady=10)

# Add languages to the list of choices
choices = ["English", "Hindi", "German", "French", "Spanish", "Russian", "Punjabi"]
click_option = StringVar()
click_option.set("Select language")

list_drop = OptionMenu(language_frame, click_option, *choices)
list_drop.configure(background="#28a745", foreground="white", font=("Arial", 12, "bold"), relief=FLAT)
list_drop.pack()

# Translated text display label
translated_text_label = Label(window, text="", bg="#1e1e2d", fg="white", font=("Arial", 14, "italic"), wraplength=600, justify="center")
translated_text_label.pack(pady=20)

# Language code dictionary
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Punjabi": "pa"
}

# Function to convert language with chunking for long text
def convert_language():
    try:
        text_to_translate = input_text.get("1.0", END).strip()  # Get all text from Text widget
        target_language = click_option.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if target_language == "Select language":
            messagebox.showwarning("Selection Error", "Please select a language.")
            return

        # Translate the text
        translator = Translator()
        target_code = language_codes.get(target_language)
        translated = translator.translate(text_to_translate, dest=target_code)
        translated_text = translated.text
        translated_text_label.config(text=translated_text)

        # Break translated text into chunks to handle long inputs for gTTS
        audio_chunks = textwrap.wrap(translated_text, width=500)  # Customize chunk size as needed

        temp_files = []
        for i, chunk in enumerate(audio_chunks):
            speech = gTTS(text=chunk, lang=target_code, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_files.append(temp_file.name)
            temp_file.close()
            speech.save(temp_file.name)

        # Play the first audio chunk and queue the rest
        play_audio_chunks(temp_files)

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")

# Function to play audio chunks in sequence
def play_audio_chunks(files):
    def cleanup_files():
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    if files:
        pygame.mixer.music.load(files[0])
        pygame.mixer.music.play()
        files.pop(0)  # Remove the first item since it is being played

        def play_next_chunk():
            if files:
                pygame.mixer.music.load(files[0])
                pygame.mixer.music.play()
                files.pop(0)
            else:
                cleanup_files()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        window.bind("<<music_ended>>", lambda _: play_next_chunk())

# Function to clear input and output fields
def clear_text():
    input_text.delete("1.0", END)
    translated_text_label.config(text="")

# Function to copy translated text to clipboard
def copy_to_clipboard():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        pyperclip.copy(translated_text)
        messagebox.showinfo("Copy to Clipboard", "Translated text copied to clipboard.")

# Function to save translated audio as MP3 file
def save_audio():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        target_language = click_option.get()
        target_code = language_codes.get(target_language)
        
        audio_chunks = textwrap.wrap(translated_text, width=500)
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:
            with open(file_path, "wb") as f:
                for chunk in audio_chunks:
                    speech = gTTS(text=chunk, lang=target_code, slow=False)
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    temp_file.close()
                    speech.save(temp_file.name)
                    with open(temp_file.name, "rb") as tf:
                        f.write(tf.read())
                    os.remove(temp_file.name)
            messagebox.showinfo("Audio Saved", f"Audio saved as {file_path}")

# Function for voice input with retries
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Please speak the text you want to translate.")
        recognizer.adjust_for_ambient_noise(source)
        for attempt in range(3):  # Retry up to 3 times
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                input_text.delete("1.0", END)
                input_text.insert("1.0", text)
                break
            except sr.RequestError:
                if attempt < 2:
                    messagebox.showwarning("Connection Error", "Retrying connection...")
                else:
                    messagebox.showerror("Voice Input Error", "Could not connect to the speech recognition service.")
            except sr.UnknownValueError:
                messagebox.showerror("Voice Input Error", "Could not understand the audio.")
                break

# Buttons
translate_button = Button(window, text="Translate", bg="#ff5733", fg="white", font=("Arial", 16, "bold"), command=convert_language, relief=FLAT, bd=0, padx=15, pady=8)
translate_button.pack(pady=10)

clear_button = Button(window, text="Clear Text", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=clear_text, relief=FLAT, padx=15, pady=8)
clear_button.pack(pady=5)

copy_button = Button(window, text="Copy to Clipboard", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), command=copy_to_clipboard, relief=FLAT, padx=15, pady=8)
copy_button.pack(pady=5)

save_button = Button(window, text="Save Audio", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=save_audio, relief=FLAT, padx=15, pady=8)
save_button.pack(pady=5)

voice_button = Button(window, text="Voice Input", bg="#ffc107", fg="white", font=("Arial", 12, "bold"), command=voice_input, relief=FLAT, padx=15, pady=8)
voice_button.pack(pady=5)

# Run the main application loop
window.mainloop()"""

"""from googletrans import Translator
from gtts import gTTS
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import tempfile
import os
import pyperclip  # For clipboard functionality
import speech_recognition as sr  # For voice input
import textwrap

# Initialize pygame for audio playback
pygame.mixer.init()

# Main application window configuration
window = Tk()
window.geometry('700x600')
window.title("Enhanced Language Translator")
window.configure(bg="#1e1e2d")  # Background color

# Title label
title_label = Label(window, text="Enhanced Language Translator", font=("Arial", 26, "bold"), bg="#1e1e2d", fg="white")
title_label.pack(pady=15)

# Function to adjust the text box height dynamically
def adjust_textbox_height(event=None):
    line_count = int(input_text.index("end-1c").split('.')[0])  # Get current line count
    input_text.configure(height=max(5, line_count))  # Set minimum height to 5

# Text box for paragraph input (initially small height, auto-expands)
input_text = Text(window, width=60, height=5, font=("Arial", 14), wrap=WORD, bd=3, relief=FLAT)
input_text.pack(pady=15)
input_text.bind("<KeyRelease>", adjust_textbox_height)  # Adjust height as text changes

# Dropdown for language selection
language_frame = Frame(window, bg="#1e1e2d")
language_frame.pack(pady=10)

# Add languages to the list of choices
choices = ["English", "Hindi", "German", "French", "Spanish", "Russian", "Punjabi"]
click_option = StringVar()
click_option.set("Select language")

list_drop = OptionMenu(language_frame, click_option, *choices)
list_drop.configure(background="#28a745", foreground="white", font=("Arial", 12, "bold"), relief=FLAT)
list_drop.pack()

# Translated text display label
translated_text_label = Label(window, text="", bg="#1e1e2d", fg="white", font=("Arial", 14, "italic"), wraplength=600, justify="center")
translated_text_label.pack(pady=20)

# Language code dictionary
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Punjabi": "pa"
}

# Function to convert language with chunking for long text
def convert_language():
    try:
        text_to_translate = input_text.get("1.0", END).strip()  # Get all text from Text widget
        target_language = click_option.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if target_language == "Select language":
            messagebox.showwarning("Selection Error", "Please select a language.")
            return

        # Translate the text
        translator = Translator()
        target_code = language_codes.get(target_language)
        translated = translator.translate(text_to_translate, dest=target_code)
        translated_text = translated.text
        translated_text_label.config(text=translated_text)

        # Break translated text into chunks to handle long inputs for gTTS
        audio_chunks = textwrap.wrap(translated_text, width=500)  # Customize chunk size as needed

        temp_files = []
        for i, chunk in enumerate(audio_chunks):
            speech = gTTS(text=chunk, lang=target_code, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_files.append(temp_file.name)
            temp_file.close()
            speech.save(temp_file.name)

        # Play the first audio chunk and queue the rest
        play_audio_chunks(temp_files)

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")

# Function to play audio chunks in sequence
def play_audio_chunks(files):
    def cleanup_files():
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    if files:
        pygame.mixer.music.load(files[0])
        pygame.mixer.music.play()
        files.pop(0)  # Remove the first item since it is being played

        def play_next_chunk():
            if files:
                pygame.mixer.music.load(files[0])
                pygame.mixer.music.play()
                files.pop(0)
            else:
                cleanup_files()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        window.bind("<<music_ended>>", lambda _: play_next_chunk())

# Function to clear input and output fields
def clear_text():
    input_text.delete("1.0", END)
    translated_text_label.config(text="")
    adjust_textbox_height()  # Reset textbox height after clearing

# Function to copy translated text to clipboard
def copy_to_clipboard():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        pyperclip.copy(translated_text)
        messagebox.showinfo("Copy to Clipboard", "Translated text copied to clipboard.")

# Function to save translated audio as MP3 file
def save_audio():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        target_language = click_option.get()
        target_code = language_codes.get(target_language)
        
        audio_chunks = textwrap.wrap(translated_text, width=500)
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:
            with open(file_path, "wb") as f:
                for chunk in audio_chunks:
                    speech = gTTS(text=chunk, lang=target_code, slow=False)
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    temp_file.close()
                    speech.save(temp_file.name)
                    with open(temp_file.name, "rb") as tf:
                        f.write(tf.read())
                    os.remove(temp_file.name)
            messagebox.showinfo("Audio Saved", f"Audio saved as {file_path}")

# Function for voice input with retries
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Please speak the text you want to translate.")
        recognizer.adjust_for_ambient_noise(source)
        for attempt in range(3):  # Retry up to 3 times
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                input_text.delete("1.0", END)
                input_text.insert("1.0", text)
                break
            except sr.RequestError:
                if attempt < 2:
                    messagebox.showwarning("Connection Error", "Retrying connection...")
                else:
                    messagebox.showerror("Voice Input Error", "Could not connect to the speech recognition service.")
            except sr.UnknownValueError:
                messagebox.showerror("Voice Input Error", "Could not understand the audio.")
                break

# Buttons
translate_button = Button(window, text="Translate", bg="#ff5733", fg="white", font=("Arial", 16, "bold"), command=convert_language, relief=FLAT, bd=0, padx=15, pady=8)
translate_button.pack(pady=10)

clear_button = Button(window, text="Clear Text", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=clear_text, relief=FLAT, padx=15, pady=8)
clear_button.pack(pady=5)

copy_button = Button(window, text="Copy to Clipboard", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), command=copy_to_clipboard, relief=FLAT, padx=15, pady=8)
copy_button.pack(pady=5)

save_button = Button(window, text="Save Audio", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=save_audio, relief=FLAT, padx=15, pady=8)
save_button.pack(pady=5)

voice_button = Button(window, text="Voice Input", bg="#ffc107", fg="white", font=("Arial", 12, "bold"), command=voice_input, relief=FLAT, padx=15, pady=8)
voice_button.pack(pady=5)

# Run the main application loop
window.mainloop()"""

#the buttons appears horizontally
"""from googletrans import Translator
from gtts import gTTS
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import tempfile
import os
import pyperclip  # For clipboard functionality
import speech_recognition as sr  # For voice input
import textwrap

# Initialize pygame for audio playback
pygame.mixer.init()

# Main application window configuration
window = Tk()
window.geometry('700x600')
window.title("Enhanced Language Translator")
window.configure(bg="#1e1e2d")  # Background color

# Title label
title_label = Label(window, text="Enhanced Language Translator", font=("Arial", 26, "bold"), bg="#1e1e2d", fg="white")
title_label.grid(row=0, column=0, columnspan=2, pady=15)

# Function to adjust the text box height dynamically
def adjust_textbox_height(event=None):
    line_count = int(input_text.index("end-1c").split('.')[0])  # Get current line count
    input_text.configure(height=max(5, line_count))  # Set minimum height to 5

# Text box for paragraph input (initially small height, auto-expands)
input_text = Text(window, width=60, height=5, font=("Arial", 14), wrap=WORD, bd=3, relief=FLAT)
input_text.grid(row=1, column=0, columnspan=2, pady=15)
input_text.bind("<KeyRelease>", adjust_textbox_height)  # Adjust height as text changes

# Dropdown for language selection
language_frame = Frame(window, bg="#1e1e2d")
language_frame.grid(row=2, column=0, columnspan=2, pady=10)

# Add languages to the list of choices
choices = ["English", "Hindi", "German", "French", "Spanish", "Russian", "Punjabi"]
click_option = StringVar()
click_option.set("Select language")

list_drop = OptionMenu(language_frame, click_option, *choices)
list_drop.configure(background="#28a745", foreground="white", font=("Arial", 12, "bold"), relief=FLAT)
list_drop.grid(row=0, column=0, padx=10)

# Translated text display label
translated_text_label = Label(window, text="", bg="#1e1e2d", fg="white", font=("Arial", 14, "italic"), wraplength=600, justify="center")
translated_text_label.grid(row=3, column=0, columnspan=2, pady=20)

# Language code dictionary
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Punjabi": "pa"
}

# Function to convert language with chunking for long text
def convert_language():
    try:
        text_to_translate = input_text.get("1.0", END).strip()  # Get all text from Text widget
        target_language = click_option.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if target_language == "Select language":
            messagebox.showwarning("Selection Error", "Please select a language.")
            return

        # Translate the text
        translator = Translator()
        target_code = language_codes.get(target_language)
        translated = translator.translate(text_to_translate, dest=target_code)
        translated_text = translated.text
        translated_text_label.config(text=translated_text)

        # Break translated text into chunks to handle long inputs for gTTS
        audio_chunks = textwrap.wrap(translated_text, width=500)  # Customize chunk size as needed

        temp_files = []
        for i, chunk in enumerate(audio_chunks):
            speech = gTTS(text=chunk, lang=target_code, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_files.append(temp_file.name)
            temp_file.close()
            speech.save(temp_file.name)

        # Play the first audio chunk and queue the rest
        play_audio_chunks(temp_files)

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")

# Function to play audio chunks in sequence
def play_audio_chunks(files):
    def cleanup_files():
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    if files:
        pygame.mixer.music.load(files[0])
        pygame.mixer.music.play()
        files.pop(0)  # Remove the first item since it is being played

        def play_next_chunk():
            if files:
                pygame.mixer.music.load(files[0])
                pygame.mixer.music.play()
                files.pop(0)
            else:
                cleanup_files()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        window.bind("<<music_ended>>", lambda _: play_next_chunk())

# Function to clear input and output fields
def clear_text():
    input_text.delete("1.0", END)
    translated_text_label.config(text="")
    adjust_textbox_height()  # Reset textbox height after clearing

# Function to copy translated text to clipboard
def copy_to_clipboard():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        pyperclip.copy(translated_text)
        messagebox.showinfo("Copy to Clipboard", "Translated text copied to clipboard.")

# Function to save translated audio as MP3 file
def save_audio():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        target_language = click_option.get()
        target_code = language_codes.get(target_language)
        
        audio_chunks = textwrap.wrap(translated_text, width=500)
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:
            with open(file_path, "wb") as f:
                for chunk in audio_chunks:
                    speech = gTTS(text=chunk, lang=target_code, slow=False)
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    temp_file.close()
                    speech.save(temp_file.name)
                    with open(temp_file.name, "rb") as tf:
                        f.write(tf.read())
                    os.remove(temp_file.name)
            messagebox.showinfo("Audio Saved", f"Audio saved as {file_path}")

# Function for voice input with retries
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Please speak the text you want to translate.")
        recognizer.adjust_for_ambient_noise(source)
        for attempt in range(3):  # Retry up to 3 times
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                input_text.delete("1.0", END)
                input_text.insert("1.0", text)
                break
            except sr.RequestError:
                if attempt < 2:
                    messagebox.showwarning("Connection Error", "Retrying connection...")
                else:
                    messagebox.showerror("Voice Input Error", "Could not connect to the speech recognition service.")
            except sr.UnknownValueError:
                messagebox.showerror("Voice Input Error", "Could not understand the audio.")
                break

# Button layout
button_frame = Frame(window, bg="#1e1e2d")
button_frame.grid(row=4, column=0, columnspan=2, pady=10)

# Buttons
translate_button = Button(button_frame, text="Translate", bg="#ff5733", fg="white", font=("Arial", 16, "bold"), command=convert_language, relief=FLAT, bd=0, padx=15, pady=8)
translate_button.grid(row=0, column=0, padx=10)

clear_button = Button(button_frame, text="Clear Text", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=clear_text, relief=FLAT, padx=15, pady=8)
clear_button.grid(row=0, column=1, padx=10)

copy_button = Button(button_frame, text="Copy to Clipboard", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), command=copy_to_clipboard, relief=FLAT, padx=15, pady=8)
copy_button.grid(row=0, column=2, padx=10)

save_button = Button(button_frame, text="Save Audio", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=save_audio, relief=FLAT, padx=15, pady=8)
save_button.grid(row=0, column=3, padx=10)

voice_button = Button(button_frame, text="Voice Input", bg="#ffc107", fg="white", font=("Arial", 12, "bold"), command=voice_input, relief=FLAT, padx=15, pady=8)
voice_button.grid(row=0, column=4, padx=10)

# Run the main application loop
window.mainloop()"""


"""from googletrans import Translator
from gtts import gTTS
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import tempfile
import os
import pyperclip  # For clipboard functionality
import speech_recognition as sr  # For voice input
import textwrap

# Initialize pygame for audio playback
pygame.mixer.init()

# Main application window configuration
window = Tk()
window.geometry('700x600')
window.title("Enhanced Language Translator")
window.configure(bg="#1e1e2d")  # Background color

# Title label
title_label = Label(window, text="Enhanced Language Translator", font=("Arial", 26, "bold"), bg="#1e1e2d", fg="white")
title_label.pack(pady=15)

# Text box for paragraph input
input_text = Text(window, width=60, height=10, font=("Arial", 14), wrap=WORD, bd=3, relief=FLAT)
input_text.pack(pady=15)

# Dropdown for language selection
language_frame = Frame(window, bg="#1e1e2d")
language_frame.pack(pady=10)

# Add languages to the list of choices
choices = ["English", "Hindi", "German", "French", "Spanish", "Russian", "Punjabi"]
click_option = StringVar()
click_option.set("Select language")

list_drop = OptionMenu(language_frame, click_option, *choices)
list_drop.configure(background="#28a745", foreground="white", font=("Arial", 12, "bold"), relief=FLAT)
list_drop.pack()

# Translated text display label
translated_text_label = Label(window, text="", bg="#1e1e2d", fg="white", font=("Arial", 14, "italic"), wraplength=600, justify="center")
translated_text_label.pack(pady=20)

# Language code dictionary
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Punjabi": "pa"
}

# Function to convert language with chunking for long text
def convert_language():
    try:
        text_to_translate = input_text.get("1.0", END).strip()  # Get all text from Text widget
        target_language = click_option.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if target_language == "Select language":
            messagebox.showwarning("Selection Error", "Please select a language.")
            return

        # Translate the text
        translator = Translator()
        target_code = language_codes.get(target_language)
        translated = translator.translate(text_to_translate, dest=target_code)
        translated_text = translated.text
        translated_text_label.config(text=translated_text)

        # Break translated text into chunks to handle long inputs for gTTS
        audio_chunks = textwrap.wrap(translated_text, width=500)  # Customize chunk size as needed

        temp_files = []
        for i, chunk in enumerate(audio_chunks):
            speech = gTTS(text=chunk, lang=target_code, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_files.append(temp_file.name)
            temp_file.close()
            speech.save(temp_file.name)

        # Play the first audio chunk and queue the rest
        play_audio_chunks(temp_files)

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")

# Function to play audio chunks in sequence
def play_audio_chunks(files):
    def cleanup_files():
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    if files:
        pygame.mixer.music.load(files[0])
        pygame.mixer.music.play()
        files.pop(0)  # Remove the first item since it is being played

        def play_next_chunk():
            if files:
                pygame.mixer.music.load(files[0])
                pygame.mixer.music.play()
                files.pop(0)
            else:
                cleanup_files()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        window.bind("<<music_ended>>", lambda _: play_next_chunk())

# Function to clear input and output fields
def clear_text():
    input_text.delete("1.0", END)
    translated_text_label.config(text="")

# Function to copy translated text to clipboard
def copy_to_clipboard():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        pyperclip.copy(translated_text)
        messagebox.showinfo("Copy to Clipboard", "Translated text copied to clipboard.")

# Function to save translated audio as MP3 file
def save_audio():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        target_language = click_option.get()
        target_code = language_codes.get(target_language)
        
        audio_chunks = textwrap.wrap(translated_text, width=500)
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:
            with open(file_path, "wb") as f:
                for chunk in audio_chunks:
                    speech = gTTS(text=chunk, lang=target_code, slow=False)
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    temp_file.close()
                    speech.save(temp_file.name)
                    with open(temp_file.name, "rb") as tf:
                        f.write(tf.read())
                    os.remove(temp_file.name)
            messagebox.showinfo("Audio Saved", f"Audio saved as {file_path}")

# Function for voice input with retries
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Please speak the text you want to translate.")
        recognizer.adjust_for_ambient_noise(source)
        for attempt in range(3):  # Retry up to 3 times
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                input_text.delete("1.0", END)
                input_text.insert("1.0", text)
                break
            except sr.RequestError:
                if attempt < 2:
                    messagebox.showwarning("Connection Error", "Retrying connection...")
                else:
                    messagebox.showerror("Voice Input Error", "Could not connect to the speech recognition service.")
            except sr.UnknownValueError:
                messagebox.showerror("Voice Input Error", "Could not understand the audio.")
                break

# Buttons
translate_button = Button(window, text="Translate", bg="#ff5733", fg="white", font=("Arial", 16, "bold"), command=convert_language, relief=FLAT, bd=0, padx=15, pady=8)
translate_button.pack(pady=10)

clear_button = Button(window, text="Clear Text", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=clear_text, relief=FLAT, padx=15, pady=8)
clear_button.pack(pady=5)

copy_button = Button(window, text="Copy to Clipboard", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), command=copy_to_clipboard, relief=FLAT, padx=15, pady=8)
copy_button.pack(pady=5)

save_button = Button(window, text="Save Audio", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=save_audio, relief=FLAT, padx=15, pady=8)
save_button.pack(pady=5)

voice_button = Button(window, text="Voice Input", bg="#ffc107", fg="white", font=("Arial", 12, "bold"), command=voice_input, relief=FLAT, padx=15, pady=8)
voice_button.pack(pady=5)

# Run the main application loop
window.mainloop()"""
#translation history added
"""from googletrans import Translator
from gtts import gTTS
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import tempfile
import os
import pyperclip  # For clipboard functionality
import speech_recognition as sr  # For voice input
import textwrap

# Initialize pygame for audio playback
pygame.mixer.init()

# Main application window configuration
window = Tk()
window.geometry('950x500')  # Adjusted width for right-side history
window.title("Enhanced Language Translator")
window.configure(bg="#1e1e2d")  # Background color

# Set up grid configuration for main window
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=0)

# Title label
title_label = Label(window, text="Enhanced Language Translator", font=("Arial", 24, "bold"), bg="#1e1e2d", fg="white")
title_label.grid(row=0, column=0, columnspan=2, pady=15, sticky=W)

# Text box for paragraph input
input_text = Text(window, width=50, height=8, font=("Arial", 14), wrap=WORD, bd=3, relief=FLAT)
input_text.grid(row=1, column=0, padx=20, pady=10, sticky=W)

# Dropdown for language selection
language_frame = Frame(window, bg="#1e1e2d")
language_frame.grid(row=2, column=0, pady=10, padx=20, sticky=W)

# Add languages to the list of choices
choices = ["English", "Hindi", "German", "French", "Spanish", "Russian", "Punjabi"]
click_option = StringVar()
click_option.set("Select language")

list_drop = OptionMenu(language_frame, click_option, *choices)
list_drop.configure(background="#28a745", foreground="white", font=("Arial", 12, "bold"), relief=FLAT)
list_drop.pack()

# Translated text display label
translated_text_label = Label(window, text="", bg="#1e1e2d", fg="white", font=("Arial", 14, "italic"), wraplength=400, justify="center")
translated_text_label.grid(row=3, column=0, padx=20, pady=20, sticky=W)

# Language code dictionary
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Punjabi": "pa"
}

# Translation history panel setup on the right side
history_label = Label(window, text="Translation History", font=("Arial", 14, "bold"), bg="#1e1e2d", fg="white")
history_label.grid(row=0, column=1, padx=20, pady=10, sticky=N)

history_frame = Frame(window, bg="#1e1e2d")
history_frame.grid(row=1, column=1, rowspan=4, padx=20, pady=10, sticky=NS)

history_text = Text(history_frame, wrap=WORD, font=("Arial", 12), bg="#33334d", fg="white", state=DISABLED, width=30, height=20)
history_text.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(history_frame, command=history_text.yview)
scrollbar.pack(side=RIGHT, fill=Y)
history_text.config(yscrollcommand=scrollbar.set)

# Function to add text to the history panel
def add_to_history(input_text, translated_text):
    history_text.config(state=NORMAL)
    history_text.insert(END, f"Input: {input_text}\nOutput: {translated_text}\n{'-'*50}\n")
    history_text.config(state=DISABLED)
    history_text.see(END)  # Auto-scroll to the latest entry

# Function to convert language with chunking for long text
def convert_language():
    try:
        text_to_translate = input_text.get("1.0", END).strip()  # Get all text from Text widget
        target_language = click_option.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if target_language == "Select language":
            messagebox.showwarning("Selection Error", "Please select a language.")
            return

        # Translate the text
        translator = Translator()
        target_code = language_codes.get(target_language)
        translated = translator.translate(text_to_translate, dest=target_code)
        translated_text = translated.text
        translated_text_label.config(text=translated_text)

        # Add translation to history
        add_to_history(text_to_translate, translated_text)

        # Break translated text into chunks to handle long inputs for gTTS
        audio_chunks = textwrap.wrap(translated_text, width=500)  # Customize chunk size as needed

        temp_files = []
        for i, chunk in enumerate(audio_chunks):
            speech = gTTS(text=chunk, lang=target_code, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_files.append(temp_file.name)
            temp_file.close()
            speech.save(temp_file.name)

        # Play the first audio chunk and queue the rest
        play_audio_chunks(temp_files)

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")

# Function to play audio chunks in sequence
def play_audio_chunks(files):
    def cleanup_files():
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    if files:
        pygame.mixer.music.load(files[0])
        pygame.mixer.music.play()
        files.pop(0)  # Remove the first item since it is being played

        def play_next_chunk():
            if files:
                pygame.mixer.music.load(files[0])
                pygame.mixer.music.play()
                files.pop(0)
            else:
                cleanup_files()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        window.bind("<<music_ended>>", lambda _: play_next_chunk())

# Function to clear input and output fields
def clear_text():
    input_text.delete("1.0", END)
    translated_text_label.config(text="")

# Function to copy translated text to clipboard
def copy_to_clipboard():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        pyperclip.copy(translated_text)
        messagebox.showinfo("Copy to Clipboard", "Translated text copied to clipboard.")

# Function to save translated audio as MP3 file
def save_audio():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        target_language = click_option.get()
        target_code = language_codes.get(target_language)
        
        audio_chunks = textwrap.wrap(translated_text, width=500)
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:
            with open(file_path, "wb") as f:
                for chunk in audio_chunks:
                    speech = gTTS(text=chunk, lang=target_code, slow=False)
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    temp_file.close()
                    speech.save(temp_file.name)
                    with open(temp_file.name, "rb") as tf:
                        f.write(tf.read())
                    os.remove(temp_file.name)
            messagebox.showinfo("Audio Saved", f"Audio saved as {file_path}")

# Function for voice input with retries
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Please speak the text you want to translate.")
        recognizer.adjust_for_ambient_noise(source)
        for attempt in range(3):  # Retry up to 3 times
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                input_text.delete("1.0", END)
                input_text.insert("1.0", text)
                break
            except sr.RequestError:
                if attempt < 2:
                    messagebox.showwarning("Connection Error", "Retrying connection...")
                else:
                    messagebox.showerror("Voice Input Error", "Could not connect to the speech recognition service.")
            except sr.UnknownValueError:
                messagebox.showerror("Voice Input Error", "Could not understand the audio.")
                break

# Buttons
translate_button = Button(window, text="Translate", bg="#ff5733", fg="white", font=("Arial", 16, "bold"), command=convert_language, relief=FLAT, bd=0, padx=15, pady=8)
translate_button.grid(row=4, column=0, pady=10, padx=20, sticky=W)

clear_button = Button(window, text="Clear Text", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=clear_text, relief=FLAT, padx=15, pady=8)
clear_button.grid(row=5, column=0, pady=5, padx=20, sticky=W)

copy_button = Button(window, text="Copy to Clipboard", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), command=copy_to_clipboard, relief=FLAT, padx=15, pady=8)
copy_button.grid(row=6, column=0, pady=5, padx=20, sticky=W)

save_button = Button(window, text="Save Audio", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=save_audio, relief=FLAT, padx=15, pady=8)
save_button.grid(row=7, column=0, pady=5, padx=20, sticky=W)

voice_button = Button(window, text="Voice Input", bg="#ffc107", fg="white", font=("Arial", 12, "bold"), command=voice_input, relief=FLAT, padx=15, pady=8)
voice_button.grid(row=8, column=0, pady=5, padx=20, sticky=W)

# Run the main application loop
window.mainloop()"""

"""from googletrans import Translator
from gtts import gTTS
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import tempfile
import os
import pyperclip  # For clipboard functionality
import speech_recognition as sr  # For voice input
import textwrap

# Initialize pygame for audio playback
pygame.mixer.init()

# Main application window configuration
window = Tk()
window.geometry('950x600')  # Adjusted window height for better view
window.title("Enhanced Language Translator")
window.configure(bg="#1e1e2d")  # Background color

# Set up grid configuration for main window
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=0)

# Title label
title_label = Label(window, text="Enhanced Language Translator", font=("Arial", 24, "bold"), bg="#1e1e2d", fg="white")
title_label.grid(row=0, column=0, columnspan=2, pady=15, sticky=W)

# Text box for paragraph input
input_text = Text(window, width=50, height=8, font=("Arial", 14), wrap=WORD, bd=3, relief=FLAT)
input_text.grid(row=1, column=0, padx=20, pady=10, sticky=W)

# Dropdown for language selection
language_frame = Frame(window, bg="#1e1e2d")
language_frame.grid(row=2, column=0, pady=10, padx=20, sticky=W)

# Add languages to the list of choices
choices = ["English", "Hindi", "German", "French", "Spanish", "Russian", "Punjabi"]
click_option = StringVar()
click_option.set("Select language")

list_drop = OptionMenu(language_frame, click_option, *choices)
list_drop.configure(background="#28a745", foreground="white", font=("Arial", 12, "bold"), relief=FLAT)
list_drop.pack()

# Translated text display label
translated_text_label = Label(window, text="", bg="#1e1e2d", fg="white", font=("Arial", 14, "italic"), wraplength=400, justify="center")
translated_text_label.grid(row=3, column=0, padx=20, pady=20, sticky=W)

# Language code dictionary
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Punjabi": "pa"
}

# Translation history panel setup on the right side
history_label = Label(window, text="Translation History", font=("Arial", 14, "bold"), bg="#1e1e2d", fg="white")
history_label.grid(row=0, column=1, padx=20, pady=10, sticky=N)

history_frame = Frame(window, bg="#1e1e2d")
history_frame.grid(row=1, column=1, rowspan=4, padx=20, pady=10, sticky=NS)

history_text = Text(history_frame, wrap=WORD, font=("Arial", 12), bg="#33334d", fg="white", state=DISABLED, width=30, height=15)
history_text.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(history_frame, command=history_text.yview)
scrollbar.pack(side=RIGHT, fill=Y)
history_text.config(yscrollcommand=scrollbar.set)

# Function to add text to the history panel
def add_to_history(input_text, translated_text):
    history_text.config(state=NORMAL)
    history_text.insert(END, f"Input: {input_text}\nOutput: {translated_text}\n{'-'*50}\n")
    history_text.config(state=DISABLED)
    history_text.see(END)  # Auto-scroll to the latest entry

# Function to convert language with chunking for long text
def convert_language():
    try:
        text_to_translate = input_text.get("1.0", END).strip()  # Get all text from Text widget
        target_language = click_option.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if target_language == "Select language":
            messagebox.showwarning("Selection Error", "Please select a language.")
            return

        # Translate the text
        translator = Translator()
        target_code = language_codes.get(target_language)
        translated = translator.translate(text_to_translate, dest=target_code)
        translated_text = translated.text
        translated_text_label.config(text=translated_text)

        # Add translation to history
        add_to_history(text_to_translate, translated_text)

        # Break translated text into chunks to handle long inputs for gTTS
        audio_chunks = textwrap.wrap(translated_text, width=500)  # Customize chunk size as needed

        temp_files = []
        for i, chunk in enumerate(audio_chunks):
            speech = gTTS(text=chunk, lang=target_code, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_files.append(temp_file.name)
            temp_file.close()
            speech.save(temp_file.name)

        # Play the first audio chunk and queue the rest
        play_audio_chunks(temp_files)

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")

# Function to play audio chunks in sequence
def play_audio_chunks(files):
    def cleanup_files():
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    if files:
        pygame.mixer.music.load(files[0])
        pygame.mixer.music.play()
        files.pop(0)  # Remove the first item since it is being played

        def play_next_chunk():
            if files:
                pygame.mixer.music.load(files[0])
                pygame.mixer.music.play()
                files.pop(0)
            else:
                cleanup_files()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        window.bind("<<music_ended>>", lambda _: play_next_chunk())

# Function to clear input and output fields
def clear_text():
    input_text.delete("1.0", END)
    translated_text_label.config(text="")

# Function to copy translated text to clipboard
def copy_to_clipboard():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        pyperclip.copy(translated_text)
        messagebox.showinfo("Copy to Clipboard", "Translated text copied to clipboard.")

# Function to save translated audio as MP3 file
def save_audio():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        target_language = click_option.get()
        target_code = language_codes.get(target_language)
        
        audio_chunks = textwrap.wrap(translated_text, width=500)
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:
            with open(file_path, "wb") as f:
                for chunk in audio_chunks:
                    speech = gTTS(text=chunk, lang=target_code, slow=False)
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    temp_file.close()
                    speech.save(temp_file.name)
                    with open(temp_file.name, "rb") as tf:
                        f.write(tf.read())
                    os.remove(temp_file.name)
            messagebox.showinfo("Audio Saved", f"Audio saved as {file_path}")

# Function for voice input with retries
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Please speak the text you want to translate.")
        recognizer.adjust_for_ambient_noise(source)
        for attempt in range(3):  # Retry up to 3 times
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                input_text.delete("1.0", END)
                input_text.insert("1.0", text)
                break
            except sr.RequestError:
                if attempt < 2:
                    messagebox.showwarning("Connection Error", "Retrying connection...")
                else:
                    messagebox.showerror("Voice Input Error", "Could not connect to the speech recognition service.")
            except sr.UnknownValueError:
                messagebox.showerror("Voice Input Error", "Could not understand the audio.")
                break

# Buttons
button_frame = Frame(window, bg="#1e1e2d")
button_frame.grid(row=4, column=0, columnspan=2, pady=10)

translate_button = Button(button_frame, text="Translate", bg="#ff5733", fg="white", font=("Arial", 16, "bold"), command=convert_language, relief=FLAT, bd=0, padx=15, pady=8)
translate_button.pack(side=LEFT, padx=5)

clear_button = Button(button_frame, text="Clear Text", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=clear_text, relief=FLAT, padx=15, pady=8)
clear_button.pack(side=LEFT, padx=5)

copy_button = Button(button_frame, text="Copy to Clipboard", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), command=copy_to_clipboard, relief=FLAT, padx=15, pady=8)
copy_button.pack(side=LEFT, padx=5)

save_button = Button(button_frame, text="Save Audio", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=save_audio, relief=FLAT, padx=15, pady=8)
save_button.pack(side=LEFT, padx=5)

voice_button = Button(button_frame, text="Voice Input", bg="#ffc107", fg="white", font=("Arial", 12, "bold"), command=voice_input, relief=FLAT, padx=15, pady=8)
voice_button.pack(side=LEFT, padx=5)

# Run the main application loop
window.mainloop()"""

"""from googletrans import Translator
from gtts import gTTS
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import tempfile
import os
import pyperclip  # For clipboard functionality
import speech_recognition as sr  # For voice input
import textwrap

# Initialize pygame for audio playback
pygame.mixer.init()

# Main application window configuration
window = Tk()
window.geometry('950x600')  # Adjusted window height for better view
window.title("Enhanced Language Translator")
window.configure(bg="#1e1e2d")  # Background color

# Set up grid configuration for main window
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=0)

# Title label
title_label = Label(window, text="Enhanced Language Translator", font=("Arial", 24, "bold"), bg="#1e1e2d", fg="white")
title_label.grid(row=0, column=0, columnspan=2, pady=15, sticky=W)

# Text box for paragraph input
input_text = Text(window, width=50, height=8, font=("Arial", 14), wrap=WORD, bd=3, relief=FLAT)
input_text.grid(row=1, column=0, padx=20, pady=10, sticky=W)

# Dropdown for language selection
language_frame = Frame(window, bg="#1e1e2d")
language_frame.grid(row=2, column=0, pady=10, padx=20, sticky=W)

# Add languages to the list of choices
choices = ["English", "Hindi", "German", "French", "Spanish", "Russian", "Punjabi"]
click_option = StringVar()
click_option.set("Select language")

list_drop = OptionMenu(language_frame, click_option, *choices)
list_drop.configure(background="#28a745", foreground="white", font=("Arial", 12, "bold"), relief=FLAT)
list_drop.pack()

# Translated text display label
translated_text_label = Label(window, text="", bg="#1e1e2d", fg="white", font=("Arial", 14, "italic"), wraplength=400, justify="center")
translated_text_label.grid(row=3, column=0, padx=20, pady=20, sticky=W)

# Language code dictionary
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Punjabi": "pa"
}

# Translation history panel setup on the right side
history_label = Label(window, text="Translation History", font=("Arial", 14, "bold"), bg="#1e1e2d", fg="white")
history_label.grid(row=0, column=1, padx=20, pady=10, sticky=N)

history_frame = Frame(window, bg="#1e1e2d")
history_frame.grid(row=1, column=1, rowspan=4, padx=20, pady=10, sticky=NS)

history_text = Text(history_frame, wrap=WORD, font=("Arial", 12), bg="#33334d", fg="white", state=DISABLED, width=30, height=15)
history_text.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(history_frame, command=history_text.yview)
scrollbar.pack(side=RIGHT, fill=Y)
history_text.config(yscrollcommand=scrollbar.set)

# Function to add text to the history panel
def add_to_history(input_text, translated_text):
    history_text.config(state=NORMAL)
    history_text.insert(END, f"Input: {input_text}\nOutput: {translated_text}\n{'-'*50}\n")
    history_text.config(state=DISABLED)
    history_text.see(END)  # Auto-scroll to the latest entry

# Function to convert language with chunking for long text
def convert_language():
    try:
        text_to_translate = input_text.get("1.0", END).strip()  # Get all text from Text widget
        target_language = click_option.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if target_language == "Select language":
            messagebox.showwarning("Selection Error", "Please select a language.")
            return

        # Translate the text
        translator = Translator()
        target_code = language_codes.get(target_language)
        translated = translator.translate(text_to_translate, dest=target_code)
        translated_text = translated.text
        translated_text_label.config(text=translated_text)

        # Add translation to history
        add_to_history(text_to_translate, translated_text)

        # Break translated text into chunks to handle long inputs for gTTS
        audio_chunks = textwrap.wrap(translated_text, width=500)  # Customize chunk size as needed

        temp_files = []
        for i, chunk in enumerate(audio_chunks):
            speech = gTTS(text=chunk, lang=target_code, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_files.append(temp_file.name)
            temp_file.close()
            speech.save(temp_file.name)

        # Play the first audio chunk and queue the rest
        play_audio_chunks(temp_files)

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")

# Function to play audio chunks in sequence
def play_audio_chunks(files):
    def cleanup_files():
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    if files:
        pygame.mixer.music.load(files[0])
        pygame.mixer.music.play()
        files.pop(0)  # Remove the first item since it is being played

        def play_next_chunk():
            if files:
                pygame.mixer.music.load(files[0])
                pygame.mixer.music.play()
                files.pop(0)
            else:
                cleanup_files()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        window.bind("<<music_ended>>", lambda _: play_next_chunk())

# Function to clear input and output fields
def clear_text():
    input_text.delete("1.0", END)
    translated_text_label.config(text="")

# Function to copy translated text to clipboard
def copy_to_clipboard():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        pyperclip.copy(translated_text)
        messagebox.showinfo("Copy to Clipboard", "Translated text copied to clipboard.")

# Function to save translated audio as MP3 file
def save_audio():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        target_language = click_option.get()
        target_code = language_codes.get(target_language)
        
        audio_chunks = textwrap.wrap(translated_text, width=500)
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:
            with open(file_path, "wb") as f:
                for chunk in audio_chunks:
                    speech = gTTS(text=chunk, lang=target_code, slow=False)
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    temp_file.close()
                    speech.save(temp_file.name)
                    with open(temp_file.name, "rb") as tf:
                        f.write(tf.read())
                    os.remove(temp_file.name)
            messagebox.showinfo("Audio Saved", f"Audio saved as {file_path}")

# Function for voice input with retries
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Please speak the text you want to translate.")
        recognizer.adjust_for_ambient_noise(source)
        for attempt in range(3):  # Retry up to 3 times
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                input_text.delete("1.0", END)
                input_text.insert("1.0", text)
                break
            except sr.RequestError:
                if attempt < 2:
                    messagebox.showwarning("Connection Error", "Retrying connection...")
                else:
                    messagebox.showerror("Voice Input Error", "Could not connect to the speech recognition service.")
            except sr.UnknownValueError:
                messagebox.showerror("Voice Input Error", "Could not understand the audio.")
                break

# Buttons arranged in a grid (2 columns)
button_frame = Frame(window, bg="#1e1e2d")
button_frame.grid(row=4, column=0, columnspan=2, pady=20)

translate_button = Button(button_frame, text="Translate", bg="#ff5733", fg="white", font=("Arial", 16, "bold"), command=convert_language, relief=FLAT, bd=0, padx=15, pady=8)
translate_button.grid(row=0, column=0, padx=10, pady=10)

clear_button = Button(button_frame, text="Clear Text", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=clear_text, relief=FLAT, padx=15, pady=8)
clear_button.grid(row=0, column=1, padx=10, pady=10)

copy_button = Button(button_frame, text="Copy to Clipboard", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), command=copy_to_clipboard, relief=FLAT, padx=15, pady=8)
copy_button.grid(row=1, column=0, padx=10, pady=10)

save_button = Button(button_frame, text="Save Audio", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=save_audio, relief=FLAT, padx=15, pady=8)
save_button.grid(row=1, column=1, padx=10, pady=10)

voice_button = Button(button_frame, text="Voice Input", bg="#ffc107", fg="white", font=("Arial", 12, "bold"), command=voice_input, relief=FLAT, padx=15, pady=8)
voice_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the main application loop
window.mainloop()"""


"""from googletrans import Translator
from gtts import gTTS
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import tempfile
import os
import pyperclip  # For clipboard functionality
import speech_recognition as sr  # For voice input
import textwrap

# Initialize pygame for audio playback
pygame.mixer.init()

# Main application window configuration
window = Tk()
window.geometry('1000x600')  # Adjusted window size
window.title("Enhanced Language Translator")
window.configure(bg="#1e1e2d")  # Background color

# Title label at the top
title_label = Label(window, text="Enhanced Language Translator", font=("Arial", 24, "bold"), bg="#1e1e2d", fg="white")
title_label.grid(row=0, column=0, columnspan=2, pady=20, sticky=W)

# Frame for input section (Left part)
input_frame = Frame(window, bg="#1e1e2d")
input_frame.grid(row=1, column=0, padx=20, pady=20, sticky=N)

# Text box for paragraph input
input_text = Text(input_frame, width=50, height=8, font=("Arial", 14), wrap=WORD, bd=3, relief=FLAT)
input_text.grid(row=0, column=0, pady=10)

# Dropdown for language selection
language_frame = Frame(input_frame, bg="#1e1e2d")
language_frame.grid(row=1, column=0, pady=10)

choices = ["English", "Hindi", "German", "French", "Spanish", "Russian", "Punjabi"]
click_option = StringVar()
click_option.set("Select language")

list_drop = OptionMenu(language_frame, click_option, *choices)
list_drop.configure(background="#28a745", foreground="white", font=("Arial", 12, "bold"), relief=FLAT)
list_drop.pack()

# Frame for output section (Right part)
output_frame = Frame(window, bg="#1e1e2d")
output_frame.grid(row=1, column=1, padx=20, pady=20, sticky=N)

# Translated text display label
translated_text_label = Label(output_frame, text="", bg="#1e1e2d", fg="white", font=("Arial", 14, "italic"), wraplength=400, justify="center")
translated_text_label.grid(row=0, column=0, pady=10)

# Translation history panel setup on the right side
history_label = Label(output_frame, text="Translation History", font=("Arial", 14, "bold"), bg="#1e1e2d", fg="white")
history_label.grid(row=1, column=0, pady=10)

history_text = Text(output_frame, wrap=WORD, font=("Arial", 12), bg="#33334d", fg="white", state=DISABLED, width=40, height=15)
history_text.grid(row=2, column=0, pady=10)

scrollbar = Scrollbar(output_frame, command=history_text.yview)
scrollbar.grid(row=2, column=1, sticky=NS)
history_text.config(yscrollcommand=scrollbar.set)

# Language code dictionary
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Punjabi": "pa"
}

# Function to add text to the history panel
def add_to_history(input_text, translated_text):
    history_text.config(state=NORMAL)
    history_text.insert(END, f"Input: {input_text}\nOutput: {translated_text}\n{'-'*50}\n")
    history_text.config(state=DISABLED)
    history_text.see(END)  # Auto-scroll to the latest entry

# Function to convert language with chunking for long text
def convert_language():
    try:
        text_to_translate = input_text.get("1.0", END).strip()  # Get all text from Text widget
        target_language = click_option.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if target_language == "Select language":
            messagebox.showwarning("Selection Error", "Please select a language.")
            return

        # Translate the text
        translator = Translator()
        target_code = language_codes.get(target_language)
        translated = translator.translate(text_to_translate, dest=target_code)
        translated_text = translated.text
        translated_text_label.config(text=translated_text)

        # Add translation to history
        add_to_history(text_to_translate, translated_text)

        # Break translated text into chunks to handle long inputs for gTTS
        audio_chunks = textwrap.wrap(translated_text, width=500)  # Customize chunk size as needed

        temp_files = []
        for i, chunk in enumerate(audio_chunks):
            speech = gTTS(text=chunk, lang=target_code, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_files.append(temp_file.name)
            temp_file.close()
            speech.save(temp_file.name)

        # Play the first audio chunk and queue the rest
        play_audio_chunks(temp_files)

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")

# Function to play audio chunks in sequence
def play_audio_chunks(files):
    def cleanup_files():
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    if files:
        pygame.mixer.music.load(files[0])
        pygame.mixer.music.play()
        files.pop(0)  # Remove the first item since it is being played

        def play_next_chunk():
            if files:
                pygame.mixer.music.load(files[0])
                pygame.mixer.music.play()
                files.pop(0)
            else:
                cleanup_files()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        window.bind("<<music_ended>>", lambda _: play_next_chunk())

# Function to clear input and output fields
def clear_text():
    input_text.delete("1.0", END)
    translated_text_label.config(text="")

# Function to copy translated text to clipboard
def copy_to_clipboard():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        pyperclip.copy(translated_text)
        messagebox.showinfo("Copy to Clipboard", "Translated text copied to clipboard.")

# Function to save translated audio as MP3 file
def save_audio():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        target_language = click_option.get()
        target_code = language_codes.get(target_language)
        
        audio_chunks = textwrap.wrap(translated_text, width=500)
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:
            with open(file_path, "wb") as f:
                for chunk in audio_chunks:
                    speech = gTTS(text=chunk, lang=target_code, slow=False)
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    temp_file.close()
                    speech.save(temp_file.name)
                    with open(temp_file.name, "rb") as tf:
                        f.write(tf.read())
                    os.remove(temp_file.name)
            messagebox.showinfo("Audio Saved", f"Audio saved as {file_path}")

# Function for voice input with retries
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Please speak the text you want to translate.")
        recognizer.adjust_for_ambient_noise(source)
        for attempt in range(3):  # Retry up to 3 times
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                input_text.delete("1.0", END)
                input_text.insert("1.0", text)
                break
            except sr.RequestError:
                if attempt < 2:
                    messagebox.showwarning("Connection Error", "Retrying connection...")
                else:
                    messagebox.showerror("Voice Input Error", "Could not connect to the speech recognition service.")
            except sr.UnknownValueError:
                messagebox.showerror("Voice Input Error", "Could not understand the audio.")
                break

# Buttons placed in a single row at the bottom
button_frame = Frame(window, bg="#1e1e2d")
button_frame.grid(row=2, column=0, columnspan=2, pady=20, sticky=S)

translate_button = Button(button_frame, text="Translate", bg="#ff5733", fg="white", font=("Arial", 16, "bold"), command=convert_language, relief=FLAT, bd=0, padx=15, pady=8)
translate_button.grid(row=0, column=0, padx=10)

clear_button = Button(button_frame, text="Clear Text", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=clear_text, relief=FLAT, padx=15, pady=8)
clear_button.grid(row=0, column=1, padx=10)

copy_button = Button(button_frame, text="Copy to Clipboard", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), command=copy_to_clipboard, relief=FLAT, padx=15, pady=8)
copy_button.grid(row=0, column=2, padx=10)

save_button = Button(button_frame, text="Save Audio", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=save_audio, relief=FLAT, padx=15, pady=8)
save_button.grid(row=0, column=3, padx=10)

voice_button = Button(button_frame, text="Voice Input", bg="#ffc107", fg="white", font=("Arial", 12, "bold"), command=voice_input, relief=FLAT, padx=15, pady=8)
voice_button.grid(row=0, column=4, padx=10)

# Run the main application loop
window.mainloop()"""

#50percnt nice
from googletrans import Translator
from gtts import gTTS
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import tempfile
import os
import pyperclip  # For clipboard functionality
import speech_recognition as sr  # For voice input
import textwrap

# Initialize pygame for audio playback
pygame.mixer.init()

# Main application window configuration
window = Tk()
window.geometry('1000x650')  # Adjusted window size for better layout
window.title("Enhanced Language Translator")
window.configure(bg="#1e1e2d")  # Background color

# Header section with title and optional instructions
header_frame = Frame(window, bg="#1e1e2d")
header_frame.grid(row=0, column=0, columnspan=2, pady=20, sticky=N)

title_label = Label(header_frame, text="Enhanced Language Translator", font=("Arial", 24, "bold"), bg="#1e1e2d", fg="white")
title_label.grid(row=0, column=0, pady=5)

instructions_label = Label(header_frame, text="Enter text, choose a language, and get translations!", font=("Arial", 12), bg="#1e1e2d", fg="white")
instructions_label.grid(row=1, column=0, pady=5)

# Frame for input and output area (Left for input, right for output)
main_frame = Frame(window, bg="#1e1e2d")
main_frame.grid(row=1, column=0, columnspan=2, pady=20, sticky=W+E)

# Left Panel (Input area)
input_frame = Frame(main_frame, bg="#1e1e2d")
input_frame.grid(row=0, column=0, padx=20, pady=10, sticky=N+W)

# Text box for paragraph input
input_text = Text(input_frame, width=40, height=8, font=("Arial", 14), wrap=WORD, bd=3, relief=FLAT)
input_text.grid(row=0, column=0, pady=10)

# Dropdown for language selection
language_frame = Frame(input_frame, bg="#1e1e2d")
language_frame.grid(row=1, column=0, pady=10)

choices = ["English", "Hindi", "German", "French", "Spanish", "Russian", "Punjabi"]
click_option = StringVar()
click_option.set("Select language")

list_drop = OptionMenu(language_frame, click_option, *choices)
list_drop.configure(background="#28a745", foreground="white", font=("Arial", 12, "bold"), relief=FLAT)
list_drop.pack()

# Right Panel (Output area)
output_frame = Frame(main_frame, bg="#1e1e2d")
output_frame.grid(row=0, column=1, padx=20, pady=10, sticky=N+E)

# Translated text display label
translated_text_label = Label(output_frame, text="", bg="#1e1e2d", fg="white", font=("Arial", 14, "italic"), wraplength=400, justify="center")
translated_text_label.grid(row=0, column=0, pady=10)

# Translation history panel setup
history_label = Label(window, text="Translation History", font=("Arial", 14, "bold"), bg="#1e1e2d", fg="white")
history_label.grid(row=2, column=0, columnspan=2, pady=10)

history_text = Text(window, wrap=WORD, font=("Arial", 12), bg="#33334d", fg="white", state=DISABLED, width=80, height=10)
history_text.grid(row=3, column=0, columnspan=2, pady=10)

scrollbar = Scrollbar(window, command=history_text.yview)
scrollbar.grid(row=3, column=2, sticky=NS)
history_text.config(yscrollcommand=scrollbar.set)

# Language code dictionary
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Punjabi": "pa"
}

# Function to add text to the history panel
def add_to_history(input_text, translated_text):
    history_text.config(state=NORMAL)
    history_text.insert(END, f"Input: {input_text}\nOutput: {translated_text}\n{'-'*50}\n")
    history_text.config(state=DISABLED)
    history_text.see(END)  # Auto-scroll to the latest entry

# Function to convert language with chunking for long text
def convert_language():
    try:
        text_to_translate = input_text.get("1.0", END).strip()  # Get all text from Text widget
        target_language = click_option.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if target_language == "Select language":
            messagebox.showwarning("Selection Error", "Please select a language.")
            return

        # Translate the text
        translator = Translator()
        target_code = language_codes.get(target_language)
        translated = translator.translate(text_to_translate, dest=target_code)
        translated_text = translated.text
        translated_text_label.config(text=translated_text)

        # Add translation to history
        add_to_history(text_to_translate, translated_text)

        # Break translated text into chunks to handle long inputs for gTTS
        audio_chunks = textwrap.wrap(translated_text, width=500)  # Customize chunk size as needed

        temp_files = []
        for i, chunk in enumerate(audio_chunks):
            speech = gTTS(text=chunk, lang=target_code, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_files.append(temp_file.name)
            temp_file.close()
            speech.save(temp_file.name)

        # Play the first audio chunk and queue the rest
        play_audio_chunks(temp_files)

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")

# Function to play audio chunks in sequence
def play_audio_chunks(files):
    def cleanup_files():
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    if files:
        pygame.mixer.music.load(files[0])
        pygame.mixer.music.play()
        files.pop(0)  # Remove the first item since it is being played

        def play_next_chunk():
            if files:
                pygame.mixer.music.load(files[0])
                pygame.mixer.music.play()
                files.pop(0)
            else:
                cleanup_files()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        window.bind("<<music_ended>>", lambda _: play_next_chunk())

# Function to clear input and output fields
def clear_text():
    input_text.delete("1.0", END)
    translated_text_label.config(text="")

# Function to copy translated text to clipboard
def copy_to_clipboard():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        pyperclip.copy(translated_text)
        messagebox.showinfo("Copy to Clipboard", "Translated text copied to clipboard.")

# Function to save translated audio as MP3 file
def save_audio():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        target_language = click_option.get()
        target_code = language_codes.get(target_language)
        
        audio_chunks = textwrap.wrap(translated_text, width=500)
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:
            with open(file_path, "wb") as f:
                for chunk in audio_chunks:
                    speech = gTTS(text=chunk, lang=target_code, slow=False)
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    temp_file.close()
                    speech.save(temp_file.name)
                    with open(temp_file.name, "rb") as tf:
                        f.write(tf.read())
                    os.remove(temp_file.name)
            messagebox.showinfo("Audio Saved", f"Audio saved as {file_path}")

# Function for voice input with retries
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Please speak the text you want to translate.")
        recognizer.adjust_for_ambient_noise(source)
        for attempt in range(3):  # Retry up to 3 times
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                input_text.delete("1.0", END)
                input_text.insert("1.0", text)
                break
            except sr.RequestError:
                if attempt < 2:
                    messagebox.showwarning("Connection Error", "Retrying connection...")
                else:
                    messagebox.showerror("Voice Input Error", "Could not connect to the speech recognition service.")
            except sr.UnknownValueError:
                messagebox.showerror("Voice Input Error", "Could not understand the audio.")
                break

# Button frame with horizontal arrangement
button_frame = Frame(window, bg="#1e1e2d")
button_frame.grid(row=4, column=0, columnspan=2, pady=20, sticky=N)

translate_button = Button(button_frame, text="Translate", bg="#ff5733", fg="white", font=("Arial", 16, "bold"), command=convert_language, relief=FLAT, bd=0, padx=15, pady=8)
translate_button.grid(row=0, column=0, padx=10)

clear_button = Button(button_frame, text="Clear Text", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=clear_text, relief=FLAT, padx=15, pady=8)
clear_button.grid(row=0, column=1, padx=10)

copy_button = Button(button_frame, text="Copy to Clipboard", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), command=copy_to_clipboard, relief=FLAT, padx=15, pady=8)
copy_button.grid(row=0, column=2, padx=10)

save_button = Button(button_frame, text="Save Audio", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=save_audio, relief=FLAT, padx=15, pady=8)
save_button.grid(row=0, column=3, padx=10)

voice_button = Button(button_frame, text="Voice Input", bg="#ffc107", fg="white", font=("Arial", 12, "bold"), command=voice_input, relief=FLAT, padx=15, pady=8)
voice_button.grid(row=0, column=4, padx=10)

# Run the main application loop
window.mainloop()


#80percent
"""from googletrans import Translator
from gtts import gTTS
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import tempfile
import os
import pyperclip  # For clipboard functionality
import speech_recognition as sr  # For voice input
import textwrap

# Initialize pygame for audio playback
pygame.mixer.init()

# Main application window configuration
window = Tk()
window.geometry('1000x750')  # Adjusted window size for better layout
window.title("Enhanced Language Translator")
window.configure(bg="#1e1e2d")  # Background color

# Header section with title and optional instructions
header_frame = Frame(window, bg="#1e1e2d")
header_frame.grid(row=0, column=0, columnspan=2, pady=20, sticky=N)

title_label = Label(header_frame, text="Enhanced Language Translator", font=("Arial", 24, "bold"), bg="#1e1e2d", fg="white")
title_label.grid(row=0, column=0, pady=5)

instructions_label = Label(header_frame, text="Enter text, choose a language, and get translations!", font=("Arial", 12), bg="#1e1e2d", fg="white")
instructions_label.grid(row=1, column=0, pady=5)

# Main input and output frame (split horizontally)
main_frame = Frame(window, bg="#1e1e2d")
main_frame.grid(row=1, column=0, columnspan=2, pady=20, sticky=W+E)

# Left Panel (Input Area)
input_frame = Frame(main_frame, bg="#1e1e2d")
input_frame.grid(row=0, column=0, padx=20, pady=10, sticky=N+W)

# Text box for paragraph input
input_text = Text(input_frame, width=40, height=8, font=("Arial", 14), wrap=WORD, bd=3, relief=FLAT)
input_text.grid(row=0, column=0, pady=10)

# Dropdown for language selection
language_frame = Frame(input_frame, bg="#1e1e2d")
language_frame.grid(row=1, column=0, pady=10)

choices = ["English", "Hindi", "German", "French", "Spanish", "Russian", "Punjabi"]
click_option = StringVar()
click_option.set("Select language")

list_drop = OptionMenu(language_frame, click_option, *choices)
list_drop.configure(background="#28a745", foreground="white", font=("Arial", 12, "bold"), relief=FLAT)
list_drop.pack()

# Right Panel (Output Area)
output_frame = Frame(main_frame, bg="#1e1e2d")
output_frame.grid(row=0, column=1, padx=20, pady=10, sticky=N+E)

# Translated text display label
translated_text_label = Label(output_frame, text="", bg="#1e1e2d", fg="white", font=("Arial", 14, "italic"), wraplength=400, justify="center")
translated_text_label.grid(row=0, column=0, pady=10)

# Translation history panel setup
history_label = Label(window, text="Translation History", font=("Arial", 14, "bold"), bg="#1e1e2d", fg="white")
history_label.grid(row=2, column=0, columnspan=2, pady=10)

history_text = Text(window, wrap=WORD, font=("Arial", 12), bg="#33334d", fg="white", state=DISABLED, width=80, height=10)
history_text.grid(row=3, column=0, columnspan=2, pady=10)

scrollbar = Scrollbar(window, command=history_text.yview)
scrollbar.grid(row=3, column=2, sticky=NS)
history_text.config(yscrollcommand=scrollbar.set)

# Language code dictionary
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Punjabi": "pa"
}

# Function to add text to the history panel
def add_to_history(input_text, translated_text):
    history_text.config(state=NORMAL)
    history_text.insert(END, f"Input: {input_text}\nOutput: {translated_text}\n{'-'*50}\n")
    history_text.config(state=DISABLED)
    history_text.see(END)  # Auto-scroll to the latest entry

# Function to convert language with chunking for long text
def convert_language():
    try:
        text_to_translate = input_text.get("1.0", END).strip()  # Get all text from Text widget
        target_language = click_option.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if target_language == "Select language":
            messagebox.showwarning("Selection Error", "Please select a language.")
            return

        # Translate the text
        translator = Translator()
        target_code = language_codes.get(target_language)
        translated = translator.translate(text_to_translate, dest=target_code)
        translated_text = translated.text
        translated_text_label.config(text=translated_text)

        # Add translation to history
        add_to_history(text_to_translate, translated_text)

        # Break translated text into chunks to handle long inputs for gTTS
        audio_chunks = textwrap.wrap(translated_text, width=500)  # Customize chunk size as needed

        temp_files = []
        for i, chunk in enumerate(audio_chunks):
            speech = gTTS(text=chunk, lang=target_code, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_files.append(temp_file.name)
            temp_file.close()
            speech.save(temp_file.name)

        # Play the first audio chunk and queue the rest
        play_audio_chunks(temp_files)

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")

# Function to play audio chunks in sequence
def play_audio_chunks(files):
    def cleanup_files():
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    if files:
        pygame.mixer.music.load(files[0])
        pygame.mixer.music.play()
        files.pop(0)  # Remove the first item since it is being played

        def play_next_chunk():
            if files:
                pygame.mixer.music.load(files[0])
                pygame.mixer.music.play()
                files.pop(0)
            else:
                cleanup_files()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        window.bind("<<music_ended>>", lambda _: play_next_chunk())

# Function to clear input and output fields
def clear_text():
    input_text.delete("1.0", END)
    translated_text_label.config(text="")

# Function to copy translated text to clipboard
def copy_to_clipboard():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        pyperclip.copy(translated_text)
        messagebox.showinfo("Copy to Clipboard", "Translated text copied to clipboard.")

# Function to save translated audio as MP3 file
def save_audio():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        target_language = click_option.get()
        target_code = language_codes.get(target_language)
        
        audio_chunks = textwrap.wrap(translated_text, width=500)
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:
            with open(file_path, "wb") as f:
                for chunk in audio_chunks:
                    speech = gTTS(text=chunk, lang=target_code, slow=False)
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    temp_file.close()
                    speech.save(temp_file.name)
                    with open(temp_file.name, "rb") as tf:
                        f.write(tf.read())
                    os.remove(temp_file.name)
            messagebox.showinfo("Audio Saved", f"Audio saved as {file_path}")

# Function for voice input with retries
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Please speak the text you want to translate.")
        recognizer.adjust_for_ambient_noise(source)
        for attempt in range(3):  # Retry up to 3 times
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                input_text.delete("1.0", END)
                input_text.insert("1.0", text)
                break
            except sr.RequestError:
                if attempt < 2:
                    messagebox.showwarning("Connection Error", "Retrying connection...")
                else:
                    messagebox.showerror("Voice Input Error", "Could not connect to the speech recognition service.")
            except sr.UnknownValueError:
                messagebox.showerror("Voice Input Error", "Could not understand the audio.")
                break

# Button Frame with Vertical Alignment
button_frame = Frame(window, bg="#1e1e2d")
button_frame.grid(row=1, column=2, padx=20, pady=20, sticky=N+S)

translate_button = Button(button_frame, text="Translate", bg="#ff5733", fg="white", font=("Arial", 16, "bold"), command=convert_language, relief=FLAT, bd=0, padx=15, pady=8)
translate_button.grid(row=0, column=0, pady=10)

clear_button = Button(button_frame, text="Clear Text", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=clear_text, relief=FLAT, padx=15, pady=8)
clear_button.grid(row=1, column=0, pady=10)

copy_button = Button(button_frame, text="Copy to Clipboard", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), command=copy_to_clipboard, relief=FLAT, padx=15, pady=8)
copy_button.grid(row=2, column=0, pady=10)

save_button = Button(button_frame, text="Save Audio", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=save_audio, relief=FLAT, padx=15, pady=8)
save_button.grid(row=3, column=0, pady=10)

voice_button = Button(button_frame, text="Voice Input", bg="#ffc107", fg="white", font=("Arial", 12, "bold"), command=voice_input, relief=FLAT, padx=15, pady=8)
voice_button.grid(row=4, column=0, pady=10)

# Start the Tkinter event loop
window.mainloop()"""

"""from googletrans import Translator
from gtts import gTTS
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import tempfile
import os
import pyperclip
import speech_recognition as sr
import textwrap

# Initialize pygame for audio playback
pygame.mixer.init()

# Main application window configuration
window = Tk()
window.geometry('1000x750')  # Adjusted window size for better layout
window.title("Enhanced Language Translator")
window.configure(bg="#1e1e2d")  # Background color

# Header section with title and optional instructions
header_frame = Frame(window, bg="#1e1e2d")
header_frame.grid(row=0, column=0, columnspan=2, pady=20, sticky=N)

title_label = Label(header_frame, text="Enhanced Language Translator", font=("Arial", 24, "bold"), bg="#1e1e2d", fg="white")
title_label.grid(row=0, column=0, pady=5)

instructions_label = Label(header_frame, text="Enter text, choose a language, and get translations!", font=("Arial", 12), bg="#1e1e2d", fg="white")
instructions_label.grid(row=1, column=0, pady=5)

# Main input and output frame (split horizontally)
main_frame = Frame(window, bg="#1e1e2d")
main_frame.grid(row=1, column=0, columnspan=2, pady=20, sticky=W+E)

# Left Panel (Input Area)
input_frame = Frame(main_frame, bg="#1e1e2d")
input_frame.grid(row=0, column=0, padx=20, pady=10, sticky=N+W)

# Text box for paragraph input
# Text box for paragraph input with increased size
# Text box for paragraph input with increased size (wider)
input_text = Text(input_frame, width=80, height=12, font=("Arial", 14), wrap=WORD, bd=3, relief=FLAT)
input_text.grid(row=0, column=0, pady=10)


# Dropdown for language selection
language_frame = Frame(input_frame, bg="#1e1e2d")
language_frame.grid(row=1, column=0, pady=10)

choices = ["English", "Hindi", "German", "French", "Spanish", "Russian", "Punjabi"]
click_option = StringVar()
click_option.set("Select language")

list_drop = OptionMenu(language_frame, click_option, *choices)
list_drop.configure(background="#28a745", foreground="white", font=("Arial", 12, "bold"), relief=FLAT)
list_drop.pack()

# Right Panel (Output Area)
output_frame = Frame(main_frame, bg="#1e1e2d")
output_frame.grid(row=0, column=1, padx=20, pady=10, sticky=N+E)

# Translated text display label
translated_text_label = Label(output_frame, text="", bg="#1e1e2d", fg="white", font=("Arial", 14, "italic"), wraplength=400, justify="center")
translated_text_label.grid(row=0, column=0, pady=10)

# Translation history panel setup
history_label = Label(window, text="Translation History", font=("Arial", 14, "bold"), bg="#1e1e2d", fg="white")
history_label.grid(row=2, column=0, columnspan=2, pady=10)

history_text = Text(window, wrap=WORD, font=("Arial", 12), bg="#33334d", fg="white", state=DISABLED, width=80, height=10)
history_text.grid(row=3, column=0, columnspan=2, pady=10)

scrollbar = Scrollbar(window, command=history_text.yview)
scrollbar.grid(row=3, column=2, sticky=NS)
history_text.config(yscrollcommand=scrollbar.set)

# Language code dictionary
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Punjabi": "pa"
}

# Function to add text to the history panel
def add_to_history(input_text, translated_text):
    history_text.config(state=NORMAL)
    history_text.insert(END, f"Input: {input_text}\nOutput: {translated_text}\n{'-'*50}\n")
    history_text.config(state=DISABLED)
    history_text.see(END)  # Auto-scroll to the latest entry

# Function to convert language with chunking for long text
def convert_language():
    try:
        text_to_translate = input_text.get("1.0", END).strip()  # Get all text from Text widget
        target_language = click_option.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if target_language == "Select language":
            messagebox.showwarning("Selection Error", "Please select a language.")
            return

        # Translate the text
        translator = Translator()
        target_code = language_codes.get(target_language)
        translated = translator.translate(text_to_translate, dest=target_code)
        translated_text = translated.text

        # Make sure the label is updated correctly
        translated_text_label.config(text=translated_text)  # This should show the translation on the right side

        # Add translation to history
        add_to_history(text_to_translate, translated_text)

        # Break translated text into chunks to handle long inputs for gTTS
        audio_chunks = textwrap.wrap(translated_text, width=500)  # Customize chunk size as needed

        temp_files = []
        for i, chunk in enumerate(audio_chunks):
            speech = gTTS(text=chunk, lang=target_code, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_files.append(temp_file.name)
            temp_file.close()
            speech.save(temp_file.name)

        # Play the first audio chunk and queue the rest
        play_audio_chunks(temp_files)

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")

# Function to play audio chunks in sequence
def play_audio_chunks(files):
    def cleanup_files():
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    if files:
        pygame.mixer.music.load(files[0])
        pygame.mixer.music.play()
        files.pop(0)  # Remove the first item since it is being played

        def play_next_chunk():
            if files:
                pygame.mixer.music.load(files[0])
                pygame.mixer.music.play()
                files.pop(0)
            else:
                cleanup_files()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        window.bind("<<music_ended>>", lambda _: play_next_chunk())

# Function to clear input and output fields
def clear_text():
    input_text.delete("1.0", END)
    translated_text_label.config(text="")

# Function to copy translated text to clipboard
def copy_to_clipboard():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        pyperclip.copy(translated_text)
        messagebox.showinfo("Copy to Clipboard", "Translated text copied to clipboard.")

# Function to save translated audio as MP3 file
def save_audio():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        target_language = click_option.get()
        target_code = language_codes.get(target_language)
        
        audio_chunks = textwrap.wrap(translated_text, width=500)
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:
            with open(file_path, "wb") as f:
                for chunk in audio_chunks:
                    speech = gTTS(text=chunk, lang=target_code, slow=False)
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    temp_file.close()
                    speech.save(temp_file.name)
                    with open(temp_file.name, "rb") as tf:
                        f.write(tf.read())
                    os.remove(temp_file.name)
            messagebox.showinfo("Save Audio", "Audio file saved successfully.")
    else:
        messagebox.showwarning("No Translated Text", "No translation available to save as audio.")

# Button Frame with Vertical Alignment
button_frame = Frame(window, bg="#1e1e2d")
button_frame.grid(row=1, column=2, padx=20, pady=20, sticky=N+S)

translate_button = Button(button_frame, text="Translate", bg="#ff5733", fg="white", font=("Arial", 16, "bold"), command=convert_language, relief=FLAT, bd=0, padx=15, pady=8)
translate_button.grid(row=0, column=0, pady=10)

clear_button = Button(button_frame, text="Clear Text", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=clear_text, relief=FLAT, padx=15, pady=8)
clear_button.grid(row=1, column=0, pady=10)

copy_button = Button(button_frame, text="Copy to Clipboard", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), command=copy_to_clipboard, relief=FLAT, padx=15, pady=8)
copy_button.grid(row=2, column=0, pady=10)

save_button = Button(button_frame, text="Save Audio", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=save_audio, relief=FLAT, padx=15, pady=8)
save_button.grid(row=3, column=0, pady=10)

voice_button = Button(button_frame, text="Voice Input", bg="#ffc107", fg="white", font=("Arial", 12, "bold"), command=voice_input, relief=FLAT, padx=15, pady=8)
voice_button.grid(row=4, column=0, pady=10)

# Start the Tkinter event loop
window.mainloop()"""

from googletrans import Translator
from gtts import gTTS
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import tempfile
import os
import pyperclip
import speech_recognition as sr
import textwrap

# Initialize pygame for audio playback
pygame.mixer.init()

# Main application window configuration
window = Tk()
window.geometry('1000x750')  # Adjusted window size for better layout
window.title("Enhanced Language Translator")
window.configure(bg="#1e1e2d")  # Background color

# Header section with title and optional instructions
header_frame = Frame(window, bg="#1e1e2d")
header_frame.grid(row=0, column=0, columnspan=2, pady=20, sticky=N)

title_label = Label(header_frame, text="Enhanced Language Translator", font=("Arial", 24, "bold"), bg="#1e1e2d", fg="white")
title_label.grid(row=0, column=0, pady=5)

instructions_label = Label(header_frame, text="Enter text, choose a language, and get translations!", font=("Arial", 12), bg="#1e1e2d", fg="white")
instructions_label.grid(row=1, column=0, pady=5)

# Main input and output frame (split horizontally)
main_frame = Frame(window, bg="#1e1e2d")
main_frame.grid(row=1, column=0, columnspan=2, pady=20, sticky=W+E)

# Left Panel (Input Area)
input_frame = Frame(main_frame, bg="#1e1e2d")
input_frame.grid(row=0, column=0, padx=20, pady=10, sticky=N+W)

# Label for Input Box
input_label = Label(input_frame, text="Input Box:", font=("Arial", 14, "bold"), bg="#1e1e2d", fg="white")
input_label.grid(row=0, column=0, pady=5, sticky=W)

# Text box for paragraph input with increased size
input_text = Text(input_frame, width=80, height=12, font=("Arial", 14), wrap=WORD, bd=3, relief=FLAT)
input_text.grid(row=1, column=0,columnspan=2, pady=10)

# Dropdown for language selection
language_frame = Frame(input_frame, bg="#1e1e2d")
language_frame.grid(row=2, column=0, pady=10)

choices = ["English", "Hindi", "German", "French", "Spanish", "Russian", "Punjabi"]
click_option = StringVar()
click_option.set("Select language")

list_drop = OptionMenu(language_frame, click_option, *choices)
list_drop.configure(background="#28a745", foreground="white", font=("Arial", 12, "bold"), relief=FLAT)
list_drop.pack()

# Right Panel (Output Area)
output_frame = Frame(main_frame, bg="#1e1e2d")
output_frame.grid(row=0, column=1, padx=20, pady=10, sticky=N+E)

# Translated text display label
translated_text_label = Label(output_frame, text="", bg="#1e1e2d", fg="white", font=("Arial", 14, "italic"), wraplength=400, justify="center")
translated_text_label.grid(row=0, column=0, pady=10)

# Translation history panel setup
history_label = Label(window, text="Translation History", font=("Arial", 14, "bold"), bg="#1e1e2d", fg="white")
history_label.grid(row=2, column=0, columnspan=2, pady=10)

history_text = Text(window, wrap=WORD, font=("Arial", 12), bg="#33334d", fg="white", state=DISABLED, width=80, height=10)
history_text.grid(row=3, column=0, columnspan=2, pady=10)

scrollbar = Scrollbar(window, command=history_text.yview)
scrollbar.grid(row=3, column=2, sticky=NS)
history_text.config(yscrollcommand=scrollbar.set)

# Language code dictionary
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Punjabi": "pa"
}

# Function to add text to the history panel
def add_to_history(input_text, translated_text):
    history_text.config(state=NORMAL)
    history_text.insert(END, f"Input: {input_text}\nOutput: {translated_text}\n{'-'*50}\n")
    history_text.config(state=DISABLED)
    history_text.see(END)  # Auto-scroll to the latest entry

# Function to convert language with chunking for long text
def convert_language():
    try:
        text_to_translate = input_text.get("1.0", END).strip()  # Get all text from Text widget
        target_language = click_option.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if target_language == "Select language":
            messagebox.showwarning("Selection Error", "Please select a language.")
            return

        # Translate the text
        translator = Translator()
        target_code = language_codes.get(target_language)
        translated = translator.translate(text_to_translate, dest=target_code)
        translated_text = translated.text

        # Make sure the label is updated correctly
        translated_text_label.config(text=translated_text)  # This should show the translation on the right side

        # Add translation to history
        add_to_history(text_to_translate, translated_text)

        # Break translated text into chunks to handle long inputs for gTTS
        audio_chunks = textwrap.wrap(translated_text, width=500)  # Customize chunk size as needed

        temp_files = []
        for i, chunk in enumerate(audio_chunks):
            speech = gTTS(text=chunk, lang=target_code, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_files.append(temp_file.name)
            temp_file.close()
            speech.save(temp_file.name)

        # Play the first audio chunk and queue the rest
        play_audio_chunks(temp_files)

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")

# Function to play audio chunks in sequence
def play_audio_chunks(files):
    def cleanup_files():
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    if files:
        pygame.mixer.music.load(files[0])
        pygame.mixer.music.play()
        files.pop(0)  # Remove the first item since it is being played

        def play_next_chunk():
            if files:
                pygame.mixer.music.load(files[0])
                pygame.mixer.music.play()
                files.pop(0)
            else:
                cleanup_files()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        window.bind("<<music_ended>>", lambda _: play_next_chunk())

# Function to clear input and output fields
def clear_text():
    input_text.delete("1.0", END)
    translated_text_label.config(text="")

# Function to copy translated text to clipboard
def copy_to_clipboard():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        pyperclip.copy(translated_text)
        messagebox.showinfo("Copy to Clipboard", "Translated text copied to clipboard.")

# Function to save translated audio as MP3 file
def save_audio():
    translated_text = translated_text_label.cget("text")
    if translated_text:
        target_language = click_option.get()
        target_code = language_codes.get(target_language)
        
        audio_chunks = textwrap.wrap(translated_text, width=500)
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:
            with open(file_path, "wb") as f:
                for chunk in audio_chunks:
                    speech = gTTS(text=chunk, lang=target_code, slow=False)
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    temp_file.close()
                    speech.save(temp_file.name)
                    with open(temp_file.name, "rb") as tf:
                        f.write(tf.read())
                    os.remove(temp_file.name)
            messagebox.showinfo("Save Audio", "Audio file saved successfully.")
    else:
        messagebox.showwarning("No Translated Text", "No translation available to save as audio.")

# Button Frame with Vertical Alignment
button_frame = Frame(window, bg="#1e1e2d")
button_frame.grid(row=1, column=2, padx=20, pady=20, sticky=N+S)

translate_button = Button(button_frame, text="Translate", bg="#ff5733", fg="white", font=("Arial", 16, "bold"), command=convert_language, relief=FLAT, bd=0, padx=15, pady=8)
translate_button.grid(row=0, column=0, pady=10)

clear_button = Button(button_frame, text="Clear Text", bg="#007bff", fg="white", font=("Arial", 12, "bold"), command=clear_text, relief=FLAT, padx=15, pady=8)
clear_button.grid(row=1, column=0, pady=10)

copy_button = Button(button_frame, text="Copy to Clipboard", bg="#6c757d", fg="white", font=("Arial", 12, "bold"), command=copy_to_clipboard, relief=FLAT, padx=15, pady=8)
copy_button.grid(row=2, column=0, pady=10)

save_button = Button(button_frame, text="Save Audio", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=save_audio, relief=FLAT, padx=15, pady=8)
save_button.grid(row=3, column=0, pady=10)

voice_button = Button(button_frame, text="Voice Input", bg="#ffc107", fg="white", font=("Arial", 12, "bold"), command=None, relief=FLAT, padx=15, pady=8)
voice_button.grid(row=4, column=0, pady=10)

# Start the Tkinter event loop
window.mainloop()




