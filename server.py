from flask import Flask, Response, request
import threading

app = Flask(__name__)

# Buffer to store the most recent frame
latest_frame = None
frame_lock = threading.Lock()

@app.route('/')
def index():
    return Response("It works!")
@app.route('/upload', methods=['POST'])
def upload():
    global latest_frame
    with frame_lock:
        latest_frame = request.data
    return 'Frame received', 200

def generate_video_stream():
    global latest_frame
    while True:
        with frame_lock:
            if latest_frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
