from Crypto.Cipher import AES
import hashlib
import os
import base64

def generate_key(password):
    return hashlib.sha256(password.encode()).digest()

def pad(data):
    return data + (16 - len(data) % 16) * chr(16 - len(data) % 16)

def unpad(data):
    return data[:-ord(data[-1])]

def encrypt(data, password):
    key = generate_key(password)
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data).encode())
    return base64.b64encode(iv + encrypted_data).decode()

def decrypt(encrypted_data, password):
    key = generate_key(password)
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data[16:])).decode()
    return decrypted_data

def encrypt_file(file_path, password):
    with open(file_path, 'rb') as f:
        data = f.read()
    encrypted_data = encrypt(data.decode(errors='ignore'), password)
    with open(file_path + ".enc", 'w') as f:
        f.write(encrypted_data)
    print("File encrypted successfully.")

def decrypt_file(file_path, password):
    with open(file_path, 'r') as f:
        encrypted_data = f.read()
    decrypted_data = decrypt(encrypted_data, password)
    with open(file_path.replace(".enc", ""), 'w', encoding='utf-8') as f:
        f.write(decrypted_data)
    print("File decrypted successfully.")

if __name__ == "__main__":
    print("Advanced Encryption Tool")
    print("1. Encrypt Text")
    print("2. Decrypt Text")
    print("3. Encrypt File")
    print("4. Decrypt File")
    choice = input("Choose an option: ")
    
    if choice == "1":
        text = input("Enter text to encrypt: ")
        password = input("Enter encryption password: ")
        encrypted_text = encrypt(text, password)
        print("Encrypted:", encrypted_text)
    elif choice == "2":
        encrypted_text = input("Enter text to decrypt: ")
        password = input("Enter decryption password: ")
        try:
            decrypted_text = decrypt(encrypted_text, password)
            print("Decrypted:", decrypted_text)
        except:
            print("Error: Invalid password or corrupted data.")
    elif choice == "3":
        file_path = input("Enter file path to encrypt: ")
        password = input("Enter encryption password: ")
        encrypt_file(file_path, password)
    elif choice == "4":
        file_path = input("Enter file path to decrypt: ")
        password = input("Enter decryption password: ")
        decrypt_file(file_path, password)
    else:
        print("Invalid choice.")
