import hashlib

def hash_data(data):
    sha256 = hashlib.sha256(data.encode()).hexdigest()
    sha512 = hashlib.sha512(data.encode()).hexdigest()
    return sha256, sha512

# Nhập dữ liệu GỐC (không sửa)
original_data = input("Nhập dữ liệu KHÔNG SỬA: ")
hash256_original, hash512_original = hash_data(original_data)

print("\n--- Kết quả Băm DỮ LIỆU KHÔNG SỬA ---")
print("SHA-256:", hash256_original)
print("SHA-512:", hash512_original)

# Nhập dữ liệu ĐÃ SỬA
modified_data = input("\nNhập dữ liệu ĐÃ SỬA: ")
hash256_modified, hash512_modified = hash_data(modified_data)

print("\n--- Kết quả Băm DỮ LIỆU ĐÃ SỬA ---")
print("SHA-256:", hash256_modified)
print("SHA-512:", hash512_modified)

# So sánh
print("\n=== So sánh ===")
if hash256_original != hash256_modified:
    print("❌ SHA-256 khác nhau → Dữ liệu đã bị thay đổi!")
else:
    print("✅ SHA-256 giống nhau → Dữ liệu chưa bị thay đổi.")

if hash512_original != hash512_modified:
    print("❌ SHA-512 khác nhau → Dữ liệu đã bị thay đổi!")
else:
    print("✅ SHA-512 giống nhau → Dữ liệu chưa bị thay đổi.")
