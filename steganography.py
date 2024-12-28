import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import wave
import os

# Helper Functions for Image Steganography
def encode_image(image_path, secret_message, output_image):
    try:
        image = Image.open(image_path)
        encoded = image.copy()
        width, height = image.size
        message_bits = ''.join([format(ord(char), '08b') for char in secret_message]) + '00000000'

        if len(message_bits) > width * height * 3:
            raise ValueError("Message too long to fit in the image.")

        idx = 0
        for y in range(height):
            for x in range(width):
                pixel = list(image.getpixel((x, y)))
                for n in range(3):
                    if idx < len(message_bits):
                        pixel[n] = (pixel[n] & ~1) | int(message_bits[idx])
                        idx += 1
                encoded.putpixel((x, y), tuple(pixel))

        encoded.save(output_image)
        messagebox.showinfo("Success", f"Message successfully hidden in {output_image}.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decode_image(image_path):
    try:
        image = Image.open(image_path)
        width, height = image.size
        message_bits = []

        for y in range(height):
            for x in range(width):
                pixel = image.getpixel((x, y))
                for n in range(3):
                    message_bits.append(pixel[n] & 1)

        message_bytes = [message_bits[i:i + 8] for i in range(0, len(message_bits), 8)]
        message = ''.join([chr(int(''.join(map(str, byte)), 2)) for byte in message_bytes])

        if "\x00" in message:
            message = message[:message.index("\x00")]

        messagebox.showinfo("Hidden Message", message)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Helper Functions for Audio Steganography
def encode_audio(audio_path, secret_message, output_audio):
    try:
        audio = wave.open(audio_path, 'rb')
        frames = bytearray(list(audio.readframes(audio.getnframes())))
        message_bits = ''.join([format(ord(char), '08b') for char in secret_message]) + '00000000'

        if len(message_bits) > len(frames):
            raise ValueError("Message too long to fit in the audio file.")

        for i in range(len(message_bits)):
            frames[i] = (frames[i] & ~1) | int(message_bits[i])

        with wave.open(output_audio, 'wb') as output:
            output.setparams(audio.getparams())
            output.writeframes(bytes(frames))

        audio.close()
        messagebox.showinfo("Success", f"Message successfully hidden in {output_audio}.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decode_audio(audio_path):
    try:
        audio = wave.open(audio_path, 'rb')
        frames = bytearray(list(audio.readframes(audio.getnframes())))

        message_bits = [frames[i] & 1 for i in range(len(frames))]
        message_bytes = [message_bits[i:i + 8] for i in range(0, len(message_bits), 8)]
        message = ''.join([chr(int(''.join(map(str, byte)), 2)) for byte in message_bytes])

        if "\x00" in message:
            message = message[:message.index("\x00")]

        messagebox.showinfo("Hidden Message", message)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Functions
def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
    return file_path

def upload_audio():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    return file_path

def hide_in_image():
    image_path = upload_image()
    if not image_path:
        return
    secret_message = message_entry.get()
    if not secret_message:
        messagebox.showerror("Error", "Please enter a message to hide.")
        return
    output_image = os.path.join(os.getcwd(), "hidden_image.png")
    encode_image(image_path, secret_message, output_image)

def extract_from_image():
    image_path = upload_image()
    if not image_path:
        return
    decode_image(image_path)

def hide_in_audio():
    audio_path = upload_audio()
    if not audio_path:
        return
    secret_message = message_entry.get()
    if not secret_message:
        messagebox.showerror("Error", "Please enter a message to hide.")
        return
    output_audio = os.path.join(os.getcwd(), "hidden_audio.wav")
    encode_audio(audio_path, secret_message, output_audio)

def extract_from_audio():
    audio_path = upload_audio()
    if not audio_path:
        return
    decode_audio(audio_path)

# GUI Setup
root = tk.Tk()
root.title("Steganography Tool")
root.geometry("500x350")  # Adjusting size for better layout

# Instructions label
instructions_label = tk.Label(root, text="Welcome to the Steganography Tool! \nHide and extract secret messages in images or audio.", font=("Helvetica", 12), pady=10)
instructions_label.pack()

message_label = tk.Label(root, text="Enter the secret message you want to hide:")
message_label.pack(pady=5)
message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=5)

# Buttons for hiding/extracting in images
image_frame = tk.Frame(root)
image_frame.pack(pady=10)
image_hide_button = tk.Button(image_frame, text="Hide Message in Image", command=hide_in_image, width=20)
image_hide_button.grid(row=0, column=0, padx=5)
image_extract_button = tk.Button(image_frame, text="Extract Message from Image", command=extract_from_image, width=20)
image_extract_button.grid(row=0, column=1, padx=5)

# Buttons for hiding/extracting in audio
audio_frame = tk.Frame(root)
audio_frame.pack(pady=10)
audio_hide_button = tk.Button(audio_frame, text="Hide Message in Audio", command=hide_in_audio, width=20)
audio_hide_button.grid(row=0, column=0, padx=5)
audio_extract_button = tk.Button(audio_frame, text="Extract Message from Audio", command=extract_from_audio, width=20)
audio_extract_button.grid(row=0, column=1, padx=5)

root.mainloop()
