from getpass import getpass
import hashlib
import sqlite3
import time

def Login_Function():
    failed_attempts = {}
    while True:
        username = input("Username: ")
        conn = sqlite3.connect('credentials.db')
        cur = conn.cursor()
        # Execute a SELECT statement to retrieve a password for the given username
        cur.execute("SELECT password FROM credentials WHERE username=?", (username,))
        result = cur.fetchone()
        if result:
            # Check if the user has exceeded the maximum number of failed attempts
            if username in failed_attempts and failed_attempts[username] >= 3:
                print("You have exceeded the maximum number of failed attempts. Please try again later.")
                # Block the user from attempting to login again for 1 minute
                time.sleep(60)
                # Reset the failed attempts count
                failed_attempts[username] = 0
            # Get the password
            password = getpass()
            # Hash the password
            enc = password.encode()
            hash1 = hashlib.md5(enc).hexdigest()
            # Compare the hashes
            if hash1 == result[0]:
                print("Login successful!")
                # Reset the failed attempts count
                failed_attempts[username] = 0
                conn.close()
                Welcome_User(username)
                break
            else:
                print("Invalid password. Please try again.")
                # Increment the failed attempts count
                if username in failed_attempts:
                    failed_attempts[username] += 1
                else:
                    failed_attempts[username] = 1
                try_again = input("Would you like to try again? (y/n): ")
                if try_again.lower() == "n":
                    break
        else:
            print("Invalid username. Please try again.")
            try_again = input("Would you like to try again? (y/n): ")
            if try_again.lower() == "n":
                break

def Welcome_User(username):
    print(f"Welcome {username}!")
    while True:
        print("Please select from the following options:")
        print("1. Display account information")
        print("2. Edit account information")
        print("3. Add account information")
        print("4. Logout")
        selection = input("Please enter your selection: ")
        if selection == "1":
            # Display account information
            conn = sqlite3.connect('credentials.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM credentials WHERE username=?", (username,))
            result = cur.fetchone()
            print(f"ID: {result[0]}")
            print(f"Username: {result[1]}")
            print(f"First Name: {result[3]}")
            print(f"Last Name: {result[4]}")
            print(f"Email: {result[5]}")
            print(f"Phone: {result[6]}")
            conn.close()
        elif selection == "2":
            # Edit account information
            conn = sqlite3.connect('credentials.db')
            cur = conn.cursor()
            print("Please select what you would like to edit:")
            print("1. First Name")
            print("2. Last Name")
            print("3. Email")
            print("4. Phone")
            edit_selection = input("Please enter your selection: ")
            if edit_selection == "1":
                new_first_name = input("Enter new first name: ")
                # Update the user's first name in the database
                cur.execute("UPDATE credentials SET firstname=? WHERE username=?", (new_first_name, username))
                conn.commit()
                print("First name updated successfully!")
            elif edit_selection == "2":
                new_last_name = input("Enter new last name: ")
                # Update the user's last name in the database
                cur.execute("UPDATE credentials SET lastname=? WHERE username=?", (new_last_name, username))
                conn.commit()
                print("Last name updated successfully!")
            elif edit_selection == "3":
                new_email = input("Enter new email: ")
                # Update the user's email in the database
                cur.execute("UPDATE credentials SET email=? WHERE username=?", (new_email, username))
                conn.commit()
                print("Email updated successfully!")
            elif edit_selection == "4":
                new_phone = input("Enter new phone number: ")
                # Update the user's phone number in the database
                cur.execute("UPDATE credentials SET phone=? WHERE username=?", (new_phone, username))
                conn.commit()
                print("Phone number updated successfully!")
            else:
                print("Invalid selection. Please try again.")
            conn.close()
        elif selection == "3":
            # Add account information
            conn = sqlite3.connect('credentials.db')
            cur = conn.cursor()
            new_first_name = input("Enter first name: ")
            new_last_name = input("Enter last name: ")
            new_email = input("Enter email: ")
            new_phone = input("Enter phone number: ")
            # Update the user's information in the database
            cur.execute("UPDATE credentials SET firstname=?, lastname=?, email=?, phone=? WHERE username=?", (new_first_name, new_last_name, new_email, new_phone, username))
            conn.commit()
            conn.close()
            print("Account information added successfully!")
        elif selection == "4":
            # Logout
            print("Logging out...")
            break
        else:
            print("Invalid selection. Please try again.")

def Register_Function():
    while True:
        # Get the username and password from the user
        username = input("Enter username: ")
        password = getpass()
        conf_password = getpass(prompt="Confirm password: ")

        # Confirm that the passwords match
        if conf_password == password:
            # Check if the password meets the complexity requirements
            if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password):
                print("Password must be at least 8 characters long and contain at least one uppercase letter and one digit. Please try again.")
                try_again = input("Would you like to try again? (y/n): ")
                if try_again.lower() == "n":
                    break
            else:
                # Hash the password
                enc = conf_password.encode()
                hash1 = hashlib.md5(enc).hexdigest()

                # Check if the username already exists in the database
                conn = sqlite3.connect('credentials.db')
                cur = conn.cursor()
                cur.execute("SELECT * FROM credentials WHERE username=?", (username,))
                result = cur.fetchone()
                if result:
                    print("Username already exists. Please try again with a different username.")
                    try_again = input("Would you like to try again? (y/n): ")
                    if try_again.lower() == "n":
                        break
                else:
                    # Store the username and password in the database
                    cur.execute("INSERT INTO credentials (username, password) VALUES (?, ?)", (username, hash1))
                    conn.commit()
                    conn.close()

                    # Let the user know that they're registered
                    print("You have registered successfully!")
                    back_to_main = input("Would you like to go back to the main menu? (y/n): ")
                    if back_to_main.lower() == "y":
                        break
        else:
            print("Password is not same as above! \n")
            try_again = input("Would you like to try again? (y/n): ")
            if try_again.lower() == "n":
                break

def main():
    # Menu loop
    while True:
        print ("Welcome to the main menu")
        print ("Please select from the following options:")
        print ("1. Login")
        print ("2. Register")
        print ("3. Exit")
        
        # Get user selection
        selection = input("Please enter your selection: ")
        
        # Respond to selection
        if selection == "1":
            Login_Function()
        elif selection == "2":
            Register_Function()
        elif selection == "3":
            print ("Thank you for using the program")
            break
        else:
            print ("Invalid selection, please try again")

main()