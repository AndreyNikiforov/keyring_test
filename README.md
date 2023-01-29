# keyring_test -- repro for teh error

Packaging the app with keyring by PyInstaller breaks keyring functionality

# Steps to repro

- open repo in vscode in dev container 
- same on Windows 10 host with latest Docker Desktop and Mac Air M1 with latest Docker Desktop
- run `pip3 install -r requirement.txt`
- run `python3 keyring_test.py`. Output:
```
Keyring: keyrings.alt.file.PlaintextKeyring (priority: 0.5)
Password: None
```
- run `pyinstaller -y keyring_test.py`
- run `dist/keyring_test/keyring_test`. Output:
```
Keyring: keyring.backends.fail.Keyring (priority: 0)
Traceback (most recent call last):
  File "keyring_test.py", line 7, in <module>
    print(f'Password: {keyring.get_password("foo", "bar")}')
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "keyring/core.py", line 55, in get_password
  File "keyring/backends/fail.py", line 25, in get_password
keyring.errors.NoKeyringError: No recommended backend was available. Install a recommended 3rd party backend package; or, install the keyrings.alt package if you want to use the non-recommended backends. See https://pypi.org/project/keyring for details.
[2091] Failed to execute script 'keyring_test' due to unhandled exception!
```

all packages (`pip3 list`):
```
Package                   Version
------------------------- -------
altgraph                  0.17.3
cffi                      1.15.1
cryptography              39.0.0
importlib-metadata        6.0.0
jaraco.classes            3.2.3
jeepney                   0.8.0
keyring                   23.13.1
keyrings.alt              4.2.0
more-itertools            9.0.0
pip                       22.3.1
pycparser                 2.21
pyinstaller               5.7.0
pyinstaller-hooks-contrib 2022.15
SecretStorage             3.3.3
setuptools                65.5.0
wheel                     0.38.4
zipp                      3.12.0
```
