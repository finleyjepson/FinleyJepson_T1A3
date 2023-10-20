# FinleyJepson_T1A3
 
## Features

### Feature 1
Login -

### Feature 2
Registry - 

### Feature 3
Editing & Inputting additional account information - 

### Feature 4
Activity logging - 

## Inplementation plan

[Trello](https://trello.com/b/hAej7lpq/finleyjepsont1a3)

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
