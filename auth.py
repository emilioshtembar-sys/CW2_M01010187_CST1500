import bcrypt 
import os

def hash_password(plain_text_password): 
    # TODO: Encode the password to bytes (bcrypt requires byte srtings)
    # TODO: Generate a salt using bycript.gensalt()
    # TODO: Hash the password using.bycrypt
    # TODO: Decode the hash back to a string to be stored in a text file
    return

def verify_password():
    
    # TODO: Encode both the plaintext password and the stored hash to byt
    
    
    # TODO: Use bcrypt.checkpw() to verify the password
    # This function extracts the salt from the hash and compares
    
    return 

#Temporary test code - remove after testing
test_password = "MDX087"

# Test hashing 
hashed = hash_password(test_password)
print(f"Hashed password: {hashed}")
print(f"Hash lenghth: {len(hashed)} characters")

# Test verification with correct password
is_valid = verify_password("Wrong Password", hashed)

USER_DATA_FILE = "users.txt"
def register_user(username, password): 
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            for line in f:
                stored_username, _ = line.strip().split(":")
                if stored_username == username:
                    print("Username already exists.")
                    return False
    hashed_password = hash_password(password)
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username}:{hashed_password}\n")
    print("User registered successfully.")
    return True