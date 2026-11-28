from auth import user_for_token


def add_note(store, token, text):
    user = user_for_token(store, token)
    store["notes"].setdefault(user, []).append(text)


def list_notes(store, token):
    user = user_for_token(store, token)
    return list(store["notes"].get(user, []))
