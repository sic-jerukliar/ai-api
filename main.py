from flask import Flask, request, jsonify
from utils import VerifyFaceByImage, VerifyFaceByBase64, RecognizeFace

app = Flask(__name__)

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
    try:
        base64_img = request.files.get('img')
        stud_id = request.form.get('studId')

        if not base64_img or not stud_id:
            return jsonify({"error": "Missing 'img' or 'studId'"}), 400

        result = RecognizeFace(base64_img, stud_id)
        return jsonify({"verified": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
