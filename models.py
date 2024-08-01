from flask_sqlalchemy import SQLAlchemy
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        key = os.urandom(32)  # Key for Camellia (256 bits)
        iv = os.urandom(16)   # Initialization vector for Camellia
        cipher = Cipher(algorithms.Camellia(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_password = encryptor.update(password.encode()) + encryptor.finalize()
        self.password = key.hex() + iv.hex() + encrypted_password.hex()

    def check_password(self, password):
        key = bytes.fromhex(self.password[:64])
        iv = bytes.fromhex(self.password[64:96])
        encrypted_password = bytes.fromhex(self.password[96:])
        cipher = Cipher(algorithms.Camellia(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_password = decryptor.update(encrypted_password) + decryptor.finalize()
        return decrypted_password.decode() == password
