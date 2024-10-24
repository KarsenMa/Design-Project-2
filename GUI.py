# Design Project 2 GUI

import tkinter as tk
from tkinter import scrolledtext
import serial
import threading

# Global flags
stop_reading_flag = False
pause_reading_flag = False

# Function to continuously read data from the serial port


def read_serial_data(serial_port, gps_labels, imu_labels):
    global stop_reading_flag, pause_reading_flag
    while not stop_reading_flag:
        if pause_reading_flag:
            continue  # If paused, skip reading data
        try:
            # Read data from the serial port
            if serial_port.in_waiting > 0:
                data = serial_port.readline().decode('utf-8').strip()
                # Simulate data update for demonstration
                gps_labels['satellites'].config(text="Satellites: 3")
                gps_labels['latitude'].config(text="Latitude: 36.177331")
                gps_labels['longitude'].config(text="Longitude: -96.836736")
                gps_labels['elevation'].config(
                    text="Elevation (MSL): 409.69 m")

                imu_labels['accel_x'].config(text="X Acceleration: -0.31 m/s²")
                imu_labels['accel_y'].config(text="Y Acceleration: -6.71 m/s²")
                imu_labels['accel_z'].config(text="Z Acceleration: 7.61 m/s²")

                imu_labels['magnetic_x'].config(
                    text="X Magnetic Field: -65.91 µT")
                imu_labels['magnetic_y'].config(
                    text="Y Magnetic Field: 30.64 µT")
                imu_labels['magnetic_z'].config(
                    text="Z Magnetic Field: 22.96 µT")

                imu_labels['gyro_x'].config(
                    text="X Angular Velocity: 0.01 rps")
                imu_labels['gyro_y'].config(
                    text="Y Angular Velocity: -0.02 rps")
                imu_labels['gyro_z'].config(
                    text="Z Angular Velocity: -0.02 rps")
        except Exception as e:
            print(f"Error reading serial port: {e}")

# Function to start reading data from the serial port


def start_reading(gps_labels, imu_labels):
    global stop_reading_flag, pause_reading_flag
    stop_reading_flag = False
    pause_reading_flag = False
    try:
        # Open the serial port (modify port and baudrate as needed)
        serial_port = serial.Serial(
            port_entry.get(), baudrate=int(baudrate_entry.get()), timeout=1)
        # Start the thread to read data from the serial port
        threading.Thread(target=read_serial_data, args=(
            serial_port, gps_labels, imu_labels), daemon=True).start()
    except Exception as e:
        print(f"Error: {e}")

# Function to pause reading data


def pause_reading():
    global pause_reading_flag
    pause_reading_flag = not pause_reading_flag  # Toggle pause state
    if pause_reading_flag:
        pause_button.config(text="Resume Display")
    else:
        pause_button.config(text="Pause Display")

# Function to reset GPS and IMU data display to all 0's


def clear_display():
    gps_labels['satellites'].config(text="Satellites: 0")
    gps_labels['latitude'].config(text="Latitude: 0.000000")
    gps_labels['longitude'].config(text="Longitude: 0.000000")
    gps_labels['elevation'].config(text="Elevation (MSL): 0.00 m")

    imu_labels['accel_x'].config(text="X Acceleration: 0.00 m/s²")
    imu_labels['accel_y'].config(text="Y Acceleration: 0.00 m/s²")
    imu_labels['accel_z'].config(text="Z Acceleration: 0.00 m/s²")

    imu_labels['magnetic_x'].config(text="X Magnetic Field: 0.00 µT")
    imu_labels['magnetic_y'].config(text="Y Magnetic Field: 0.00 µT")
    imu_labels['magnetic_z'].config(text="Z Magnetic Field: 0.00 µT")

    imu_labels['gyro_x'].config(text="X Angular Velocity: 0.00 rps")
    imu_labels['gyro_y'].config(text="Y Angular Velocity: 0.00 rps")
    imu_labels['gyro_z'].config(text="Z Angular Velocity: 0.00 rps")

# Function to stop reading and exit the application


def finish_session():
    global stop_reading_flag
    stop_reading_flag = True
    root.quit()


# Create the main window
root = tk.Tk()
root.title("GPS and IMU Data Display")
root.geometry("500x600")
root.configure(bg="white")

