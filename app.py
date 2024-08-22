from flask import Flask, render_template, request, send_from_directory
import os
from werkzeug.utils import secure_filename
from utils import allowed_file, ensure_directory_exists
from face_recognition import find_matching_images
import atexit

app = Flask(__name__)

# Directories for dataset and results
DATASET_FOLDER = 'static/dataset/'
RESULT_FOLDER = 'static/results/'

# Ensure the result directory exists
ensure_directory_exists(RESULT_FOLDER)

def cleanup():
    """Delete all files in the result folder when the app closes."""
    if os.path.exists(RESULT_FOLDER):
        for filename in os.listdir(RESULT_FOLDER):
            file_path = os.path.join(RESULT_FOLDER, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

atexit.register(cleanup)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded target image
        target_image = request.files.get('target_image')
        
        if target_image and allowed_file(target_image.filename):
            target_filename = secure_filename(target_image.filename)
            target_path = os.path.join(RESULT_FOLDER, target_filename)
            target_image.save(target_path)
            
            # Find matching images in the dataset
            matching_images = find_matching_images(target_path, RESULT_FOLDER)
            
            return render_template('results.html', images=matching_images)
        
    return render_template('index.html')

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(RESULT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
