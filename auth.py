import bcrypt
import os

USER_DATA_FILE = "users.txt"

# Hash a password
def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

# Verify a password against a stored hash
def verify_password(plaintext_password, stored_hash):
    encoded_password = plaintext_password.encode('utf-8')
    encoded_hash = stored_hash.encode('utf-8')
    return bcrypt.checkpw(encoded_password, encoded_hash)


#Temporary test code - remove after testing
test_password = "Magic123#"

# Check if user exists in file
def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            stored_username = line.strip().split(',')[0]
            if stored_username == username:
                return True
    return False

# Register a new user
def register_user(username, password):
    if user_exists(username):
        print(f"Username '{username}' already exists. Please choose another.")
        return False
    hashed_password = hash_password(password)
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username},{hashed_password}\n")
    print(f"User '{username}' registered successfully.")
    return True

# Login user
def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        print("No users registered yet.")
        return False
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            stored_username, stored_hash = line.strip().split(',')
            if stored_username == username:
                if verify_password(password, stored_hash):
                    return True
                else:
                    print("Incorrect password.")
                    return False
    print("Username not found.")
    return False

# Validate username (basic check)
def validate_username(username):
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if ',' in username:
        return False, "Username cannot contain commas."
    return True, ""

# Validate password strength
def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not any(c.islower() for c in password):
        return False, "Password must contain a lowercase letter."
    if not any(c.isupper() for c in password):
        return False, "Password must contain an uppercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain a digit."
    if not any(c in "!@#$%^&*()-_=+[]{}|;:',.<>?/" for c in password):
        return False, "Password must contain a special character."
    return True, ""

# Display menu
def display_menu():
    print("\n1. Register User")
    print("2. Login User")
    print("3. Exit")

# Main loop
def main():
    print("\nWelcome to the Week 7 Authentication System!")
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            register_user(username, password)

        elif choice == '2':
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            if login_user(username, password):
                print("\nYou are now logged in.")
            input("\nPress Enter to return to main menu...")

        elif choice == '3':
            print("\nThank you for using the authentication system.")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()

