import rsa

# Tạo cặp khóa 2048-bit
(public_key, private_key) = rsa.newkeys(2048)

# Lưu private key
with open("private_key.pem", "wb") as priv_file:
    priv_file.write(private_key.save_pkcs1())

# Lưu public key
with open("public_key.pem", "wb") as pub_file:
    pub_file.write(public_key.save_pkcs1())

print("Đã tạo xong private_key.pem và public_key.pem")
