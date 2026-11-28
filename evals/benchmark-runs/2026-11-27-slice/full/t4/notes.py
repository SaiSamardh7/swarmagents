from auth import AuthError, user_for_token


def add_note(store, token, text):
    user = user_for_token(store, token)
    store.setdefault("notes", {}).setdefault(user, []).append(text)


def list_notes(store, token):
    user = user_for_token(store, token)
    return list(store.get("notes", {}).get(user, []))
