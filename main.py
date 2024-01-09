import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import time

# Initialize serial port - Replace 'COM3' with your port
ser = serial.Serial('COM4', 115200)

# Prepare deques for storing data and time
data_anglex = deque(maxlen=100)
data_angley = deque(maxlen=100)
data_anglez = deque(maxlen=100)
timestamps = deque(maxlen=100)

def read_serial():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            anglex, angley, anglez = map(float, line.split(" "))  # Split the line into parts and convert to float
            data_anglex.append(anglex)
            data_angley.append(angley)
            data_anglez.append(anglez)
            timestamps.append(time.time())  # Store the current time

def animate(i):
    ax.clear()
    if timestamps:
        ax.plot(timestamps, data_anglex, label='Angle X')
        ax.plot(timestamps, data_angley, label='Angle Y')
        ax.plot(timestamps, data_anglez, label='Angle Z')
        ax.axhline(y=0, color='r', linestyle='-', label='Setpoint')  # Setpoint line
        ax.legend(loc='upper left')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Angle Value')

        # Format x-axis to show elapsed time
        start_time = timestamps[0]
        ax.set_xticklabels([f"{x - start_time:.2f}" for x in ax.get_xticks()])

# Set up the plot
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, animate, interval=100)

# Read data from serial in a separate thread
import threading
thread = threading.Thread(target=read_serial)
thread.daemon = True
thread.start()

# Show the plot
plt.show()