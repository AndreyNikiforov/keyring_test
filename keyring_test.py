import pkgutil
import keyring
import keyrings.alt

print(f"Keyring: {keyring.get_keyring()}")

print(f'Password: {keyring.get_password("foo", "bar")}')