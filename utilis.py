import json
import logging

# Logging configuration
# For functionality flexibility, displaying an informational message with the number of detected errors and execution time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Reading the .json file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
