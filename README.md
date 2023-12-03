# keyring_test -- journey for fixing the `keyring` error

Packaging the app with keyring by PyInstaller breaks `keyring` functionality

# Steps to repro

- open repo in vscode in dev container 
- same on Windows 10 host with latest Docker Desktop and Mac Air M1 with latest Docker Desktop
- run `pip3 install -r requirements.txt && python3 keyring_test.py`. Output (as expected):
```
All backends: [<keyring.backends.fail.Keyring object at 0x7f8d1bf35310>, <keyring.backends.chainer.ChainerBackend object at 0x7f8d1bda78d0>, <PlaintextKeyring with no encyption v.1.0 at /home/vscode/.local/share/python_keyring/keyring_pass.cfg>]
Keyring: keyrings.alt.file.PlaintextKeyring (priority: 0.5)
Password: None
```
- run `pyinstaller -y keyring_test.py && dist/keyring_test/keyring_test`. Output (actual with error):
```
All backends: [<keyring.backends.chainer.ChainerBackend object at 0x7f1d17f4bf50>, <keyring.backends.fail.Keyring object at 0x7f1d17b43f50>]
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

all packages installed (`pip3 list`):
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
Docker Desktop v4.15.0

# Trials

## `--hidden-import` params

- use `--hidden-import keyrings.alt.file` for `pyinstaller` gives:
```
All backends: [<keyring.backends.chainer.ChainerBackend object at 0x7f7cc582f510>, <keyring.backends.fail.Keyring object at 0x7f7cc58f3e90>]
Keyring: keyring.backends.fail.Keyring (priority: 0)
Traceback (most recent call last):
  File "keyring_test.py", line 7, in <module>
    print(f'Password: {keyring.get_password("foo", "bar")}')
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "keyring/core.py", line 55, in get_password
  File "keyring/backends/fail.py", line 25, in get_password
keyring.errors.NoKeyringError: No recommended backend was available. Install a recommended 3rd party backend package; or, install the keyrings.alt package if you want to use the non-recommended backends. See https://pypi.org/project/keyring for details.
[3666] Failed to execute script 'keyring_test' due to unhandled exception!
```

## `--collect-all keyrings.alt` params

- use `--collect-all keyrings.alt` for `pyinstaller` gives:
```
Error initializing plugin EntryPoint(name='Gnome', value='keyrings.alt.Gnome', group='keyring.backends').
Traceback (most recent call last):
  File "keyring/backend.py", line 202, in _load_plugins
  File "importlib_metadata/__init__.py", line 208, in load
  File "importlib/__init__.py", line 126, in import_module
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "PyInstaller/loader/pyimod02_importers.py", line 499, in exec_module
  File "keyrings/__init__.py", line 1, in <module>
ModuleNotFoundError: No module named 'pkgutil'
Error initializing plugin EntryPoint(name='Google', value='keyrings.alt.Google', group='keyring.backends').
Traceback (most recent call last):
  File "keyring/backend.py", line 202, in _load_plugins
  File "importlib_metadata/__init__.py", line 208, in load
  File "importlib/__init__.py", line 126, in import_module
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "PyInstaller/loader/pyimod02_importers.py", line 499, in exec_module
  File "keyrings/__init__.py", line 1, in <module>
ModuleNotFoundError: No module named 'pkgutil'
Error initializing plugin EntryPoint(name='Windows (alt)', value='keyrings.alt.Windows', group='keyring.backends').
Traceback (most recent call last):
  File "keyring/backend.py", line 202, in _load_plugins
  File "importlib_metadata/__init__.py", line 208, in load
  File "importlib/__init__.py", line 126, in import_module
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "PyInstaller/loader/pyimod02_importers.py", line 499, in exec_module
  File "keyrings/__init__.py", line 1, in <module>
