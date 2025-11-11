"""
source https://github.com/AttilaTheDog/hybridunifier_changed
!pip install pycryptodome
"""
from base64 import b64encode as be, b64decode as bd
from Crypto.Util.number import getPrime, long_to_bytes as l2b
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from secrets import randbelow
from hashlib import sha256
import os, json

class SecureSession:
    def __init__(self, bits):
        self.bits = bits
        self.g = 2
        self.p = getPrime(self.bits)
        self.compute_server_public_key()
        self.reset_challenge()
        self.initialized = False

    def compute_server_public_key(self):
        self.a = randbelow(self.p)
        self.server_public_key = pow(self.g, self.a, self.p)
    
    def establish_session_key(self, client_public_key):
        key = pow(client_public_key, self.a, self.p)
        self.session_key = sha256(str(key).encode()).digest()

    def reset_challenge(self):
        self.challenge = os.urandom(24)
    
    def validate_challenge(self, challenge_hash):
        validated = challenge_hash == sha256(self.challenge).hexdigest()
        if validated:
            self.reset_challenge()
        return validated

    def encrypt_packet(self, packet):
        iv = os.urandom(16)
        cipher = AES.new(self.session_key, AES.MODE_CBC, iv)
        encrypted_packet = iv + cipher.encrypt(pad(packet.encode(), 16))
        return {'packet_data': be(encrypted_packet).decode()}

    def decrypt_packet(self, packet):
        decoded_packet = bd(packet.encode())
        iv = decoded_packet[:16]
        encrypted_packet = decoded_packet[16:]
        cipher = AES.new(self.session_key, AES.MODE_CBC, iv)
        try:
            decrypted_packet = unpad(cipher.decrypt(encrypted_packet), 16)
            packet_data = decrypted_packet.decode()
        except:
            return {'error': 'Malformed packet.'}
        
        return {'packet_data': packet_data}

    def get_encrypted_challenge(self):
        iv = os.urandom(16)
        cipher = AES.new(self.session_key, AES.MODE_CBC, iv)
        encrypted_challenge = iv + cipher.encrypt(pad(self.challenge, 16))
        return be(encrypted_challenge)