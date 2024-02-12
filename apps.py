import os
import tkinter as tk
from tkinter import *
from pytube import YouTube
from tqdm import tqdm, trange
import time
from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar
import sqlite3
import pytube.exceptions

import threading

# Initialize the database and create tables if they don't exist
def initialize_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Downloads (
                        DownloadID INTEGER PRIMARY KEY,
                        UserID INTEGER,
                        VideoURL TEXT,
                        DownloadPath TEXT,
                        Quality VARCHAR,
                        DownloadDate DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
    conn.close()

# Function to log a download in the database
def log_download(user_id, video_url, download_path, quality):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Downloads (UserID, VideoURL, DownloadPath, Quality)
                      VALUES (?, ?, ?, ?)""", (user_id, video_url, download_path, quality))
    conn.commit()
    conn.close()

'''for i in tqdm(range(20)):
       time.sleep(0.3)'''

with tqdm(total=100) as pbar:
    for i in range(10):
        time.sleep(0.3)
        pbar.update(10) 
# Defining CreateWidgets() function
# to create necessary tkinter widgets
def Widgets():
    head_label = Label(root, text="YouTube Video Downloader:",
    padx=20,
    pady=20,
    font="SegoeUI 14",
    bg="blue",
    fg="white")
    head_label.grid(row=1,
    column=1, 
    pady=10, 
    padx=5, 
    columnspan=3)

    link_label = Label(root, 
    text="YouTube link:", 
    bg="blue", 
    pady=5, 
    padx=5, 
    fg="white")
    link_label.grid(row=2,
    column=0,
    pady=5, 
    padx=5)

    root.linkText = Entry(root, 
    width=35, 
    textvariable=video_Link, 
    font="Arial 14")
    root.linkText.grid(row=2, 
    column=1, 
    pady=5, 
    padx=5, 
    columnspan=2)

    destination_label = Label(root,
    text="Destination:", 
    bg="blue", 
    pady=5, 
    padx=5, 
    fg="white")
    destination_label.grid(row=3, 
    column=0, 
    pady=5, 
    padx=5)

    root.destinationText = Entry(root, width=27, 
    textvariable=download_Path, 
    font="Arial 14")
    root.destinationText.grid(row=3, 
    column=1, 
    pady=5, 
    padx=5)

    browse_B = Button(root,
    text="Browse", 
    command=Browse,
    width=10,
    bg="yellow",
    fg="black", 
    font="SegoeUI 11", 
    relief=GROOVE)
    browse_B.grid(row=3,
    column=2,
    pady=1,
    padx=1)

    quality_label = Label(root,
    text="Image Quality:",
    bg="blue", 
    pady=5, 
    padx=5, 
    fg="white")
    quality_label.grid(row=4,
    column=0,
    pady=5, 
    padx=5)

    # Add your own quality options here
    quality_options = ["High", 
    "Medium", 
    "Low"] 
    root.qualityVar = StringVar()
    root.qualityVar.set(quality_options[0])

    quality_dropdown = OptionMenu(root, 
    root.qualityVar,
    *quality_options)
    quality_dropdown.config(width=10)
    quality_dropdown.grid(row=4,
    column=1,
    pady=5,
    padx=5)

    Download_B = Button(root,
    text="Download Video",
    command=Download,
    width=20, 
    bg="blue", 
    fg="white", 
    pady=10, 
    padx=15, 
    relief=GROOVE, 
    font="Georgia, 13")
    Download_B.grid(row=5, 
    column=1, 
    pady=20, 
    padx=20)

    global progress_bar  # Declare the progress bar as a global variable to access it in other functions
    progress_bar = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
    progress_bar.grid(row=6, column=1, pady=20, padx=20, columnspan=2)

# Defining Browse() to select a destination folder to save the video
def Browse():
    download_Directory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH",
    title="Save Video")
    download_Path.set(download_Directory)


# Callback function to track download progress
def progress_function(stream, chunk, bytes_remaining):
    file_size = stream.filesize
    bytes_downloaded = file_size - bytes_remaining
    progress = int((bytes_downloaded / file_size) * 100)
    progress_bar['value'] = progress
    root.update_idletasks()  # This is necessary to update the GUI

# Defining Download() to download the video
def Download():
    print("Starting download")
    # Getting user-input YouTube Link
    Youtube_link = video_Link.get()

    # Selecting the optimal location for saving files
    download_Folder = download_Path.get()

    try:
        # Creating object of YouTube()
        getVideo = YouTube(Youtube_link, on_progress_callback=progress_function)

        # Getting all the available streams of the YouTube video and selecting the first
        videoStream = getVideo.streams.first()

        # Getting the resolution of the video
        resolution = videoStream.resolution

        def _download():
            # Downloading the video to the destination directory
            videoStream.download(download_Folder)

            # Log the download in the database
            log_download(1, Youtube_link, download_Folder, root.qualityVar.get())

            # Displaying the message
            messagebox.showinfo("SUCCESSFULLY", 
            f"DOWNLOADED AND SAVED IN\n{download_Folder}\nResolution: {resolution}")

            # Additional code for image quality
            image_quality = root.qualityVar.get()
            print(f"Image quality: {image_quality}")
        
        download_thread = threading.Thread(target=_download)
        download_thread.start()
    except pytube.exceptions.AgeRestrictedError:
        messagebox.showerror("Download Failed", "This video is age-restricted and cannot be downloaded.")

# Creating object of tk class
root = tk.Tk()

# Setting the title, background color and size of the tkinter window and disabling the resizing property
root.geometry("520x320")
root.resizable(False, False)
root.title("YouTube Video Downloader")
root.config(background="blue")

# Creating the tkinter Variables
video_Link = StringVar()
download_Path = StringVar()

# Calling the Widgets() function
Widgets()

# Defining infinite loop to run the application
root.mainloop()