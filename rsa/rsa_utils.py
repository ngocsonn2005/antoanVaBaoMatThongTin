import rsa
import hashlib

def generate_keys():
    (pub_key, priv_key) = rsa.newkeys(2048)
    return pub_key, priv_key

def sign_file(file_path, private_key_data):
    private_key = rsa.PrivateKey.load_pkcs1(private_key_data)
    with open(file_path, 'rb') as f:
        data = f.read()
    hash_value = hashlib.sha256(data).digest()
    signature = rsa.sign(hash_value, private_key, 'SHA-256')
    return signature

def verify_signature(file_path, signature, public_key_data):
    public_key = rsa.PublicKey.load_pkcs1(public_key_data)
    with open(file_path, 'rb') as f:
        data = f.read()
    hash_value = hashlib.sha256(data).digest()
    try:
        rsa.verify(hash_value, signature, public_key)
        return True
    except rsa.VerificationError:
        return False
