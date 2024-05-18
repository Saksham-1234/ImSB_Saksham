import os
from flask import Flask, request, render_template
from PIL import Image
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

G1, C1 = 40, 16
G2, C2 = 255, 1

def calculate_concentration(G):
    if G1 == G2:
        raise ValueError("G1 and G2 cannot be the same value")
    return C1 + (C2 - C1) * (G - G1) / (G2 - G1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        img = Image.open(filepath)
        img = img.convert('RGB')
        pixels = np.array(img)
        
        G_values = pixels[:, :, 1]
        G_avg = np.mean(G_values)
        
        concentration = calculate_concentration(G_avg)
        rounded_number = round(concentration, 2)
        
        return render_template('index.html', concentration=rounded_number)
    
    return "File upload failed"

if __name__ == "__main__":
    app.run()