ModuleNotFoundError: No module named 'pkgutil'
Error initializing plugin EntryPoint(name='file', value='keyrings.alt.file', group='keyring.backends').
Traceback (most recent call last):
  File "keyring/backend.py", line 202, in _load_plugins
  File "importlib_metadata/__init__.py", line 208, in load
  File "importlib/__init__.py", line 126, in import_module
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "PyInstaller/loader/pyimod02_importers.py", line 499, in exec_module
  File "keyrings/__init__.py", line 1, in <module>
ModuleNotFoundError: No module named 'pkgutil'
Error initializing plugin EntryPoint(name='keyczar', value='keyrings.alt.keyczar', group='keyring.backends').
Traceback (most recent call last):
  File "keyring/backend.py", line 202, in _load_plugins
  File "importlib_metadata/__init__.py", line 208, in load
  File "importlib/__init__.py", line 126, in import_module
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "PyInstaller/loader/pyimod02_importers.py", line 499, in exec_module
  File "keyrings/__init__.py", line 1, in <module>
ModuleNotFoundError: No module named 'pkgutil'
Error initializing plugin EntryPoint(name='multi', value='keyrings.alt.multi', group='keyring.backends').
Traceback (most recent call last):
  File "keyring/backend.py", line 202, in _load_plugins
  File "importlib_metadata/__init__.py", line 208, in load
  File "importlib/__init__.py", line 126, in import_module
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "PyInstaller/loader/pyimod02_importers.py", line 499, in exec_module
  File "keyrings/__init__.py", line 1, in <module>
ModuleNotFoundError: No module named 'pkgutil'
Error initializing plugin EntryPoint(name='pyfs', value='keyrings.alt.pyfs', group='keyring.backends').
Traceback (most recent call last):
  File "keyring/backend.py", line 202, in _load_plugins
  File "importlib_metadata/__init__.py", line 208, in load
  File "importlib/__init__.py", line 126, in import_module
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "PyInstaller/loader/pyimod02_importers.py", line 499, in exec_module
  File "keyrings/__init__.py", line 1, in <module>
ModuleNotFoundError: No module named 'pkgutil'
All backends: [<keyring.backends.chainer.ChainerBackend object at 0x7f20ae0583d0>, <keyring.backends.fail.Keyring object at 0x7f20ae058bd0>]
Keyring: keyring.backends.fail.Keyring (priority: 0)
Traceback (most recent call last):
  File "keyring_test.py", line 7, in <module>
    print(f'Password: {keyring.get_password("foo", "bar")}')
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "keyring/core.py", line 55, in get_password
  File "keyring/backends/fail.py", line 25, in get_password
keyring.errors.NoKeyringError: No recommended backend was available. Install a recommended 3rd party backend package; or, install the keyrings.alt package if you want to use the non-recommended backends. See https://pypi.org/project/keyring for details.
[13680] Failed to execute script 'keyring_test' due to unhandled exception!
```
pyinstaller mentions warnings:
```
2189 WARNING: Unable to find package for requirement jaraco.classes from package keyrings.alt.
```

## `--collect-all keyrings.alt.file` params

- use `--collect-all keyrings.alt.file` for `pyinstaller` gives:
```
All backends: [<keyring.backends.chainer.ChainerBackend object at 0x7f9401c580d0>, <keyring.backends.fail.Keyring object at 0x7f9401c58490>]
Keyring: keyring.backends.fail.Keyring (priority: 0)
Traceback (most recent call last):
  File "keyring_test.py", line 7, in <module>
    print(f'Password: {keyring.get_password("foo", "bar")}')
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "keyring/core.py", line 55, in get_password
  File "keyring/backends/fail.py", line 25, in get_password
