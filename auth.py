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
    #