from time import sleep
import RPi.GPIO as gpio

def degreesToSteps(angle):
    stepsPerRevolution = 6400 # we have 6400 steps (microsteps), in the current driver configuration
    steps = float(20.0 * (angle / 360.0) * stepsPerRevolution) # multiplying by 20, because we have a drive systme with 20:1 ratio
    return int(steps)

# motor 1
direction_pin1 = 20
pulse_pin1 = 21

# motor 2
#direction_pin2 = 19
#pulse_pin2 = 26

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

# setting pins for motor 2
#gpio.setup(direction_pin2, gpio.OUT)
#gpio.setup(pulse_pin2, gpio.OUT)

# setting direction for motor 1
gpio.output(direction_pin1, cw_direction)

# setting direction for motor 2
#gpio.output(direction_pin2, cw_direction)

try:
    while True:
        angle = float(input('Enter degrees: '))
        sleep(.5)
        maxSteps = degreesToSteps(angle)
        for currentStep in range(maxSteps):
                # stepping motor 1
                gpio.output(pulse_pin1, gpio.HIGH)
                sleep(0.001)  # Adjust this to control motor speed
                gpio.output(pulse_pin1, gpio.LOW)
                # stepping motor 2
                #gpio.output(pulse_pin2, gpio.HIGH)
                #sleep(0.001)
                #gpio.output(pulse_pin2, gpio.LOW)

except KeyboardInterrupt:
    gpio.cleanup()