import os, tempfile, unittest
from userdb import connect, register, find_users, login

class TestBasic(unittest.TestCase):
    def setUp(self):
        fd, self.db = tempfile.mkstemp(suffix=".db"); os.close(fd); os.unlink(self.db)
        self.conn = connect(self.db)
    def tearDown(self):
        self.conn.close()
        if os.path.exists(self.db): os.unlink(self.db)
    def test_register_and_find(self):
        register(self.conn, "ana", "pw-1")
        register(self.conn, "bob", "pw-2")
        self.assertEqual(find_users(self.conn, "an"), [("ana",)])
        self.assertEqual(find_users(self.conn, "zzz"), [])
    def test_login(self):
        register(self.conn, "ana", "pw-1")
        self.assertTrue(login(self.conn, "ana", "pw-1"))
        self.assertFalse(login(self.conn, "ana", "wrong"))
        self.assertFalse(login(self.conn, "ghost", "pw-1"))

if __name__ == "__main__":
    unittest.main()
