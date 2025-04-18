import os
import base64
from io import BytesIO
from PIL import Image
from deepface import DeepFace
import cv2 as cv
import numpy as np
from scipy.spatial import distance
from pickle import load

def check_antispoofing(img_path):
    result = DeepFace.extract_faces(img_path)
    print("RESULT: ", type(result))
    print("RESULT: ", result)
    
    return False

def RecognizeFace(uploaded_img, studId, trehsohld=0.75):
    receive_image_path = "temp_received_image.jpg"
    embedfile = f"identityimage/{studId}/{studId}.pkl"
    
    if not os.path.isfile(embedfile):
        return 'Data Wajah tidak valid, Tidak pernah terdaftar'
    
    receive_image = Image.open(uploaded_img)
    receive_image.save(receive_image_path)
    
    # image_array = np.array(receive_image)
    # imgS = cv.cvtColor(image_array, cv.COLOR_BGR2RGB)
    encodeImage = None
    
    try:
        # check anti spoofing
        # antispoofing = check_antispoofing(receive_image_path)
        # print(antispoofing)
        # if antispoofing:
        #     return 'Anti Spoofing Terdeteksi'
        
        # load data pickle
        with open(embedfile, "rb") as f:
            embeddata = load(f)
        
        # encode image
        encodeImage = DeepFace.represent(
            receive_image_path,
            enforce_detection=False
        )
        encodeImage = encodeImage[0]["embedding"]
        
        for embed_item in embeddata['data']:
            try:
                dist = distance.cosine(encodeImage, embed_item)
                if dist < (1 - trehsohld):
                    return True
            except Exception as e:
                return e
    
    finally :
        os.remove(receive_image_path)
    
    return False
