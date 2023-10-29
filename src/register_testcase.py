import unittest
from unittest.mock import patch
from maintemp import UserManager
import hashlib

class TestUserManager(unittest.TestCase):

    @patch('builtins.input', side_effect=['testuser', 'Test1234!', 'Test1234!'])
    @patch('getpass.getpass', side_effect=['Test1234!', 'Test1234!'])
    def test_successful_registration(self, mock_getpass, mock_input):
        user_manager = UserManager()
        
        # Clear the test user if exists
        user_manager.cur.execute("DELETE FROM credentials WHERE username=?", ('testuser',))
        user_manager.conn.commit()

        result = user_manager.register('testuser', 'Test1234!', 'Test1234!')
        self.assertEqual(result, "You have registered successfully!")

    @patch('builtins.input', side_effect=['existinguser', 'Test1234!', 'Test1234!'])
    @patch('getpass.getpass', side_effect=['Test1234!', 'Test1234!'])
    def test_existing_username_registration(self, mock_getpass, mock_input):
        user_manager = UserManager()
        
        # Create a user to simulate existing user scenario
        enc_pass = 'Test1234!'.encode()
        hash_pass = hashlib.md5(enc_pass).hexdigest()
        user_manager.cur.execute("INSERT OR IGNORE INTO credentials (username, password) VALUES (?, ?)", ('existinguser', hash_pass))
        user_manager.conn.commit()

        result = user_manager.register('existinguser', 'Test1234!', 'Test1234!')
        self.assertEqual(result, "Username already exists. Please try again with a different username.")

# If this module is the main module, run the tests
if __name__ == '__main__':
    unittest.main()
