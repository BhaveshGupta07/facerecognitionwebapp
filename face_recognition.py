import cv2
import torch
import numpy as np
from mtcnn import MTCNN
from facenet_pytorch import InceptionResnetV1
import os
from shutil import copyfile

# Initialize MTCNN for face detection and InceptionResnetV1 for face recognition
detector = MTCNN()
recognizer = InceptionResnetV1(pretrained='vggface2').eval()

def process_image(image_path):
    """Process an image to extract face embeddings."""
    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not load image {image_path}")
        return None
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(image_rgb)
    if not faces:
        return None
    
    face_embeddings = []
    for face in faces:
        x, y, w, h = face['box']
        face_img = image_rgb[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (160, 160))
        face_img = torch.tensor(face_img).permute(2, 0, 1).float().unsqueeze(0) / 255.0
        
        with torch.no_grad():
            embedding = recognizer(face_img).numpy()
        
        embedding = embedding / np.linalg.norm(embedding)
        face_embeddings.append(embedding)
    
    return face_embeddings

def find_matching_images(target_photo_path, result_folder, dataset_folder='static/dataset/', threshold=0.9):
    """Find images in the dataset folder that match the target image."""
    target_embeddings = process_image(target_photo_path)
    if target_embeddings is None:
        return []
    
    matching_images = []
    for photo_filename in os.listdir(dataset_folder):
        photo_path = os.path.join(dataset_folder, photo_filename)
        image_embeddings = process_image(photo_path)
        if image_embeddings is None:
            continue
        
        match_found = False
        for target_embedding in target_embeddings:
            for image_embedding in image_embeddings:
                distance = np.linalg.norm(target_embedding - image_embedding)
                if distance < threshold:
                    match_found = True
                    break
            if match_found:
                break
        
        if match_found:
            result_path = os.path.join(result_folder, photo_filename)
            copyfile(photo_path, result_path)
            matching_images.append(photo_filename)
    
    return matching_images
