import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
import pyttsx3
import os

# --- Initialization ---
app = Tk()
app.title("Voice Generator")
app.geometry("900x450")
app.resizable(False, False)
app.configure(bg="#F9F4EF")

# --- Logic Functions ---

def get_configured_engine():
    engine = pyttsx3.init()
    
    # Set Speed (Rate)
    rate_option = rate_dropdown.get()
    rate_map = {'Fast': 250, 'Normal': 150, 'Slow': 60}
    engine.setProperty('rate', rate_map.get(rate_option, 150))
        
    # Set Voice (Gender)
    voices = engine.getProperty('voices')
    voice_type = voice_dropdown.get()
    
    # Logic to find the correct voice by checking the description
    chosen_voice = None
    for voice in voices:
        # We check if 'male' or 'female' is in the voice name/id (case insensitive)
        if voice_type.lower() in voice.name.lower():
            chosen_voice = voice.id
            break
            
    # Fallback: If we didn't find a match by name, use index 0 or 1
    if not chosen_voice:
        if voice_type == 'Male':
            chosen_voice = voices[0].id
        else:
            chosen_voice = voices[1].id if len(voices) > 1 else voices[0].id

    engine.setProperty('voice', chosen_voice)
    return engine


def play_voice():
    content = input_box.get(1.0, END).strip()
    if not content:
        messagebox.showwarning("Warning", "Please enter some text first!")
        return

    try:
        engine = get_configured_engine()
        engine.say(content)
        engine.runAndWait()
        # Explicitly stop to reset the engine state for the next click
        engine.stop()
    except Exception as e:
        messagebox.showerror("Error", f"Speech Error: {e}")

def save_audio():
    content = input_box.get(1.0, END).strip()
    if not content:
        messagebox.showwarning("Warning", "Please enter some text first!")
        return

    directory = filedialog.askdirectory()
    if directory:
        try:
            # Change to selected directory
            os.chdir(directory)
            engine = get_configured_engine()
            # Save to file
            filename = "audio.mp3"
            engine.save_to_file(content, filename)
            engine.runAndWait()
            messagebox.showinfo("Success", f"File saved successfully in {directory}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

# --- UI Layout ---

# Application Icon
try:
    icon_image = PhotoImage(file="speak.png")
    app.iconphoto(False, icon_image)
except:
    pass # Falls back to default if image is missing

# Header Section
header = Frame(app, bg="#292C7B", width=900, height=100)
header.place(x=0, y=0)

try:
    logo_image = PhotoImage(file="Speakerr (1).png")
    Label(header, image=logo_image, bg="#292C7B").place(x=10, y=5)
except:
    pass

Label(header, text="VOICE GENERATOR", font="arial 20 bold", bg="#292C7B", fg="white").place(x=100, y=30)

# Text Input Area
text_frame = Frame(app, bg="white")
text_frame.place(x=10, y=150, width=500, height=250)

scrollbar = Scrollbar(text_frame)
scrollbar.pack(side=RIGHT, fill=Y)

input_box = Text(text_frame, font="Roboto 16", bg="white", relief=GROOVE, wrap=WORD, yscrollcommand=scrollbar.set)
input_box.pack(expand=True, fill=BOTH)
scrollbar.config(command=input_box.yview)

# Controls (Dropdowns)
Label(app, text="VOICE", font="arial 12 bold", bg="#F9F4EF", fg="black").place(x=550, y=160)
voice_dropdown = Combobox(app, values=['Male', 'Female'], font='arial 12', state='readonly', width=12)
voice_dropdown.place(x=550, y=190)
voice_dropdown.set('Male')

Label(app, text="SPEED", font="arial 12 bold", bg="#F9F4EF", fg="black").place(x=730, y=160)
rate_dropdown = Combobox(app, values=['Slow', 'Normal', 'Fast'], font='arial 12', state='readonly', width=12)
rate_dropdown.place(x=730, y=190)
rate_dropdown.set('Normal')

# Buttons
try:
    speak_icon = PhotoImage(file="humans.png")
    speak_button = Button(app, text=" Speak", compound=LEFT, image=speak_icon, width=130, bg="white", font="arial 12 bold", command=play_voice)
except:
    speak_button = Button(app, text="Speak", width=15, bg="white", font="arial 12 bold", command=play_voice)
speak_button.place(x=550, y=280)

try:
    save_icon = PhotoImage(file="download-Photoroom (1).png")
    save_button = Button(app, text=" Save", compound=LEFT, image=save_icon, width=130, bg="white", font="arial 12 bold", command=save_audio)
except:
    save_button = Button(app, text="Save", width=15, bg="white", font="arial 12 bold", command=save_audio)
save_button.place(x=730, y=280)

app.mainloop()