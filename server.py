from flask import Flask, render_template, request, send_from_directory, send_file
import uuid
import io
import cv2
from PIL import Image
import numpy as np
import base64


app = Flask(__name__)


def serve_pil_image(pil_img):
    img_io = io.StringIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@app.route('/image/<path>')
def image(path):
    return send_from_directory('media', path)

@app.route('/home')
def home():

    return render_template("index.html")

@app.route('/resize', methods=['POST'])
def resized():
    # Unpack HTML form
    width = int(request.form['width'])
    height = int(request.form['height'])
    image = request.files['image']
    
    # Create random name
    # fake_name = str(uuid.uuid1())
    ext = image.filename.split('.')[-1]

    # Save img to /media
    # image.save(f'media/{fake_name}.{ext}')
    # Resize file
    image_obj = Image.open(io.BytesIO(image.read()))
    image_obj = image_obj.resize((width, height), Image.ANTIALIAS)
    image_obj = np.array(image_obj)
    print(image_obj.shape) 

    ret, buffer = cv2.imencode('.jpg', image_obj)
    frame = buffer.tobytes()
    data = io.BytesIO(frame)

    encoded_img_data = base64.b64encode(data.getvalue())
    # return send_file(io.BytesIO(frame),
    #                  mimetype='image/jpeg')
    return render_template('out.html', output=encoded_img_data.decode('utf-8'))

if __name__ == '__main__':
    app.run(debug=True, threaded=True)