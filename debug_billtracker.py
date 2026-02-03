
import sys
import os
import inspect

# Add current dir to path
sys.path.append(os.getcwd())

try:
    from Billtracker_qt import DataManager
    print("DataManager class imported successfully.")
    print("Methods of DataManager:")
    for name, method in inspect.getmembers(DataManager, predicate=inspect.isfunction):
        print(f" - {name}")
    
    dm = DataManager(".")
    if hasattr(dm, 'load_data'):
        print("DataManager instance HAS load_data method.")
    else:
        print("DataManager instance DOES NOT HAVE load_data method.")

except Exception as e:
    print(f"Error importing or inspecting: {e}")
