from flask import Flask, render_template, Response, request
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

app = Flask(__name__)

# Use the pigpio pin factory for better PWM control
factory = PiGPIOFactory()

# Define GPIO pins for the servos
servo1_pin = 12
servo2_pin = 13

# Initialize the servos with the pigpio pin factory
servo1 = Servo(servo1_pin, pin_factory=factory)
servo2 = Servo(servo2_pin, pin_factory=factory)

# Initialize the camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=(640, 480))

# Function to control continuous rotation servo speed and direction
def control_servo(servo, speed):
    if speed < -1:
        speed = -1
    elif speed > 1:
        speed = 1
    servo.value = speed

# Route to stream the video
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()

        # Yield the output frame in byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        rawCapture.truncate(0)

# Route to control servos
@app.route('/control', methods=['POST'])
def control():
    if 'servo1_left' in request.form:
        control_servo(servo1, -1)
    elif 'servo1_right' in request.form:
        control_servo(servo1, 1)
    elif 'servo2_up' in request.form:
        control_servo(servo2, 1)
    elif 'servo2_down' in request.form:
        control_servo(servo2, -1)
    return ('', 204)

# Route to stop servos
@app.route('/stop', methods=['POST'])
def stop():
    control_servo(servo1, 0)
    control_servo(servo2, 0)
    return ('', 204)

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='192.168.1.23', port=5000)