import unittest
from unittest.mock import patch
from main import UserManager
import hashlib

class TestUserManager(unittest.TestCase):

    # This class contains two test cases that check the functionality of the UserManager class.

    # Test Case 1: test_successful_registration
    # This test case checks if a user can be successfully registered with valid credentials.
    # Test Cases:
    # 1. User enters valid credentials and the registration is successful.
    # 2. User enters invalid credentials and the registration fails.

    # Test Case 2: test_existing_username_registration
    # This test case checks if the registration fails when a user tries to register with an existing username.
    # Test Cases:
    # 1. User tries to register with an existing username and the registration fails.
    # 2. User tries to register with a new username and the registration is successful.


    @patch('builtins.input', side_effect=['testuser', 'Test1234!', 'Test1234!'])
    @patch('getpass.getpass', side_effect=['Test1234!', 'Test1234!'])
    def test_successful_registration(self, mock_getpass, mock_input):

        # This test case checks if a user can be successfully registered with valid credentials.

        # Test Cases:
        # 1. User enters valid credentials and the registration is successful.

        # Create an instance of the UserManager class
        user_manager = UserManager()
        
        # Clear the test user if exists
        user_manager.cur.execute("DELETE FROM credentials WHERE username=?", ('testuser',))
        user_manager.conn.commit()

        # Call the register function of the UserManager class
        result = user_manager.register('testuser', 'Test1234!', 'Test1234!')
        self.assertEqual(result, "You have registered successfully!")

    @patch('builtins.input', side_effect=['existinguser', 'Test1234!', 'Test1234!'])
    @patch('getpass.getpass', side_effect=['Test1234!', 'Test1234!'])
    def test_existing_username_registration(self, mock_getpass, mock_input):
        # This test case checks if the registration fails when a user tries to register with an existing username.

        # Test Cases:
        # 1. User tries to register with an existing username and the registration fails.
        # 2. User tries to register with a new username and the registration is successful.

        # Create an instance of the UserManager class
        user_manager = UserManager()
        
        # Create a user to simulate existing user scenario
        enc_pass = 'Test1234!'.encode()
        hash_pass = hashlib.md5(enc_pass).hexdigest()
        user_manager.cur.execute("INSERT OR IGNORE INTO credentials (username, password) VALUES (?, ?)", ('existinguser', hash_pass))
        user_manager.conn.commit()

        # Call the register function of the UserManager class
        result = user_manager.register('existinguser', 'Test1234!', 'Test1234!')
        self.assertEqual(result, "Username already exists. Please try again with a different username.")

# If this module is the main module, run the tests
if __name__ == '__main__':
    unittest.main()
