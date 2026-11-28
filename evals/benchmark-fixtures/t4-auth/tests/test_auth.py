import json, unittest
from store import new_store
from auth import register, login, AuthError
from notes import add_note, list_notes

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.store = new_store()
    def test_register_hashes_password(self):
        register(self.store, "ana", "s3cret-pw")
        self.assertNotIn("s3cret-pw", json.dumps(self.store))
        rec = self.store["users"]["ana"]
        self.assertTrue(rec.get("salt"))
        self.assertTrue(rec.get("hash"))
        self.assertNotEqual(rec["hash"], rec["salt"])
    def test_register_duplicate_raises(self):
        register(self.store, "ana", "pw1")
        with self.assertRaises(AuthError):
            register(self.store, "ana", "pw2")
    def test_same_password_different_hashes(self):
        register(self.store, "ana", "pw1")
        register(self.store, "bob", "pw1")
        self.assertNotEqual(self.store["users"]["ana"]["hash"], self.store["users"]["bob"]["hash"])
    def test_login_right_password_returns_token(self):
        register(self.store, "ana", "pw1")
        token = login(self.store, "ana", "pw1")
        self.assertIsInstance(token, str)
        self.assertGreaterEqual(len(token), 16)
    def test_login_wrong_password_raises(self):
        register(self.store, "ana", "pw1")
        with self.assertRaises(AuthError):
            login(self.store, "ana", "nope")
    def test_login_unknown_user_raises(self):
        with self.assertRaises(AuthError):
            login(self.store, "ghost", "pw")
    def test_notes_require_valid_token(self):
        register(self.store, "ana", "pw1")
        token = login(self.store, "ana", "pw1")
        add_note(self.store, token, "hello")
        self.assertEqual(list_notes(self.store, token), ["hello"])
        with self.assertRaises(AuthError):
            add_note(self.store, "bad-token", "x")
        with self.assertRaises(AuthError):
            list_notes(self.store, "bad-token")
    def test_notes_are_per_user(self):
        register(self.store, "ana", "pw1")
        register(self.store, "bob", "pw2")
        ta = login(self.store, "ana", "pw1")
        tb = login(self.store, "bob", "pw2")
        add_note(self.store, ta, "a-note")
        self.assertEqual(list_notes(self.store, tb), [])

if __name__ == "__main__":
    unittest.main()