# Create the top buttons (Start, Pause, Clear, Finish)
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start Display", bg="green", fg="white", font=(
    "Arial", 14), width=15, command=lambda: start_reading(gps_labels, imu_labels))
start_button.grid(row=0, column=0, padx=10)

pause_button = tk.Button(button_frame, text="Pause Display", bg="orange",
                         fg="white", font=("Arial", 14), width=15, command=pause_reading)
pause_button.grid(row=0, column=1, padx=10)

clear_button = tk.Button(button_frame, text="Clear", bg="brown", fg="white", font=(
    "Arial", 14), width=15, command=clear_display)
clear_button.grid(row=1, column=0, padx=10)

finish_button = tk.Button(button_frame, text="Finish", bg="red", fg="white", font=(
    "Arial", 14), width=15, command=finish_session)
finish_button.grid(row=1, column=1, padx=10)

# Create the GPS and IMU data display area
display_frame = tk.Frame(root, bg="white", relief=tk.RAISED, borderwidth=2)
display_frame.pack(pady=10, padx=20, fill="both", expand=True)

# GPS Frame
gps_frame = tk.Frame(display_frame, bg="lightblue", padx=10, pady=5)
gps_frame.pack(pady=10, padx=20, fill="x")

tk.Label(gps_frame, text="GPS", bg="lightblue",
         font=("Arial", 16, "bold")).pack()

gps_labels = {
    "satellites": tk.Label(gps_frame, text="Satellites: 0", bg="lightblue", font=("Arial", 12)),
    "latitude": tk.Label(gps_frame, text="Latitude: 0.000000", bg="lightblue", font=("Arial", 12)),
    "longitude": tk.Label(gps_frame, text="Longitude: 0.000000", bg="lightblue", font=("Arial", 12)),
    "elevation": tk.Label(gps_frame, text="Elevation (MSL): 0.00 m", bg="lightblue", font=("Arial", 12))
}

for label in gps_labels.values():
    label.pack(anchor="w")

# IMU Frame
imu_frame = tk.Frame(display_frame, bg="lightyellow", padx=10, pady=5)
imu_frame.pack(pady=10, padx=20, fill="x")

tk.Label(imu_frame, text="IMU", bg="lightyellow",
         font=("Arial", 16, "bold")).pack()

imu_labels = {
    "accel_x": tk.Label(imu_frame, text="X Acceleration: 0.00 m/s²", bg="lightyellow", font=("Arial", 12)),
    "accel_y": tk.Label(imu_frame, text="Y Acceleration: 0.00 m/s²", bg="lightyellow", font=("Arial", 12)),
    "accel_z": tk.Label(imu_frame, text="Z Acceleration: 0.00 m/s²", bg="lightyellow", font=("Arial", 12)),

    "magnetic_x": tk.Label(imu_frame, text="X Magnetic Field: 0.00 µT", bg="lightyellow", font=("Arial", 12)),
    "magnetic_y": tk.Label(imu_frame, text="Y Magnetic Field: 0.00 µT", bg="lightyellow", font=("Arial", 12)),
    "magnetic_z": tk.Label(imu_frame, text="Z Magnetic Field: 0.00 µT", bg="lightyellow", font=("Arial", 12)),

    "gyro_x": tk.Label(imu_frame, text="X Angular Velocity: 0.00 rps", bg="lightyellow", font=("Arial", 12)),
    "gyro_y": tk.Label(imu_frame, text="Y Angular Velocity: 0.00 rps", bg="lightyellow", font=("Arial", 12)),
    "gyro_z": tk.Label(imu_frame, text="Z Angular Velocity: 0.00 rps", bg="lightyellow", font=("Arial", 12))
}

for label in imu_labels.values():
    label.pack(anchor="w")

# Create a label and entry for the serial port
tk.Label(root, text="Serial Port:", bg="white").pack()
port_entry = tk.Entry(root)
port_entry.pack(pady=5)
port_entry.insert(0, "COM3")  # Default value, change as needed for

# Create a label and entry for the baud rate
tk.Label(root, text="Baud Rate:", bg="white").pack()
baudrate_entry = tk.Entry(root)
baudrate_entry.pack(pady=5)
# Default value, change according to your device
baudrate_entry.insert(0, "9600")

# Start the Tkinter event loop
root.mainloop()
