import time
import matplotlib.pyplot as plt
import threading
import subprocess

from Tracker import Tracker
from datetime import datetime

# Data shown on the plot represents the last 5 minutes
DATA_DURATION = 5
# The data variable
speeds_recv = []
speeds_sent = []
times = []

def table():
    subprocess.call("Bandwidth_monitor_table.py", shell=True)

def graph():
    """ Executes the program.
    """
    tracker = Tracker()
    plt.ion()

    while True:
        # Retrieve the up and down speeds
        time.sleep(0.5)
        down_speed = tracker.get_current_download_speed() / (2**20)
        up_speed = tracker.get_current_upload_speed() / (2**20)

        # Store it
        add_data(down_speed, up_speed)

        # Update & display the plot
        recv_curve, = plt.plot(times, speeds_recv)
        sent_curve, = plt.plot(times, speeds_sent)

        plt.legend([recv_curve, sent_curve], ['Download', 'Upload'])
        plt.ylabel('MB/s', fontsize=8)
        ax = plt.gca()
        ax.tick_params(axis='x', labelsize=6)
        ax.tick_params(axis='y', labelsize=6)
        ax.get_figure().canvas.set_window_title('Bandwidth monitor')

        plt.draw()
        plt.pause(0.0001)
        plt.clf()

        def add_data(down_speed, up_speed):
    if len(times) > 1:
        if (times[-1] - times[0]).total_seconds() // 60 >= DATA_DURATION:
            del times[0]
            del speeds_recv[0]
            del speeds_sent[0]
    speeds_recv.append(down_speed)
    speeds_sent.append(up_speed)
    times.append(datetime.now())

if __name__ == '__main__':
    try:
        threading.Thread(target=graph).start()
        threading.Thread(target=table).start()
    except:
        print("An exception occurred")
