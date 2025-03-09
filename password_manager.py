from cryptography.fernet import Fernet
import json
import os

# File untuk menyimpan password
db_file = "passwords.json"
key_file = "key.key"

# Fungsi untuk membuat dan menyimpan kunci enkripsi
def generate_key():
    key = Fernet.generate_key()
    with open(key_file, "wb") as keyfile:
        keyfile.write(key)

def load_key():
    if not os.path.exists(key_file):
        generate_key()
    with open(key_file, "rb") as keyfile:
        return keyfile.read()

def encrypt_password(password, key):
    return Fernet(key).encrypt(password.encode()).decode()

def decrypt_password(encrypted_password, key):
    return Fernet(key).decrypt(encrypted_password.encode()).decode()

def load_passwords():
    if os.path.exists(db_file):
        with open(db_file, "r") as file:
            return json.load(file)
    return {}

def save_passwords(passwords):
    with open(db_file, "w") as file:
        json.dump(passwords, file, indent=4)

def add_password(service, username, password):
    key = load_key()
    passwords = load_passwords()
    passwords[service] = {
        "username": username,
        "password": encrypt_password(password, key)
    }
    save_passwords(passwords)
    print("Password berhasil disimpan!")

def view_passwords():
    key = load_key()
    passwords = load_passwords()
    if not passwords:
        print("Belum ada password yang disimpan.")
        return
    for service, data in passwords.items():
        decrypted_pass = decrypt_password(data['password'], key)
        print(f"Service: {service}\nUsername: {data['username']}\nPassword: {decrypted_pass}\n")

def delete_password(service):
    passwords = load_passwords()
    if service in passwords:
        del passwords[service]
        save_passwords(passwords)
        print("Password berhasil dihapus!")
    else:
        print("Service tidak ditemukan.")

def main():
    while True:
        print("\nPassword Manager Sederhana")
        print("1. Tambah Password")
        print("2. Lihat Password")
        print("3. Hapus Password")
        print("4. Keluar")
        choice = input("Pilih opsi: ")

        if choice == "1":
            service = input("Masukkan nama layanan: ")
            username = input("Masukkan username: ")
            password = input("Masukkan password: ")
            add_password(service, username, password)
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            service = input("Masukkan nama layanan yang ingin dihapus: ")
            delete_password(service)
        elif choice == "4":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
