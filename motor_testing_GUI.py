# For the motors
from time import sleep
import RPi.GPIO as gpio
# For the GUI
import tkinter as tk
from tkinter import ttk, messagebox

# Setting up drivers and motors

# motor 1
direction_pin1 = 20
pulse_pin1 = 21

# directions:
# clockwise (cw) -> LOW
# counterclockwise (ccw) -> HIGH
cw_direction = gpio.LOW
ccw_direction = gpio.HIGH

# setting GPIO pin numbering system -> BCM (Broadcom SOC channel)
gpio.setmode(gpio.BCM)

# setting pins for motor 1
gpio.setup(direction_pin1, gpio.OUT)
gpio.setup(pulse_pin1, gpio.OUT)


def degreesToSteps(angle, steps_per_rev):
    steps = float(20.0 * (angle / 360.0) * steps_per_rev) # multiplying by 20, because we have a drive systme with 20:1 ratio
    return int(steps)

def step_motor(steps_per_rev, dt, direction, angle):
    print("Running motor with:")
    print(f"Steps/rev: {steps_per_rev}")
    print(f"dt (speed): {dt}")
    print(f"Direction: {direction}")
    print(f"Angle: {angle}")
    try:
        if direction == "CW":
            # setting clockwise direction for motor 1
            gpio.output(direction_pin1, cw_direction)
        elif direction == "CCW":
            # setting counterclockwise direction for motor 1
            gpio.output(direction_pin1, ccw_direction)
        else:
            messagebox.showerror("Error", "Invalid direction")
            return

        maxSteps = degreesToSteps(angle, steps_per_rev)
        for currentStep in range(maxSteps):
                # stepping motor 1
                gpio.output(pulse_pin1, gpio.HIGH)
                sleep(dt)  # Adjust this to control motor speed
                gpio.output(pulse_pin1, gpio.LOW)

    except KeyboardInterrupt:
        gpio.cleanup()


def run_motor():
    try:
        steps_per_rev = int(steps_entry.get())
        dt = float(dt_entry.get())
        angle = float(angle_entry.get())
        direction = direction_var.get()

        step_motor(steps_per_rev, dt, direction, angle)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

# GUI

# Main window
root = tk.Tk()
root.title("Stepper Motor Control")
root.geometry("450x400")

# Style font
FONT = ("Arial", 15)

# --- Steps per revolution ---
ttk.Label(root, text="Steps per revolution:", font=FONT).pack(pady=(15, 0))
steps_entry = ttk.Entry(root, font=FONT)
steps_entry.insert(0, "6400")
steps_entry.pack()

# --- dt (speed) ---
ttk.Label(root, text="dt (speed):", font=FONT).pack(pady=(15, 0))
dt_entry = ttk.Entry(root, font=FONT)
dt_entry.insert(0, "0.001")
dt_entry.pack()

# --- Angle ---
ttk.Label(root, text="Angle to step:", font=FONT).pack(pady=(15, 0))
angle_entry = ttk.Entry(root, font=FONT)
angle_entry.pack()

# --- Direction radio buttons ---
direction_var = tk.StringVar(value="CW")

ttk.Label(root, text="Direction:", font=FONT).pack(pady=(15, 0))

frame = ttk.Frame(root)
frame.pack()

ttk.Radiobutton(frame, text="Clockwise", variable=direction_var, value="CW").pack(side="left", padx=10)
ttk.Radiobutton(frame, text="Counter Clockwise", variable=direction_var, value="CCW").pack(side="left", padx=10)

# --- Execute button ---
ttk.Button(root, text="Run Motor", command=run_motor).pack(pady=25)

# Run app
root.mainloop()