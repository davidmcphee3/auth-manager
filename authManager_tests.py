import unittest

from authManager import AuthManager

class TestCode(unittest.TestCase):
    def setUp(self):
        self.auth_manager_plain = AuthManager("databases/plainDB.csv", False, False)
        self.auth_manager_hash = AuthManager("databases/hashDB.csv", True, False)
        self.auth_manager_salt = AuthManager("databases/saltDB.csv", True, True)

    def test_file_runs(self):
        self.assertEqual(1, 1)

    def test_A_add_user(self):
        self.assertTrue(self.auth_manager_plain.add_user("mike", "pass"))
        self.assertTrue(self.auth_manager_hash.add_user("mike", "pass"))
        self.assertTrue(self.auth_manager_salt.add_user("mike", "pass"))

    def test_B_add_dup_user(self):
        self.assertFalse(self.auth_manager_plain.add_user("mike", "pass"))
        self.assertFalse(self.auth_manager_hash.add_user("mike", "pass"))
        self.assertFalse(self.auth_manager_salt.add_user("mike", "pass"))

    def test_C_add_second_user(self):
        self.assertTrue(self.auth_manager_plain.add_user("john", "word"))
        self.assertTrue(self.auth_manager_hash.add_user("john", "word"))
        self.assertTrue(self.auth_manager_salt.add_user("john", "word"))

    def test_D_add_third_user_dup_pass(self):
        self.assertTrue(self.auth_manager_plain.add_user("bill", "word"))
        self.assertTrue(self.auth_manager_hash.add_user("bill", "word"))
        self.assertTrue(self.auth_manager_salt.add_user("bill", "word"))

    def test_E_successful_login(self):
        self.assertTrue(self.auth_manager_plain.login("mike", "pass"))
        self.assertTrue(self.auth_manager_hash.login("mike", "pass"))
        self.assertTrue(self.auth_manager_salt.login("mike", "pass"))

    def test_F_bad_password(self):
        self.assertFalse(self.auth_manager_plain.login("mike", "word"))
        self.assertFalse(self.auth_manager_hash.login("mike", "word"))
        self.assertFalse(self.auth_manager_salt.login("mike", "word"))
        

    def test_G_bad_username(self):
        self.assertFalse(self.auth_manager_plain.login("john", "pass"))
        self.assertFalse(self.auth_manager_hash.login("john", "pass"))
        self.assertFalse(self.auth_manager_salt.login("john", "pass"))
  


if __name__ == '__main__':
    auth1 = AuthManager("databases/plainDB.csv", False, False)
    auth2 = AuthManager("databases/hashDB.csv", True, False)
    auth3 = AuthManager("databases/saltDB.csv", True, True)
    auth1.clear_db()
    auth2.clear_db()
    auth3.clear_db()
    unittest.main()