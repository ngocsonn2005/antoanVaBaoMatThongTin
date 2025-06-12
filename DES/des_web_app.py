from flask import Flask, render_template, request, send_file
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import io

app = Flask(__name__)

# Hàm tạo đối tượng mã hóa DES từ key người dùng nhập
def get_des_cipher(key_str):
    key = key_str.encode('utf-8')
    if len(key) < 8:
        key = key.ljust(8, b'0')  # Bổ sung bằng số 0 nếu chưa đủ
    else:
        key = key[:8]  # Cắt nếu dài quá
    return DES.new(key, DES.MODE_ECB)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        key = request.form.get('key')
        file = request.files.get('file')

        if not file or not key:
            return "⚠️ Vui lòng chọn file và nhập khóa!", 400

        file_bytes = file.read()
        filename = file.filename

        cipher = get_des_cipher(key)
        try:
            if action == 'encrypt':
                result_bytes = cipher.encrypt(pad(file_bytes, DES.block_size))
                output_filename = 'encrypted_' + filename
            elif action == 'decrypt':
                result_bytes = unpad(cipher.decrypt(file_bytes), DES.block_size)
                output_filename = 'decrypted_' + filename
            else:
                return "Hành động không hợp lệ!", 400
        except ValueError:
            return "❌ Giải mã thất bại: Sai khóa hoặc dữ liệu không hợp lệ.", 400

        return send_file(
            io.BytesIO(result_bytes),
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/octet-stream'
        )

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
