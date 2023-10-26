# FinleyJepson_T1A3
[Trello](https://trello.com/b/hAej7lpq/finleyjepsont1a3)

[Repo](https://github.com/finleyjepson/FinleyJepson_T1A3)
## Help Documentation

This program is a simple login and registration system that uses a SQLite database to store user credentials. Upon successful login, the user is presented with a menu of options to view and edit their account information, monitor system performance, or logout.

## Style guide
Source code for this application was styled using PEP 8, [styling guide link here](https://peps.python.org/pep-0008/)

### Software & Hardware Requirements

#### Python minimum hardware requirements:
Modern Operating System: 
Windows 7 or 10
Mac OS X 10.11 or higher, 64-bit
Linux: RHEL 6/7, 64-bit (almost all libraries also work in Ubuntu)
x86 64-bit CPU (Intel / AMD architecture). ARM CPUs are not supported.
4 GB RAM
5 GB free disk space

[Source](https://support.enthought.com/hc/en-us/articles/204273874-Enthought-Python-Minimum-Hardware-Requirements)

#### Software Requirements
- Python 3.10 or higher
- Terminal application that is a standalone application

### Usage

To use this program, simply run the `main.py` file in a standalone Terminal (do not run from a built in termnal interface, such as in VSCode) from the `/src` folder. The program will prompt you to either login or register a new account. Once logged in, you can select from the available options in the menu.

### Dependencies



This program requires the following Python packages to be installed:

- `getpass`
- `hashlib`
- `sqlite3`
- `time`
- `psutil`
- `curses`
- `re`
- `email_validator`

You can install these packages using pip by running the following command:

```
pip install getpass hashlib sqlite3 time psutil curses re email_validator
```

## Installation Documentation

To install this program, follow these steps:

1. Clone the repository or download the `main.py` file.
2. Install the required dependencies using pip (see above).
3. Run the `main.py` file in a Python environment.

That's it! You should now be able to use the program.

## Features

### Feature 1 - Login Function
This Login feature allows users to log in by checking their credentials against the SQLite database. After inputting a username, the function fetches the associated hashed password. The user's inputted password is then hashed and compared to the stored hash. If they match, login is successful. If a password is incorrect, the function tracks the failed attempts for each username. After three failed attempts, the user is temporarily locked out for one minute. If the user enters an invalid username or encounters a database error, appropriate messages are displayed. The user can choose to try again or exit after each failed attempt. The function also handles generic exceptions and ensures the database connection is closed properly.

### Feature 2 - Register Function
The Register feature facilitates user registration. Users provide a username and password, which they must confirm. Passwords need to meet complexity requirements: at least 8 characters, containing an uppercase letter and a digit. If criteria aren't met, users are prompted to try again. Passwords are then hashed using MD5 before storage. The SQLite database is queried to ensure the username isn't already taken. If unique, the username and hashed password are stored in the database. If registration succeeds, users are notified and given an option to return to the main menu. Database errors are handled, and users are informed of any issues.

### Feature 3 - Editing/Adding additional account information
The feature, when activated with the selection "2", facilitates users in editing their account details stored in the 'credentials.db' SQLite database. Upon activation, the program connects to the database and prompts users with a menu to choose which information they wish to modify: first name, last name, email, phone, or an option to go back. Depending on the choice:

- For the first name, users provide a new name which replaces the old one in the database.
- Updating the last name follows a similar process.
- When users opt to modify their email, the program conducts a validation step. If the email is found invalid, users are informed and can decide to reattempt or exit. Upon entering a valid email, it's saved in the database.
- For phone number updates, the system checks if the entered number matches the expected format (10 digits). If not, the user is prompted to input again. A valid phone number is stored in the database.
  
If users select "5" or make an invalid selection, they're redirected to the initial menu or informed of their incorrect choice, respectively.

### Feature 4 - System Performance Monitor
The performance monitor feature leverages the `curses` library to display real-time CPU and memory usage statistics in a terminal window. Upon activation, the cursor is hidden for a cleaner display. The screen then prompts "CPU usage:" and "Memory usage:" labels, along with an instruction indicating users can press any key to exit the monitoring. The window is set to non-blocking mode to enable continuous updating of usage statistics. Every second, the function fetches and displays the current CPU usage percentage and the memory utilization percentage using the `psutil` library. The memory usage value is presented in bold. If a user presses any key during this real-time monitoring, the loop breaks, and the window returns to its regular blocking mode. Any unexpected issues that arise during execution are caught, and an error message is printed.


## Inplementation plan


1. Create a login page with a form that asks for a username and password.
2. When the form is submitted, check if the username exists in a file that stores user information.
3. If the username does not exist, display an error message and prompt the user to try again.
4. If the username exists, check if the password matches the hashed password stored in the file.
5. If the password matches, log the user in and display a welcome message with a list of features they can access.
6. If the password does not match, increment a counter for the number of failed login attempts for that user.
7. If the number of failed login attempts is less than 3, display an error message and prompt the user to try again.
8. If the number of failed login attempts is 3 or more, lock the account for a period of time and display an error message.
9. Create a registration page with a form that asks for a username and password.
10. When the form is submitted, check if the username is unique and if the password meets complexity requirements.
11. If the username is not unique or the password does not meet complexity requirements, display an error message and prompt the user to try again.
12. If the username is unique and the password meets complexity requirements, hash the password and store the username and hashed password in the file.
13. Create a function to encrypt passwords using a Python hashing library.
14. Create a function to log all activity into a file.
15. Create functions to allow users to edit/add additional information to their account, change their password, display all account information except password, and monitor system performance.
16. Create a logout function that logs the user out and redirects them to the login page.
