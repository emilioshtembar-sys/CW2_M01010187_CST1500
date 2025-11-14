"# CW2_M01010187_CST1500" 
# Week 7 Secure Authentication System
## Project Description 
This is a secure authentication system  with hashing,which i have designed for week 7.
 The aim is to allow users to register theur accounts and to log in. 
 The project consists of 2 main flies which Main.py and auth.py
## Features
secure passowrd hasing is carreied out thrpugh the import bcrypt FUNCTION.
there was a menu that presents the user  with three option register user, login user,  and exit
Password login included password verification when a password was entered to see if it was valid.
here is an output example of the user login system for registration, login and  and it is working coorectly
1. Register User
2. Login User
3. Exit
Choose an option: 3
Exiting program.
Enter username: Emilio
Enter password: Magic123#
User 'Emilio' registered successfully.

1. Register User
2. Login User
3. Exit
Choose an option: 2
Enter username: Emilio
Enter password: Magic123#
Login successful.

1. Register User
2. Login User
3. Exit
Choose an option: 3
Exiting program.





## Technical implementation  
I hads to install bccrypt, as it was not previoulsy installed in order for the registration system to run, otherwise it would nor run without it. 
I put the menu and main in the main.py file as it made it simpler 