import os
import base64
from io import BytesIO
from PIL import Image
from deepface import DeepFace
import cv2 as cv
import numpy as np
from scipy.spatial import distance
from pickle import load
import psycopg2
from dotenv import load_dotenv

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

def connect_db():
    load_dotenv()
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT")),
            sslmode='require'
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None

def get_table_data(table_name, column_names):
    conn = connect_db()
    cur = conn.cursor()
    try:
        columns = ", ".join(column_names)
        cur.execute(f"SELECT {columns} FROM {table_name}")
        rows = cur.fetchall()
        return [dict(zip(column_names, row)) for row in rows]
    finally:
        cur.close()
        conn.close()