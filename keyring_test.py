import keyring

print(f"All backends: {keyring.backend.get_all_keyring()}")

print(f"Keyring: {keyring.get_keyring()}")

print(f'Password: {keyring.get_password("foo", "bar")}')