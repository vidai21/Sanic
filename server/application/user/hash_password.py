import hashlib

def hash_password(password):
    hash = hashlib.sha512(password).hexdigest()
    return hash