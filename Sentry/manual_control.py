import curses
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import time

# Set up GPIO control using the pigpio factory
factory = PiGPIOFactory()

# Define pins for the servos
servo1_pin = 13  # Horizontal control (e.g., left-right)
servo2_pin = 12  # Vertical control (e.g., up-down)

# Initialize the servos
servo1 = Servo(servo1_pin, pin_factory=factory)
servo2 = Servo(servo2_pin, pin_factory=factory)

# Function to set the servo position and print a message
def set_servo_position(servo, position):
    servo.value = position
    print(f"Servo position set to {position}")

# Main function to handle the `curses` interface
def main(stdscr):
    # Initialize the current positions of the servos
    curr1 = 0
    curr2 = 0

    # Clear screen and display instructions
    stdscr.clear()
    stdscr.addstr(0, 0, "Control Servo1: 8 to increase, 5 to decrease | Control Servo2: 6 to increase, 4 to decrease | Press 'q' to quit\n")
    stdscr.addstr(2, 0, f"Servo1 Position: {curr1}, Servo2 Position: {curr2}")

    while True:
        # Wait for a single key press
        key = stdscr.getch()

        # Control Servo1 (Horizontal Movement)
        if key == ord('8') and curr1 < 1:  # Ensure the servo does not exceed the upper limit
            curr1 += 0.05
            set_servo_position(servo1, curr1)
        elif key == ord('5') and curr1 > -1:  # Ensure the servo does not exceed the lower limit
            curr1 -= 0.05
            set_servo_position(servo1, curr1)

        # Control Servo2 (Vertical Movement)
        elif key == ord('6') and curr2 < 1:  # Ensure the servo does not exceed the upper limit
            curr2 += 0.05
            set_servo_position(servo2, curr2)
        elif key == ord('4') and curr2 > -1:  # Ensure the servo does not exceed the lower limit
            curr2 -= 0.05
            set_servo_position(servo2, curr2)

        # Exit the program
        elif key == ord('q'):
            stdscr.addstr(4, 0, "Exiting the program.")
            stdscr.refresh()
            time.sleep(1)  # Pause for a moment before exiting
            break

        # Update the display with new positions
        stdscr.clear()
        stdscr.addstr(0, 0, "Control Servo1: 8 to increase, 5 to decrease | Control Servo2: 6 to increase, 4 to decrease | Press 'q' to quit\n")
        stdscr.addstr(2, 0, f"Servo1 Position: {curr1:.2f}, Servo2 Position: {curr2:.2f}")
        stdscr.refresh()

# Start the `curses` application
curses.wrapper(main)
