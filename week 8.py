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

# Part 1 - Database Setup 
-- Table 1: Users
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'analyst', 'support') DEFAULT 'analyst',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Cybersecurity Incidents
CREATE TABLE Cybersecurity_incidents (
    incident_id INT PRIMARY KEY AUTO_INCREMENT,
    reported_by INT,
    incident_type VARCHAR(100),
    severity_level ENUM('low', 'medium', 'high', 'critical'),
    description TEXT,
    date_reported DATE,
    status ENUM('open', 'investigating', 'resolved') DEFAULT 'open',
    FOREIGN KEY (reported_by) REFERENCES users(user_id)
);

-- Table 3: Datasets Metadata
CREATE TABLE datasets_metadata (
    dataset_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    source VARCHAR(100),
    date_added DATE,
    owner_id INT,
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

-- Table 4: IT Support Tickets
CREATE TABLE it_tickets (
    ticket_id INT PRIMARY KEY AUTO_INCREMENT,
    submitted_by INT,
    issue_summary VARCHAR(255),
    issue_details TEXT,
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    status ENUM('open', 'in_progress', 'closed') DEFAULT 'open',
    date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (submitted_by) REFERENCES users(user_id)
);
