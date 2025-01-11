from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt6', 'speech_recognition', 'pyttsx3'],
    'plist': {
        'CFBundleName': 'المساعد الشخصي',
        'CFBundleDisplayName': 'المساعد الشخصي',
        'CFBundleVersion': '0.1',
        'CFBundleShortVersionString': '0.1',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)