
# 🔐 Ứng dụng truyền file có ký số bằng RSA

Ứng dụng web đơn giản sử dụng Flask cho phép người dùng:

- Tải lên file và ký số bằng thuật toán RSA.
- Tạo và lưu cặp khóa RSA (công khai & riêng).
- Tạo chữ ký số cho file tải lên.
- Xác minh tính toàn vẹn file bằng chữ ký số.
- Giao diện web hiện đại, dễ sử dụng.

---


## 🧰 Công nghệ sử dụng

- Python 
- Flask
- Thư viện [`rsa`]
- HTML + CSS 

---

## 🛠️ Cài đặt & chạy thử



### 1. Cài thư viện cần thiết

pip install flask rsa
```

### 2. Chạy ứng dụng


python rsa/app.py



## 📁 Cấu trúc thư mục

```
rsa/
├── app.py
├── generate_key.py
├── rsa_utils.py
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── uploads/



