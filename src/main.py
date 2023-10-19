from getpass import getpass

users = {
"user1": "password1",
"user2": "password2",
"user3": "password3"
}

def Login_Function():
    while True:
        username = input("Username: ")
        if username in users:
            password = getpass()
            if password == users[username]:
                print("Login successful!")
                Welcome_User(username)
                break
            else:
                print("Invalid password. Please try again.")
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

def Register_Function():
    pass

def main():
    while True:
        print ("Welcome to the main menu")
        print ("Please select from the following options:")
        print ("1. Login")
        print ("2. Register")
        print ("3. Exit")
        selection = input("Please enter your selection: ")
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