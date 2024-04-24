import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import pypianoroll
import numpy as np
from PIL import Image, ImageTk

#TODO Fix issues on visualizer for the pianoroll plot

class MidiPlayerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("MIDI Player")
        self.master.geometry("1000x350")
        self.master.configure(bg="#f0f0f0")

        # Navigation Bar
        self.nav_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)

        import_img = Image.open("assets/import_icon.png").resize((24, 24))
        self.import_icon = ImageTk.PhotoImage(import_img)
        self.import_label = tk.Label(self.nav_frame, image=self.import_icon, bg="#f0f0f0", cursor="hand2")
        self.import_label.pack(side=tk.LEFT, padx=10)
        self.import_label.bind("<Button-1>", self.import_midi)

        play_img = Image.open("assets/play_icon.png").resize((24, 24))
        self.play_icon = ImageTk.PhotoImage(play_img)
        self.play_label = tk.Label(self.nav_frame, image=self.play_icon, bg="#f0f0f0", cursor="hand2")
        self.play_label.pack(side=tk.LEFT, padx=10)
        self.play_label.bind("<Button-1>", self.play_midi)

        pause_img = Image.open("assets/pause_icon.png").resize((24, 24))
        self.pause_icon = ImageTk.PhotoImage(pause_img)
        self.pause_label = tk.Label(self.nav_frame, image=self.pause_icon, bg="#f0f0f0", cursor="hand2")
        self.pause_label.pack(side=tk.LEFT, padx=10)
        self.pause_label.bind("<Button-1>", self.pause_midi)

        # Canvas for Visualization
        self.canvas = tk.Canvas(self.master, bg="white", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.midi_file = None
        self.playing = False
        self.image_refs = []

    def import_midi(self, event):
        file_path = filedialog.askopenfilename(filetypes=[("MIDI files", "*.mid")])
        if file_path:
            self.midi_file = file_path
            self.visualize_multitrack_piano_roll()

    def play_midi(self, event):
        if self.midi_file:
            if not self.playing:
                pygame.mixer.init()
                pygame.mixer.music.load(self.midi_file)
                pygame.mixer.music.play()
                self.playing = True
        else:
            print("No MIDI file selected.")

    def pause_midi(self, event):
        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False

    def visualize_multitrack_piano_roll(self):
        if self.midi_file:
            multitrack = pypianoroll.read(self.midi_file)

            num_tracks = len(multitrack.tracks)
            max_length = max(len(track.pianoroll) for track in multitrack.tracks)
            downbeats = multitrack.get_downbeat_steps()

            canvas_height = num_tracks * 50
            canvas_width = max_length * 2

            self.canvas.config(width=canvas_width, height=canvas_height)

            for i, track in enumerate(multitrack.tracks):
                piano_roll = track.pianoroll
                resized_piano_roll = np.repeat(piano_roll[:, :, np.newaxis], 3, axis=2) * 255
                image = Image.fromarray(resized_piano_roll.astype(np.uint8))
                photo_image = ImageTk.PhotoImage(image.resize((canvas_width, 50)))
                self.image_refs.append(photo_image)  # Store reference to prevent garbage collection
                self.canvas.create_image(0, i * 50, anchor=tk.NW, image=photo_image)

def main():
    root = tk.Tk()
    app = MidiPlayerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
