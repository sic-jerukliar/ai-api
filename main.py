import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, request, jsonify, send_from_directory, render_template_string
from utils import RecognizeFace, get_table_data
import os
from datetime import datetime
from dotenv import load_dotenv

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
load_dotenv()

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

@app.route('/show')
def show_image():
    files = os.listdir(UPLOAD_FOLDER)
    # Filter hanya file gambar
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    if not image_files:
        return jsonify({"error": "No image found"}), 404

    latest_image = sorted(image_files)[-1]
    return send_from_directory(UPLOAD_FOLDER, latest_image)

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

# TUGAS IJAL
@app.route('/recap')
def recap():
    smtp_server = os.getenv("EMAIL_SMTP")
    smtp_port = os.getenv("EMAIL_PORT")
    sender_email = os.getenv("EMAIL_SENDER")
    sender_password = os.getenv("EMAIL_PASSWORD")

    users = get_table_data('users', ['email', 'nama'])

    def create_message(user):
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = user['email']
        msg['Subject'] = f"Monthly Attendance Recap for {user['nama']}"

        body = f"""
            Dear Parent,
            
            This is the monthly attendance recap for {user['nama']}.
            
            Attendance details for {datetime.now().strftime('%B %Y')}:
            - Total present: X days
            - Total absent: Y days
            
            Best regards,
            School Administration
            """
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        return msg

    def send_emails_batch(user_batch):
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)

                for user in user_batch:
                    try:
                        msg = create_message(user)
                        server.send_message(msg)
                    except Exception as e:
                        print(f"Error sending email to {user['email']}: {str(e)}")
        except Exception as e:
            print(f"Batch sending error: {str(e)}")

    try:
        from concurrent.futures import ThreadPoolExecutor
        from math import ceil

        # Split users into batches of 10
        batch_size = 10
        user_batches = [users[i:i + batch_size] for i in range(0, len(users), batch_size)]

        # Use thread pool to send emails in parallel
        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(send_emails_batch, user_batches)

        return jsonify({"message": "Recap emails sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to send emails: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
