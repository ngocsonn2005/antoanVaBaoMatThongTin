import os
from crypto_utils import encrypt_aes, decrypt_aes_cbc, sign_data, verify_signature, hash_data
from crypto_utils import decrypt_aes_cbc

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.encrypted_data = None
        self.signature = None
        self.hash = None
        self.aes_key = os.urandom(32)  # Sử dụng khóa 256-bit cho AES
    
    def encrypt(self, key, iv):
        """Mã hóa thông tin giao dịch bằng AES-CBC"""
        try:
            data = f"{self.sender}|{self.receiver}|{self.amount}".encode()
            from crypto_utils import encrypt_aes
            self.encrypted_data = encrypt_aes(key, iv, data)
            return True
        except Exception as e:
            print("Encryption error:", e)
            return False

    def decrypt(self):
        """Giải mã thông tin giao dịch"""
        if not self.encrypted_data:
            return False
        decrypted_data = decrypt_aes_cbc(self.aes_key, self.encrypted_data)  # Sửa tên hàm
        return decrypted_data.decode()

    def sign(self, private_key):
        self.signature = sign_data(private_key, self.encrypted_data)

    def verify(self, public_key):
        return verify_signature(public_key, self.encrypted_data, self.signature)

    def generate_hash(self):
        self.hash = hash_data(self.encrypted_data)

    def verify_hash(self, received_hash):
        return self.hash == received_hash
