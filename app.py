from flask import Flask, render_template, Response
import os
from cam import VideoCamera
import cv2

app = Flask(__name__, template_folder='templates')

overlay_image = []
header_img = "Images"
header_img_list = os.listdir(header_img)
for i in header_img_list:
    image = cv2.imread(f'{header_img}/{i}')
    overlay_image.append(image)


@app.route('/')
def index():
    return render_template('index.html')


def gen():
    cam1 = VideoCamera(overlay_image=overlay_image)
    print("VideoCamera initialized")

    while True:
        frame = cam1.get_frame(overlay_image=overlay_image)
        if frame is None:
            print("Frame is None")
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    print("Video feed requested")
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
