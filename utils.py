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

def VerifyFaceByBase64(base64_img, studId):
    identity_image_path = f'identityimage/{studId}'
    
    # Decode base64 menjadi image
    decoded_img = base64.b64decode(base64_img)
    receive_image = Image.open(BytesIO(decoded_img))
    print(receive_image)
    receive_image_path = "temp_received_image.jpg"
    receive_image.save(receive_image_path)

    # Loop semua gambar referensi
    for image_filename in os.listdir(identity_image_path):
        img2_path = os.path.join(identity_image_path, image_filename)
        try:
            print(receive_image_path)
            result = DeepFace.verify(
                img1_path=receive_image_path,
                img2_path=img2_path,
                enforce_detection=False
            )
            if result['verified']:
                return True
        except Exception as e:
            print(f"Error comparing to {img2_path}: {e}")
            raise e
    
    return False  # Tidak ada wajah yang cocok

def VerifyFaceByImage(uploaded_img, studId):
    identity_image_path = f'identityimage/{studId}'

    # Simpan file upload ke file sementara
    receive_image = Image.open(uploaded_img)
    receive_image_path = "temp_received_image.jpg"
    receive_image.save(receive_image_path)

    # Loop semua gambar referensi
    for image_filename in os.listdir(identity_image_path):
        img2_path = os.path.join(identity_image_path, image_filename)
        try:
            result = DeepFace.verify(
                img1_path=receive_image_path,
                img2_path=img2_path,
                enforce_detection=False,
            )
            if result['verified']:
                os.remove(receive_image_path)
                return True
        except Exception as e:
            print(f"Error comparing to {img2_path}: {e}")
            raise e
        
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
            # model_name="Facenet",
            # detector_backend="mtcnn",
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
