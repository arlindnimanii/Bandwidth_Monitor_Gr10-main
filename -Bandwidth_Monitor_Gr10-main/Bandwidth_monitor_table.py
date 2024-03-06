# NetworkBandwidthMonitor.py
# Written by: https://github.com/waterrmalann
# Written on: 15th May, 2020
# Written in: Python 3.7 w/ Tkinter

import tkinter as tk
from psutil import net_io_counters
from Tracker import Tracker

# Variables for use in the size() function.
KB = float(1024)
MB = float(KB ** 2) # 1,048,576
GB = float(KB ** 3) # 1,073,741,824
TB = float(KB ** 4) # 1,099,511,627,776

def size(B):
	B = float(B)
	if B < KB: return f"{B:.2f} Bytes"
	elif KB <= B < MB: return f"{B/KB:.2f} KB"
	elif MB <= B < GB: return f"{B/MB:.2f} MB"
	elif GB <= B < TB: return f"{B/GB:.2f} GB"
	elif TB <= B: return f"{B/TB:.2f} TB"

## Constants
WINDOW_SIZE = (400, 400)  # Width x Height
WINDOW_RESIZEABLE = False  # If the window is resizeable or not.
REFRESH_DELAY = 1000 # Window update delay in ms.

## Initializing
window = tk.Tk()

window.title("Network Bandwidth Monitor")  # Setting the window title.
window.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")  # Setting the window size.
window.resizable(width = WINDOW_RESIZEABLE, height = WINDOW_RESIZEABLE)  # We now lock the window.

label_total_upload_header = tk.Label(text = "Total Upload:", font = "Quicksand 12 bold")
label_total_upload_header.pack()
label_total_upload = tk.Label(text = "Calculating...", font = "Quicksand 12")
label_total_upload.pack()

label_total_download_header = tk.Label(text = "Total Download:", font = "Quicksand 12 bold")
label_total_download_header.pack()
label_total_download = tk.Label(text = "Calculating...", font = "Quicksand 12")
label_total_download.pack()

label_total_usage_header = tk.Label(text = "Total Usage:", font = "Quicksand 12 bold")
label_total_usage_header.pack()
label_total_usage = tk.Label(text = "Calculating...\n", font = "Quicksand 12")
label_total_usage.pack()

label_upload_header = tk.Label(text = "Upload speed:", font = "Quicksand 12 bold")
label_upload_header.pack()
label_upload = tk.Label(text = "Calculating...", font = "Quicksand 12")
label_upload.pack()

label_download_header = tk.Label(text = "Download speed:", font = "Quicksand 12 bold")
label_download_header.pack()
label_download = tk.Label(text = "Calculating...", font = "Quicksand 12")
label_download.pack()

tracker = Tracker()

# Updating Labels
def update():

	upload = tracker.__get_bytes_sent_total__() - tracker.init_total_sent
	download = tracker.__get_bytes_recv_total__() - tracker.init_total_recv
	total = upload + download

	down_speed = tracker.get_current_download_speed()
	up_speed = tracker.get_current_upload_speed()
	
	label_total_upload["text"] = f"{size(upload)} ({upload} Bytes)"
	label_total_download["text"] = f"{size(download)} ({download} Bytes)"
	label_total_usage["text"] = f"{size(total)}\n"
	
	label_upload["text"] = size(up_speed) + "/s"
	label_download["text"] = size(down_speed) + "/s"
	
	label_total_upload.pack()
	label_total_download.pack()
	label_total_usage.pack()
	label_upload.pack()
	label_download.pack()
	
	window.after(REFRESH_DELAY, update)  # reschedule event in refresh delay.

window.after(REFRESH_DELAY, update)
window.mainloop()

