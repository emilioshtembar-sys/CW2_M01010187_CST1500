# Part 0 
#!pip install pandas bcrypt # in your project environment you just use pip install pandas bcrypt without the !
import sqlite3
import pandas as pd
import bcrypt
from pathlib import Path

# Define paths
DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"

# Create DATA folder if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

print(" Imports successful!")
print(f" DATA folder: {DATA_DIR.resolve()}")
print(f" Database will be created at: {DB_PATH.resolve()}")