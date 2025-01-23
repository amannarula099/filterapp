from flask import Flask, render_template, request, send_file, url_for
from PIL import Image, ImageOps
import os

app = Flask(__name__)

# Folders for uploaded and processed images
UPLOAD_FOLDER = 'static/uploaded_images'
PROCESSED_FOLDER = 'static/processed_images'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No file part", 400
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return render_template('index.html', uploaded_image=file.filename)

@app.route('/process/<filter_type>/<filename>')
def process_image(filter_type, filename):
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(PROCESSED_FOLDER, filename)

    if not os.path.exists(input_path):
        return "Image not found", 404

    image = Image.open(input_path)

    # Apply selected filter
    if filter_type == 'greyscale':
        processed_image = ImageOps.grayscale(image)
    elif filter_type == 'blackandwhite':
        processed_image = image.convert('1')  # Black and white filter
    else:
        return "Invalid filter type", 400

    processed_image.save(output_path)
    return render_template(
        'index.html',
        uploaded_image=filename,
        processed_image=url_for('static', filename='processed_images/' + filename)
    )

@app.route('/download/<filename>')
def download_image(filename):
    output_path = os.path.join(PROCESSED_FOLDER, filename)
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    else:
        return "File not found", 404

if __name__ == '__main__':
    # Updated to bind to 0.0.0.0 and use port 10000 as required by Render
    app.run(host='0.0.0.0', port=10000, debug=True)
