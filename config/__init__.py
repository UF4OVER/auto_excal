# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

# 生成随机密钥和初始化向量
key = os.urandom(32)  # 256位密钥
iv = os.urandom(16)  # 128位初始化向量


# 加密函数
def encrypt_data(data, key=key, iv=iv):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_data).decode()


# 解密函数
def decrypt_data(encrypted_data, key=iv):
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return decrypted_data.decode()


# 示例使用
client_id = "Ov23liihJAbtWX6zyXr9"
client_secret = "22c66bfe6d83d341c787eadc5ca0a0218b3b6a75"

encrypted_client_id = encrypt_data(client_id, key, iv)
encrypted_client_secret = encrypt_data(client_secret, key, iv)

print("Encrypted Client ID:", encrypted_client_id)
print("Encrypted Client Secret:", encrypted_client_secret)

decrypted_client_id = decrypt_data(encrypted_client_id, key)
decrypted_client_secret = decrypt_data(encrypted_client_secret, key)

print("Decrypted Client ID:", decrypted_client_id)
print("Decrypted Client Secret:", decrypted_client_secret)
