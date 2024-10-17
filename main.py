#Progress bar for playlist needs to be fixed.
import os
from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
from pytubefix.exceptions import VideoUnavailable
import customtkinter as ctk
from customtkinter import filedialog


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def download_video():
    try:
        youtube_url = url.get()
        save_path = filedialog.askdirectory(initialdir=f'/home/{os.getlogin()}/Videos')
        if option_menu.get() == options[0]:
            yt = YouTube(youtube_url, on_progress_callback=on_progress)
            yt.streams.first().download(output_path=save_path)
        elif option_menu.get() == options[1]:
            yt = YouTube(youtube_url, on_progress_callback=on_progress)
            yt.streams.get_audio_only().download()
        elif option_menu.get() == options[2]:
            pl = Playlist(youtube_url)
            for video in pl.videos:
                try:
                    video.register_on_progress_callback(on_progress)
                    video.streams.first().download()
                except VideoUnavailable:
                    download_status_label.configure(text="Link not available, download skipped.")
        elif option_menu.get() == options[3]:
            pl = Playlist(youtube_url)
            for audio in pl.videos:
                try:
                    audio.register_on_progress_callback(on_progress)
                    out_file = audio.streams.get_audio_only().download(output_path=save_path)
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                except VideoUnavailable:
                    download_status_label.configure(text="Link not available, download skipped.")
        download_status_label.configure(text="File successfully downloaded!")
    except VideoUnavailable:
        download_status_label.config(text="Link not available.", text_color="red")


def on_progress(stream, chunk, bytes_remaining):
    file_size = stream.filesize
    bytes_downloaded = file_size - bytes_remaining
    percentage = bytes_downloaded / file_size * 100
    percent = str(int(percentage))
    progress_bar.set(float(percentage / 100))
    progress_bar_label.configure(text=f"{percent}%")
    progress_bar_label.update()


#Main window
root = ctk.CTk()
root.title("Youtube Video Downloader")
root.geometry("860x620")

options = ["Video", "Audio", "Playlist", "Playlist Audio"]


#UI
option_menu = ctk.CTkOptionMenu(root, values=options, font=("arial", 20))
url_label = ctk.CTkLabel(root, text="Paste the URL in the next box:", font=("arial", 20))
url = ctk.CTkEntry(root, width=600, height=35, border_width=1, font=("arial", 20))
btn_start = ctk.CTkButton(master=root, text="Download", command=download_video, font=("arial", 16), width=150, height=50)
progress_bar = ctk.CTkProgressBar(root, width=450)
progress_bar_label = ctk.CTkLabel(root, text="0%", font=("arial", 20))
download_status_label = ctk.CTkLabel(root, text='', font=("arial", 20))

progress_bar.set(0)

option_menu.pack(pady=(50, 10))
url_label.pack(pady=10)
url.pack()
btn_start.pack(pady=30)
progress_bar.pack(pady=10)
progress_bar_label.pack(pady=10)
download_status_label.pack(pady=10)


root.mainloop()



