import hashlib

# Hàm tính hash SHA-512 của file
def hash_file_sha512(file_path):
    sha512 = hashlib.sha512()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha512.update(chunk)
        return sha512.hexdigest()
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {file_path}")
        return None

# File gốc và file kiểm tra

file_goc = "băm/anhtkd.jpg"              
file_kiemtra = "băm/anhtkdKiemtra.jpg"          

# Băm cả 2 file
hash_goc = hash_file_sha512(file_goc)
hash_kt = hash_file_sha512(file_kiemtra)

# So sánh và in kết quả
if hash_goc and hash_kt:
    print("\n--- Mã băm SHA-512 ---")
    print(f"File gốc     : {hash_goc}")
    print(f"File kiểm tra: {hash_kt}")

    print("\n=== KẾT LUẬN ===")
    if hash_goc == hash_kt:
        print("✅ File không bị thay đổi. Tính toàn vẹn ĐƯỢC ĐẢM BẢO.")
    else:
        print("❌ File đã bị thay đổi. Tính toàn vẹn KHÔNG được đảm bảo.")
