import os, tempfile, unittest
from userdb import connect, register, find_users, login

class TestSecurity(unittest.TestCase):
    def setUp(self):
        fd, self.db = tempfile.mkstemp(suffix=".db"); os.close(fd); os.unlink(self.db)
        self.conn = connect(self.db)
        register(self.conn, "ana", "pw-secret-1")
    def tearDown(self):
        self.conn.close()
        if os.path.exists(self.db): os.unlink(self.db)
    def test_password_not_stored_in_plaintext(self):
        stored = self.conn.execute("SELECT password FROM users WHERE name='ana'").fetchone()[0]
        self.assertNotIn("pw-secret-1", stored)
        self.assertNotEqual(stored, "pw-secret-1")
    def test_login_still_works_with_hashing(self):
        self.assertTrue(login(self.conn, "ana", "pw-secret-1"))
        self.assertFalse(login(self.conn, "ana", "nope"))
    def test_find_users_injection_returns_nothing(self):
        self.assertEqual(find_users(self.conn, "%' OR '1'='1"), [])
    def test_find_users_statement_injection_harmless(self):
        result = find_users(self.conn, "x'; DROP TABLE users; --")
        self.assertEqual(result, [])
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM users").fetchone()[0], 1)
    def test_register_with_quote_in_name(self):
        register(self.conn, "o'hara", "pw-2")
        self.assertEqual(find_users(self.conn, "hara"), [("o'hara",)])

if __name__ == "__main__":
    unittest.main()
