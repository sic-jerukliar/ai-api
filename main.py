from flask import Flask, request, jsonify, send_from_directory, render_template_string
from utils import VerifyFaceByImage, VerifyFaceByBase64, RecognizeFace
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{now}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, 'wb') as f:
        f.write(request.data)
    print(f"Saved {filename}")
    return "Image received!", 200

@app.route('/')
def gallery():
    files = os.listdir(UPLOAD_FOLDER)
    images_html = ''.join(
        f'<div><img src="/uploads/{file}" width="400"><p>{file}</p></div>' for file in sorted(files, reverse=True)
    )
    return render_template_string(f"""
    <html>
      <head><title>ESP32-CAM Gallery</title></head>
      <body>
        <h1>Uploaded Images</h1>
        {images_html}
      </body>
    </html>
    """)

@app.route('/uploads/<filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/image/verifystudents', methods=['POST'])
def verifybyImage():
    try:
        base64_img = request.files.get('img')
        stud_id = request.form.get('studId')

        if not base64_img or not stud_id:
            return jsonify({"error": "Missing 'img' or 'studId'"}), 400

        result = VerifyFaceByImage(base64_img, stud_id)
        return jsonify({"verified": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/baseimage/verifystudents', methods=['POST'])
def verifybyBase64():
    try:
        base64_img = request.files.get('img')
        stud_id = request.form.get('studId')

        if not base64_img or not stud_id:
            return jsonify({"error": "Missing 'img' or 'studId'"}), 400

        result = VerifyFaceByBase64(base64_img, stud_id)
        return jsonify({"verified": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/verifystudents', methods=['POST'])
def verify():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    uploaded_img = f"image_{now}.jpg"
    uploaded_img = os.path.join(UPLOAD_FOLDER, uploaded_img)
    with open(uploaded_img, 'wb') as f:
        f.write(request.data)

    stud_id = request.headers.get('X-UID')

    if not uploaded_img or not stud_id:
        return jsonify({"error": "Missing 'img' or 'studId'"}), 400

    result = RecognizeFace(uploaded_img, stud_id)
    print(result)
    return jsonify({"verified": result}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
