import json # Using the in-built json package to store data in users.json
import os #Using os to access files in other directories.

import time # Delete


my_path = os.path.abspath(os.path.dirname(__file__)) #This accesses the current absolute path of the device
file_path = os.path.join(my_path, "../data/users.json") # The absolute path is combined with the relative path to user.json to actually read the file. Sourced from Stack Overflow

# Basic command syntax:
'''Python to JSON'''
python_data = {
    "username": 'User1',
    "password": 'password'
}

converted_json_data = json.dumps(python_data)

data_to_write = python_data
with open(file_path, 'w') as file_to_write:
    json.dump(data_to_write, file_to_write)
    print(f'Data: {data_to_write} written to file in path: {file_path}')

# Note: json.dumps() writes to a string  and accepts dictionary arguments, whereas json.dump() writes to a file object with a write() method, and takes a python dictionary and a file object as arguments.
time.sleep(2)
'''JSON To Python'''
## Converting JSON data to a python dictionary
test_data = '{"username": "User", "passsword": 12345}'
parsed_python_data = json.loads(test_data) #Loads parses the JSON data into a python dictionary.


file_data = test_data
with open(file_path, 'r') as JSON_file:
    data_from_file = json.load(JSON_file)
print(f'Data read from {file_path} with data: {data_from_file}')

# Note: json.loads() reads from a string  and accepts string arguments, whereas json.load() reads from a file object with a read() method, and takes a file object as an argument.

def user_exists():
    pass

def save_user():
    pass

def get_user():
    pass

'''Expected data structure:

users = {
    user_{username}: {
        password_hash: {password}

        session: {}
        transactions: []
        income: []
        expense: []
    }
}

Each of the transactions, income and expense lists will (probably) store either dictionaries.
'''