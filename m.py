import tkinter as tk
from tkinter import filedialog, messagebox
import vlc
import os

class MiniMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Mini Music Player")
        self.root.geometry("420x400")

        # VLC player setup
        self.player = vlc.MediaPlayer()

        # Playlist
        self.playlist = []
        self.current_index = 0
        self.is_paused = False

        # Playlist box
        self.listbox = tk.Listbox(root, bg="lightgray", width=55, height=12)
        self.listbox.pack(pady=20)

        # Control buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Songs", width=10, command=self.add_songs).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Play", width=10, command=self.play_song).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Pause/Resume", width=12, command=self.pause_resume).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Stop", width=10, command=self.stop_song).grid(row=0, column=3, padx=5)

        nav_frame = tk.Frame(root)
        nav_frame.pack(pady=10)

        tk.Button(nav_frame, text="Previous", width=10, command=self.prev_song).grid(row=0, column=0, padx=10)
        tk.Button(nav_frame, text="Next", width=10, command=self.next_song).grid(row=0, column=1, padx=10)

        # Label showing current song
        self.song_label = tk.Label(root, text="No song playing", fg="blue")
        self.song_label.pack(pady=10)

    def add_songs(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav")])
        for file in files:
            self.playlist.append(file)
            self.listbox.insert(tk.END, os.path.basename(file))

    def play_song(self):
        if not self.playlist:
            messagebox.showwarning("Warning", "No songs in playlist. Please add songs first.")
            return

        selected = self.listbox.curselection()
        if selected:
            self.current_index = selected[0]

        song = self.playlist[self.current_index]
        self.player.set_media(vlc.Media(song))
        self.player.play()
        self.is_paused = False

        self.song_label.config(text=f"Playing: {os.path.basename(song)}")
        self.listbox.select_clear(0, tk.END)
        self.listbox.select_set(self.current_index)

    def pause_resume(self):
        if self.player.is_playing():
            self.player.pause()
            self.is_paused = True
            self.song_label.config(text="Paused")
        elif self.is_paused:
            self.player.play()
            self.is_paused = False
            current_song = os.path.basename(self.playlist[self.current_index])
            self.song_label.config(text=f"Playing: {current_song}")

    def stop_song(self):
        self.player.stop()
        self.song_label.config(text="No song playing")

    def next_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play_song()

    def prev_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play_song()

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniMusicPlayer(root)
    root.mainloop()
