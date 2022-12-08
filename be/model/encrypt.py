import hashlib

def encrypt(password):
    pw = "2022" + password + "shudian"
    hash = hashlib.sha256()
    hash.update(pw.encode('utf-8'))
    return hash.hexdigest()