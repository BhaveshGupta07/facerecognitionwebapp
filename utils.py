import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_directory_exists(directory):
    """Ensure that a directory exists, and create it if it doesn't."""
    if not os.path.exists(directory):
        os.makedirs(directory)
