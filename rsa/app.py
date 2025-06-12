from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from rsa_utils import generate_keys, sign_file, verify_signature

app = Flask(__name__)
app.secret_key = 'secret123'
UPLOAD_FOLDER = os.path.abspath(os.path.join('rsa', 'uploads'))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign', methods=['POST'])
def sign():
    file = request.files['file']
    private_key = request.files['private_key']
    if not file or not private_key:
        flash('Vui lòng chọn file và khóa riêng!', 'danger')
        return redirect(url_for('index'))

    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(file_path)
    private_key_data = private_key.read()
    signature = sign_file(file_path, private_key_data)

    sig_path = file_path + '.sig'
    with open(sig_path, 'wb') as f:
        f.write(signature)

    flash('Ký thành công! Bạn có thể gửi cả file và chữ ký.', 'success')
    return render_template('index.html', signed_file=file.filename, sig_file=os.path.basename(sig_path))

@app.route('/verify')
def verify_page():
    return render_template('verify.html')

@app.route('/verify', methods=['POST'])
def verify():
    file = request.files['file']
    signature = request.files['signature']
    public_key = request.files['public_key']

    if not file or not signature or not public_key:
        flash('Vui lòng chọn đủ 3 tệp!', 'danger')
        return redirect(url_for('verify_page'))

    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    sig_path = os.path.join(UPLOAD_FOLDER, secure_filename(signature.filename))
    file.save(file_path)
    signature.save(sig_path)
    pub_key_data = public_key.read()

    with open(sig_path, 'rb') as f:
        sig_data = f.read()

    valid = verify_signature(file_path, sig_data, pub_key_data)
    if valid:
        flash('✅ Chữ ký hợp lệ! File không bị thay đổi.', 'success')
    else:
        flash('❌ Chữ ký KHÔNG hợp lệ hoặc file đã bị thay đổi!', 'danger')

    return redirect(url_for('verify_page'))

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
