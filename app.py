from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import cv2
import numpy as np
import uuid

app = Flask(__name__, static_folder='static', template_folder='templates')

# Directories
MODEL_DIR = "/Users/apple/Documents/project/OK/my_project/model"
IMAGE_DIR = "/Users/apple/Documents/project/OK/my_project/static/images"
UPLOAD_FOLDER = "/Users/apple/Documents/project/OK/my_project/static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy user store (can be replaced by a database later)
users = {}

# Home route
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check credentials
        if username in users and users[username]['password'] == password:
            return redirect(url_for('colorizer'))
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'})

    return render_template('Amarjit.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if username in users:
            return jsonify({'success': False, 'error': 'Username already exists'})
        
        users[username] = {'email': email, 'password': password}
        return redirect(url_for('login'))

    return render_template('signup.html')

# Colorizer route
@app.route('/colorizer', methods=['GET', 'POST'])
def colorizer():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file part'})

        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No selected file'})

        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return jsonify({'success': False, 'error': 'Invalid file type. Please upload an image.'})

        # Save uploaded file
        unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(upload_path)

        try:
            # Colorize image
            colorized_image = colorize_image(upload_path)
            colorized_image_path = os.path.join(IMAGE_DIR, 'colorized_' + unique_filename)
            cv2.imwrite(colorized_image_path, colorized_image)
            return jsonify({'success': True, 'image_path': f'/static/images/colorized_{unique_filename}'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    return render_template('colorizer.html')

# Colorization logic
def colorize_image(image_path):
    PROTOTXT = os.path.join(MODEL_DIR, "colorization_deploy_v2.prototxt")
    MODEL = os.path.join(MODEL_DIR, "colorization_release_v2.caffemodel")
    POINTS = os.path.join(MODEL_DIR, "pts_in_hull.npy")

    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
    pts = np.load(POINTS)
    pts = pts.transpose().reshape(2, 313, 1, 1)

    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image not found: {image_path}")

    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")

    return colorized

if __name__ == '__main__':
    app.run(debug=True, port=5001)