keyring.errors.NoKeyringError: No recommended backend was available. Install a recommended 3rd party backend package; or, install the keyrings.alt package if you want to use the non-recommended backends. See https://pypi.org/project/keyring for details.
[3666] Failed to execute script 'keyring_test' due to unhandled exception!
```
pyinstaller mentions warnings:
```
198 WARNING: Unable to copy metadata for keyrings.alt.file: The 'keyrings.alt.file' distribution was not found and is required by the application
241 WARNING: collect_data_files - skipping data collection for module 'keyrings.alt.file' as it is not a package.
292 WARNING: collect_dynamic_libs - skipping library collection for module 'keyrings.alt.file' as it is not a package.
441 INFO: Determining a mapping of distributions to packages...
1648 WARNING: Unable to determine requirements for keyrings.alt.file: The 'keyrings.alt.file' distribution was not found and is required by the application
```

## Env var

- use `PYTHON_KEYRING_BACKEND=keyrings.alt.file.PlaintextKeyring dist/keyring_test/keyring_test` gives:
```
All backends: [<keyring.backends.chainer.ChainerBackend object at 0x7fe5c134bcd0>, <keyring.backends.fail.Keyring object at 0x7fe5c1374c10>]
Traceback (most recent call last):
  File "keyring_test.py", line 5, in <module>
    print(f"Keyring: {keyring.get_keyring()}")
                      ^^^^^^^^^^^^^^^^^^^^^
  File "keyring/core.py", line 32, in get_keyring
  File "keyring/core.py", line 83, in init_backend
  File "keyring/core.py", line 97, in _detect_backend
  File "keyring/core.py", line 143, in load_env
  File "keyring/core.py", line 134, in load_keyring
  File "keyring/core.py", line 124, in _load_keyring_class
ModuleNotFoundError: No module named 'keyrings'
[2762] Failed to execute script 'keyring_test' due to unhandled exception!
```
## `import keyrings.alt` in source

- use `import keyrings.alt` to the source throws
```
Traceback (most recent call last):
  File "keyring_test.py", line 2, in <module>
    import keyrings.alt
  File "PyInstaller/loader/pyimod02_importers.py", line 499, in exec_module
  File "keyrings/__init__.py", line 1, in <module>
ModuleNotFoundError: No module named 'pkgutil'
[11865] Failed to execute script 'keyring_test' due to unhandled exception!
```
## `import keyrings.alt` and `import pkgutil` in source

- use `import keyrings.alt` and `import pkgutil` to the source throws
```
All backends: [<keyring.backends.chainer.ChainerBackend object at 0x7fbbe7a5a710>, <keyring.backends.fail.Keyring object at 0x7fbbe7634f90>]
Keyring: keyring.backends.fail.Keyring (priority: 0)
Traceback (most recent call last):
  File "keyring_test.py", line 9, in <module>
    print(f'Password: {keyring.get_password("foo", "bar")}')
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "keyring/core.py", line 55, in get_password
  File "keyring/backends/fail.py", line 25, in get_password
keyring.errors.NoKeyringError: No recommended backend was available. Install a recommended 3rd party backend package; or, install the keyrings.alt package if you want to use the non-recommended backends. See https://pypi.org/project/keyring for details.
[12660] Failed to execute script 'keyring_test' due to unhandled exception!
```

# Workaround/Solution

## with source code change

- use `import keyrings.alt.file` and `import pkgutil` to the source produces expected result

## with params to `pyinstaller`

- use `--collect-all keyrings.alt --hidden-import pkgutil` params for pyinstaller produces output (as expected):
```
All backends: [<keyring.backends.fail.Keyring object at 0x7f88614b1c50>, <PlaintextKeyring with no encyption v.1.0 at /home/vscode/.local/share/python_keyring/keyring_pass.cfg>, <keyring.backends.chainer.ChainerBackend object at 0x7f88614e4cd0>]
Keyring: keyrings.alt.file.PlaintextKeyring (priority: 0.5)
Password: None
```
pyinstaller gives warning during compile:
```
2015 WARNING: Unable to find package for requirement jaraco.classes from package keyrings.alt.
```
adding `--onefile` to `pyinstaller` cmd gives the same correct result