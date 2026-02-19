import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Robust fallback: use script directory
        base_path = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.path.abspath(".")

    return os.path.join(base_path, relative_path)

readme_path = resource_path('README.md')
print(f"Calculated path: {readme_path}")
print(f"Exists: {os.path.exists(readme_path)}")

if os.path.exists(readme_path):
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            print(f"Content length: {len(f.read())}")
    except Exception as e:
        print(f"Error reading file: {e}")
