import unittest
from unittest.mock import patch, Mock
import hashlib
from maintest import UserManager

class TestUserManager(unittest.TestCase):

    def setUp(self):
        # This method is run before each test
        self.user_manager = UserManager()

    def tearDown(self):
        # This method is run after each test
        # Clean up any changes to avoid side effects
        self.user_manager.cur.execute("DELETE FROM credentials WHERE username=?", ('testuser',))
        self.user_manager.conn.commit()

    @patch('builtins.input', side_effect=['testuser'])
    @patch('getpass.getpass', return_value='Test1234!')
    def test_successful_login(self, mock_getpass, mock_input):
        # Insert a user to simulate the existing user in database
        enc_pass = 'Test1234!'.encode()
        hash_pass = hashlib.md5(enc_pass).hexdigest()
        self.user_manager.cur.execute("INSERT OR IGNORE INTO credentials (username, password) VALUES (?, ?)", ('testuser', hash_pass))
        self.user_manager.conn.commit()

        result = self.user_manager.login('testuser', 'Test1234!')
        self.assertTrue(result)

    @patch('builtins.input', side_effect=['invaliduser'])
    @patch('getpass.getpass', return_value='WrongPass')
    def test_invalid_username_login(self, mock_getpass, mock_input):
        result = self.user_manager.login('invaliduser', 'WrongPass')
        self.assertFalse(result)

# If this module is the main module, run the tests
if __name__ == '__main__':
    unittest.main()
