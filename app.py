from flask import Flask, render_template
from flask_socketio import SocketIO
import os
from scripts.image_predictor import SamImagePredictor
from matplotlib import pyplot as plt
from scripts.utils import show_image
import yaml

main_path = os.path.dirname(os.path.abspath(__file__))
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

checkpoint = os.path.join(main_path, config['checkpoint'])
onnx_model = os.path.join(main_path, config['onnx_model'])
images_folder = os.path.join(main_path, config['images_folder'])
model_type = config['model_type']

sam = SamImagePredictor(checkpoint, onnx_model, model_type)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

images = [os.path.join(images_folder, f) for f in os.listdir(images_folder)]
image_index = 0

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('click')
def click(event):
    x, y = event['x'], event['y']
    
    # if x and y outside image, return
    if x < 0 or y < 0 or x > sam.image.shape[1] or y > sam.image.shape[0]:
        return
    else:
        img_data = sam.calculate_position(x, y)
    
    
    socketio.emit('show_image', img_data)

@socketio.on('get_image')
def get_image():
    global image_index
    image_path = images[image_index]
    image_index = (image_index + 1) % len(images)
    sam.set_image(image_path)
    
    img_data = show_image(sam.image)

    socketio.emit('show_image', img_data)
    
    
if __name__ == '__main__':
    socketio.run(app)
    

