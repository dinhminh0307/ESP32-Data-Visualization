import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import time

# Initialize serial port - Replace 'COM3' with your port
ser = serial.Serial('COM7', 115200)

# Prepare deques for storing data and time
data_anglex = deque(maxlen=100)
data_angley = deque(maxlen=100)
data_anglez = deque(maxlen=100)
timestamps = deque(maxlen=100)

# Prepare deques for motor data
data_motor1 = deque(maxlen=100)
data_motor2 = deque(maxlen=100)
data_motor3 = deque(maxlen=100)
data_motor4 = deque(maxlen=100)

# Modify read_serial to include motor data reading
def read_serial():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            parts = line.split(" ")
            anglex, angley, anglez = map(float, parts[:3])
            motor1, motor2, motor3, motor4 = map(float, parts[3:7])  # Assuming motor data follows angle data

            # Append angle and motor data
            data_anglex.append(anglex)
            data_angley.append(angley)
            data_anglez.append(anglez)
            data_motor1.append(motor1)
            data_motor2.append(motor2)
            data_motor3.append(motor3)
            data_motor4.append(motor4)
            timestamps.append(time.time())

# Function to animate angle data
def animate_angles(i):
    ax_angles.clear()
    if timestamps:
        ax_angles.plot(timestamps, data_anglex, label='Angle X')
        ax_angles.plot(timestamps, data_angley, label='Angle Y')
        ax_angles.plot(timestamps, data_anglez, label='Angle Z')
        ax_angles.axhline(y=0, color='r', linestyle='-', label='Setpoint')
        ax_angles.legend(loc='upper left')
        ax_angles.set_xlabel('Time (s)')
        ax_angles.set_ylabel('Angle Value')
        start_time = timestamps[0]
        ax_angles.set_xticklabels([f"{x - start_time:.2f}" for x in ax_angles.get_xticks()])

# Function to animate motor data
def animate_motors(i):
    ax_motors.clear()
    if timestamps:
        ax_motors.plot(timestamps, data_motor1, label='Motor 1')
        ax_motors.plot(timestamps, data_motor2, label='Motor 2')
        ax_motors.plot(timestamps, data_motor3, label='Motor 3')
        ax_motors.plot(timestamps, data_motor4, label='Motor 4')
        ax_motors.legend(loc='upper left')
        ax_motors.set_xlabel('Time (s)')
        ax_motors.set_ylabel('Motor Value')
        start_time = timestamps[0]
        ax_motors.set_xticklabels([f"{x - start_time:.2f}" for x in ax_motors.get_xticks()])

# Set up two separate figures for angles and motors
fig_angles, ax_angles = plt.subplots()
fig_motors, ax_motors = plt.subplots()

# Start animation for both figures
ani_angles = animation.FuncAnimation(fig_angles, animate_angles, interval=100)
ani_motors = animation.FuncAnimation(fig_motors, animate_motors, interval=100)

import threading
thread = threading.Thread(target=read_serial)
thread.daemon = True
thread.start()

# Show the plot
plt.show()