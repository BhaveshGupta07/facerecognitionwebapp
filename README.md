# Face Recognition Web App

This Flask-based web application allows users to upload a target image and search through an existing dataset of images. The application identifies and returns all images from the dataset where the user's face appears.

## Features

- **User-Friendly Interface:** Easily upload a target image and get results through a simple web interface.
- **Face Recognition:** Uses MTCNN for face detection and InceptionResnetV1 for face recognition, pre-trained on VGGFace2.
- **Automatic Cleanup:** Automatically deletes the result images when the application is closed to keep the environment clean.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.6+
- Pip

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/face-recognition-webapp.git
    cd face-recognition-webapp
    ```

2. **Create a Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the Required Packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Prepare Your Dataset:**

    Place all the images you want to search through in the `static/dataset/` directory.

## Usage

1. **Start the Flask Application:**

    ```bash
    python app.py
    ```

2. **Open Your Web Browser:**

    Navigate to `http://127.0.0.1:5000/` in your web browser.

3. **Upload an Image:**

    - Upload a target image through the web interface.
    - The application will search the dataset and display all matching images.

