# Libraries
import curses
import re
import sqlite3
import time
from email_validator import validate_email, EmailNotValidError
from getpass import getpass
import hashlib
import psutil

class UserManager:
    def __init__(self):
        self.failed_attempts = {}
        self.conn = sqlite3.connect('credentials.db')
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def monitor_performance(self, stdscr):
        try:
            # Hide the cursor
            curses.curs_set(0)

            stdscr.addstr(0, 0, "CPU usage: | Memory usage: ")
            stdscr.addstr("\n Press any key to go back...")
            stdscr.refresh()

            # Set the window to non-blocking mode
            stdscr.nodelay(True)

            while True:
                cpu_percent = psutil.cpu_percent()
                mem_stats = psutil.virtual_memory()
                mem_percent = mem_stats.used / mem_stats.total * 100

                stdscr.addstr(0, 11, f"{cpu_percent}% | ")
                stdscr.addstr(0, 28, f"{mem_percent:.2f}%", curses.A_BOLD)

                stdscr.refresh()
                time.sleep(1)

                if stdscr.getch() != curses.ERR:
                    break

            # Set the window back to blocking mode
            stdscr.nodelay(False)

        except Exception as e:
            print(f"An error occurred: {e}")

    def login(self, username, password):
        try:
            # Execute a SELECT statement to retrieve a password for the given username
            self.cur.execute("SELECT password FROM credentials WHERE username=?", (username,))
            result = self.cur.fetchone()
            if result:
                # Check if the user has exceeded the maximum number of failed attempts
                if username in self.failed_attempts and self.failed_attempts[username] >= 3:
                    print("You have exceeded the maximum number of failed attempts. Please try again later.")
                    # Block the user from attempting to login again for 1 minute
                    time.sleep(60)
                    # Reset the failed attempts count
                    self.failed_attempts[username] = 0
                # Hash the password
                enc = password.encode()
                hash1 = hashlib.md5(enc).hexdigest()
                # Compare the hashes
                if hash1 == result[0]:
                    print("Login successful!")
                    # Reset the failed attempts count
                    self.failed_attempts[username] = 0
                    return True
                else:
                    print("Invalid password. Please try again.")
                    # Increment the failed attempts count
                    if username in self.failed_attempts:
                        self.failed_attempts[username] += 1
                    else:
                        self.failed_attempts[username] = 1
                    return False
            else:
                print("Invalid username. Please try again.")
                return False
        except sqlite3.Error as e:
            print(f"An error occurred with the database: {e}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def display_account_info(self, username):
        try:
            self.cur.execute("SELECT * FROM credentials WHERE username=?", (username,))
            result = self.cur.fetchone()
            if result is None:
                print("No account information found.")
            else:
                print(f"ID: {result[0]}")
                print(f"Username: {result[1]}")
                print(f"First Name: {result[3]}")
                print(f"Last Name: {result[4]}")
                print(f"Email: {result[5]}")
                print(f"Phone: {result[6]}")
        except sqlite3.Error as e:
            print(f"An error occurred with the database: {e}")

    def edit_account_info(self, username):
        try:
            print("Please select what you would like to edit:")
            print("1. First Name")
            print("2. Last Name")
            print("3. Email")
            print("4. Phone")
            print("5. Go back")
            edit_selection = input("Please enter your selection: ")
            if edit_selection == "1":
                new_first_name = input("Enter new first name: ")
                # Update the user's first name in the database
                self.cur.execute("UPDATE credentials SET firstname=? WHERE username=?", (new_first_name, username))
                self.conn.commit()
                print("First name updated successfully!")
            elif edit_selection == "2":
                new_last_name = input("Enter new last name: ")
                # Update the user's last name in the database
                self.cur.execute("UPDATE credentials SET lastname=? WHERE username=?", (new_last_name, username))
                self.conn.commit()
                print("Last name updated successfully!")
            elif edit_selection == "3":
                while True:
                    new_email = input("Enter new email: ")
                    try:
                        # Validate the email entered by the user
                        valid = validate_email(new_email)
                        # Update the user's email in the database
                        self.cur.execute("UPDATE credentials SET email=? WHERE username=?", (new_email, username))
                        self.conn.commit()
                        print("Email updated successfully!")
                        break
                    except EmailNotValidError as e:
                        print(f"Invalid email: {e}")
                        go_back = input("Would you like to try again? (y/n): ")
                        if go_back.lower() == "n":
                            break
                        else:
                            continue
            elif edit_selection == "4":
                while True:
                    new_phone = input("Enter new phone number: ")
                    # Check if the phone number is valid
                    if re.match(r'^\d{10}$', new_phone):
                        # Update the user's phone number in the database
                        self.cur.execute("UPDATE credentials SET phone=? WHERE username=?", (new_phone, username))
                        self.conn.commit()
                        print("Phone number updated successfully!")
                        break
                    else:
                        print("Invalid phone number. Please enter a valid phone number.")
            elif edit_selection == "5":
                # Go back
                pass
            else:
                print("Invalid selection. Please try again.")
        except sqlite3.Error as e:
            print(f"An error occurred with the database: {e}")

    def register(self, username, password, conf_password):
        if conf_password == password:
            if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password):
                return "Password must be at least 8 characters long and contain at least one uppercase letter and one digit. Please try again."
            else:
                enc = conf_password.encode()
                hash1 = hashlib.md5(enc).hexdigest()
                self.cur.execute("SELECT * FROM credentials WHERE username=?", (username,))
                result = self.cur.fetchone()
                if result:
                    return "Username already exists. Please try again with a different username."
                else:
                    self.cur.execute("INSERT INTO credentials (username, password) VALUES (?, ?)", (username, hash1))
                    self.conn.commit()
                    return "You have registered successfully!"
        else:
            return "Password is not same as above!"

    def menu(self, username):
        while True:
            print("Please select from the following options:")
            print("1. Display account information")
            print("2. Edit account information")
            print("3. System Performance")
            print("4. Logout")
            selection = input("Please enter your selection: ")
            if selection == "1":
                # Display account information
                self.display_account_info(username)
            elif selection == "2":
                # Edit account information
                self.edit_account_info(username)
            elif selection == "3":
                curses.wrapper(self.monitor_performance)
            elif selection == "4":
                # Logout
                print("Logging out...")
                break
            else:
                print("Invalid selection. Please try again.")

if __name__ == "__main__":
    # Menu loop
    while True:
        # Display the menu
        print ("Welcome to the main menu")
        print ("Please select from the following options:")
        print ("1. Login")
        print ("2. Register")
        print ("3. Exit")
        
        # Get user selection
        selection = input("Please enter your selection: ")
        
        # Respond to selection
        if selection == "1":
            username = input("Username: ")
            password = getpass()
            user_manager = UserManager()
            if user_manager.login(username, password):
                user_manager.menu(username)
        elif selection == "2":
            username = input("Username: ")
            password = getpass()
            conf_password = getpass(prompt="Confirm Password: ")
            user_manager = UserManager()
            print(user_manager.register(username, password, conf_password))
        elif selection == "3":
            print ("Thank you for using the program")
            break
        else:
            print ("Invalid selection, please try again")