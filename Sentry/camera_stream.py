from flask import Flask, render_template, Response
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

app = Flask(__name__)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# Load pre-trained classifiers
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')

def generate_frames():
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array

        # Convert image to grayscale for detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
      # Detect full bodies
        bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Draw rectangles around bodies
        for (x, y, w, h) in bodies:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()

        # Yield the output frame in byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        rawCapture.truncate(0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

