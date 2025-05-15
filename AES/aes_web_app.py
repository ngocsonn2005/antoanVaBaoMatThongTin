from flask import Flask, render_template, request, send_file
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import io

app = Flask(__name__)

# Hàm tạo đối tượng mã hóa AES từ key người dùng nhập
def get_aes_cipher(key_str):
    key = key_str.encode('utf-8')
    # Đảm bảo key có độ dài hợp lệ: 16, 24, 32 byte
    if len(key) < 16:
        key = key.ljust(16, b'0')  # Padding thêm 0 nếu ngắn
    elif len(key) > 32:
        key = key[:32]  # Cắt nếu quá dài
    elif len(key) not in [16, 24, 32]:
        # Nếu độ dài không phải 16, 24, 32 thì làm tròn lên gần nhất
        key = key.ljust(32, b'0') if len(key) > 24 else key.ljust(24, b'0')
    return AES.new(key, AES.MODE_ECB)

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

        cipher = get_aes_cipher(key)
        try:
            if action == 'encrypt':
                result_bytes = cipher.encrypt(pad(file_bytes, AES.block_size))
                output_filename = 'encrypted_' + filename
            elif action == 'decrypt':
                result_bytes = unpad(cipher.decrypt(file_bytes), AES.block_size)
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
