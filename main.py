from auth import register_user, login_user, validate_username, validate_password
# Display menu
def display_menu():
    print("\n1. Register User")
    print("2. Login User")
    print("3. Exit")

# Main loop
def main():
    while True:
        display_menu()
        choice = input("Choose an option: ").strip()
        if choice == '1':
            username = input("Enter username: ").strip()
            valid, msg = validate_username(username)
            if not valid:
                print(msg)
                continue
            password = input("Enter password: ").strip()
            valid, msg = validate_password(password)
            if not valid:
                print(msg)
                continue
            register_user(username, password)
        elif choice == '2':
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            if login_user(username, password):
                print("Login successful.")
            else:
                print("Login failed.")
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()