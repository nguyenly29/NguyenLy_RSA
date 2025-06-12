# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json  # 🧠 BẠT BUỘC
from werkzeug.utils import secure_filename
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import base64
from flask import send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/download/<filename>')
def download_json(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "Không tìm thấy file"}), 404

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        print("Lỗi đọc JSON:", e)
        return jsonify({"error": "Lỗi đọc file"}), 500


@app.route('/')
def home():
    return render_template('sender.html')

@app.route('/receiver')
def receiver():
    return render_template('receiver.html')

@app.route('/sign', methods=['POST'])
def sign_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(filepath)

    with open(filepath, 'rb') as f:
        data = f.read()

    # Tạo khóa RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Ký dữ liệu
    signature = private_key.sign(
        data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    # Xuất public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Tạo file chứa chữ ký và public key
    signed_info = {
        "filename": filename,
        "signature": base64.b64encode(signature).decode(),
        "public_key": base64.b64encode(public_pem).decode()
    }

    # Ghi ra file JSON đính kèm
    sig_json_path = filepath + ".signed.json"
    with open(sig_json_path, "w") as f:
        json.dump(signed_info, f)

    return jsonify({
    "message": "File đã được ký và tạo file chữ ký JSON.",
    "signature_file": filename + ".signed.json",
    "signature": signed_info["signature"],
    "public_key": signed_info["public_key"]
})




@app.route('/verify', methods=['POST'])
def verify_file():
    file = request.files['file']
    data = file.read()

    # Đọc chữ ký và khóa từ form text
    try:
        signature = base64.b64decode(request.form['signature'])
        public_key_pem = base64.b64decode(request.form['public_key'])

        public_key = serialization.load_pem_public_key(
            public_key_pem, backend=default_backend()
        )

        public_key.verify(
            signature,
            data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return jsonify({"valid": True})
    except Exception as e:
        print("LỖI XÁC MINH:", e)
        return jsonify({"valid": False})


app.run(host="0.0.0.0", port=5000, debug=True)