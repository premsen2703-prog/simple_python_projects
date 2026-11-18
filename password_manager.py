
import os
import json
import base64
import secrets
import string
import msvcrt

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


FILE_NAME = "passwords.enc"


# ==========================================
# 1. SECURE PASSWORD INPUT (WINDOWS)
# ==========================================

def secure_input(prompt="Enter password: "):
    print(prompt, end="", flush=True)

    password = ""

    while True:
        char = msvcrt.getwch()

        if char == "\r":
            print()
            break

        elif char == "\x03":
            raise KeyboardInterrupt

        elif char == "\b":
            if password:
                password = password[:-1]
                print("\b \b", end="", flush=True)

        elif char in ("\x00", "\xe0"):
            msvcrt.getwch()

        else:
            password += char
            print("*", end="", flush=True)

    return password


# ==========================================
# 2. GENERATE ENCRYPTION KEY
# ==========================================

def generate_key(master_password, salt):

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000
    )

    key = base64.urlsafe_b64encode(
        kdf.derive(master_password.encode())
    )

    return key


# ==========================================
# 3. INITIALIZE PASSWORD MANAGER
# ==========================================

def initialize(master_password):

    salt = os.urandom(16)

    key = generate_key(master_password, salt)

    fernet = Fernet(key)

    encrypted_data = fernet.encrypt(
        json.dumps({}).encode()
    )

    with open(FILE_NAME, "wb") as file:
        file.write(salt + encrypted_data)

    return fernet


# ==========================================
# 4. LOAD ENCRYPTED DATA
# ==========================================

def load_data(master_password):

    with open(FILE_NAME, "rb") as file:
        content = file.read()

    if len(content) <= 16:
        print("Password database is damaged!")
        return None, None

    salt = content[:16]
    encrypted_data = content[16:]

    key = generate_key(master_password, salt)

    fernet = Fernet(key)

    try:
        decrypted_data = fernet.decrypt(encrypted_data)

        data = json.loads(decrypted_data.decode())

        if not isinstance(data, dict):
            print("Invalid password database format!")
            return None, None

        return fernet, data

    except (InvalidToken, ValueError, UnicodeDecodeError):
        print("Incorrect master password or damaged database!")
        return None, None


# ==========================================
# 5. SAVE ENCRYPTED DATA
# ==========================================

def save_data(fernet, data):

    encrypted_data = fernet.encrypt(
        json.dumps(data).encode()
    )

    with open(FILE_NAME, "rb") as file:
        salt = file.read(16)

    with open(FILE_NAME, "wb") as file:
        file.write(salt + encrypted_data)


# ==========================================
# 6. ADD PASSWORD
# ==========================================

def add_password(data):

    website = input("Enter website: ").strip()

    username = input("Enter username/email: ").strip()

    password = secure_input("Enter website password: ")

    if not website or not username or not password:
        print("All fields are required!")
        return

    data[website] = {
        "username": username,
        "password": password
    }

    print("Password added successfully!")


# ==========================================
# 7. VIEW PASSWORDS
# ==========================================

def view_passwords(data):

    if not data:
        print("No passwords saved.")
        return

    for website, details in data.items():

        print("\nWebsite:", website)
        print("Username:", details["username"])
        print("Password:", details["password"])


# ==========================================
# 8. SEARCH PASSWORD
# ==========================================

def search_password(data):

    website = input("Enter website to search: ").strip()

    if website in data:

        print("\nWebsite:", website)
        print("Username:", data[website]["username"])
        print("Password:", data[website]["password"])

    else:
        print("Website not found!")


# ==========================================
# 9. UPDATE PASSWORD
# ==========================================

def update_password(data):

    website = input("Enter website to update: ").strip()

    if website in data:

        username = input("Enter new username: ").strip()

        password = secure_input("Enter new password: ")

        if username:
            data[website]["username"] = username

        if password:
            data[website]["password"] = password

        print("Password updated successfully!")

    else:
        print("Website not found!")


# ==========================================
# 10. DELETE PASSWORD
# ==========================================

def delete_password(data):

    website = input("Enter website to delete: ").strip()

    if website in data:

        confirm = input(
            "Are you sure you want to delete? (yes/no): "
        ).strip().lower()

        if confirm == "yes":
            del data[website]
            print("Password deleted successfully!")

        else:
            print("Deletion cancelled.")

    else:
        print("Website not found!")


# ==========================================
# 11. GENERATE STRONG PASSWORD
# ==========================================

def generate_password():

    try:
        length = int(input("Enter password length (8-128): "))

    except ValueError:
        print("Please enter a valid number!")
        return

    if length < 8 or length > 128:
        print("Choose a length between 8 and 128.")
        return

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    characters = lowercase + uppercase + digits + symbols

    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    password.extend(
        secrets.choice(characters)
        for _ in range(length - 4)
    )

    secrets.SystemRandom().shuffle(password)

    print("\nGenerated Password:", "".join(password))


# ==========================================
# 12. MAIN APPLICATION
# ==========================================

def main():

    print("=" * 45)
    print("       PYTHON PASSWORD MANAGER")
    print("=" * 45)

    if os.path.exists(FILE_NAME):

        print("\nExisting password database found.")

        master_password = secure_input(
            "Enter master password: "
        )

        fernet, data = load_data(master_password)

        if fernet is None:
            return

        print("\nLogin successful!")

    else:

        print("\nCreate your master password.")

        master_password = secure_input(
            "Enter master password: "
        )

        confirm_password = secure_input(
            "Confirm master password: "
        )

        if len(master_password) < 12:
            print("Master password must contain at least 12 characters.")
            return

        if master_password != confirm_password:
            print("Passwords do not match!")
            return

        fernet = initialize(master_password)

        data = {}

        print("\nPassword manager initialized successfully!")

    # MAIN MENU

    while True:

        print("\n========== MENU ==========")
        print("1. Add Password")
        print("2. View All Passwords")
        print("3. Search Password")
        print("4. Update Password")
        print("5. Delete Password")
        print("6. Generate Strong Password")
        print("7. Exit")
        print("==========================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            add_password(data)
            save_data(fernet, data)

        elif choice == "2":

            view_passwords(data)

        elif choice == "3":

            search_password(data)

        elif choice == "4":

            update_password(data)
            save_data(fernet, data)

        elif choice == "5":

            delete_password(data)
            save_data(fernet, data)

        elif choice == "6":

            generate_password()

        elif choice == "7":

            print("\nThank you for using Password Manager!")
            print("Goodbye!")
            break

        else:

            print("Invalid choice! Please try again.")


# ==========================================
# 13. START PROGRAM
# ==========================================

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")

    except Exception as error:
        print("\nUnexpected error:", error)
