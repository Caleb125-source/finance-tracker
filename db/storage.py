import json # Using the in-built json package to store data in users.json
import os #Using os to access files in other directories.

my_path = os.path.abspath(os.path.dirname(__file__)) #This accesses the current absolute path of the device
file_path = os.path.join(my_path, "../data/users.json") # The absolute path is combined with the relative path to user.json to actually read the file. Sourced from Stack Overflow

"""# Basic command syntax:
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
'''JSON To Python'''
## Converting JSON data to a python dictionary
test_data = '{"username": "User", "passsword": 12345}'
parsed_python_data = json.loads(test_data) #Loads parses the JSON data into a python dictionary.


file_data = test_data
with open(file_path, 'r') as JSON_file:
    data_from_file = json.load(JSON_file)
print(f'Data read from {file_path} with data: {data_from_file}')

# Note: json.loads() reads from a string  and accepts string arguments, whereas json.load() reads from a file object with a read() method, and takes a file object as an argument.
# """


#Function for appending data:
def append_data(data, filepath = file_path):
    try:
        with open(filepath, 'r') as file_to_read:
            file_contents = json.load(file_to_read)
    except (FileNotFoundError, json.JSONDecodeError, IOError):
        file_contents = []
    
    # Adds data to the the read contents of the file
    file_contents.append(data) 

    with open(filepath, 'w', encoding='utf-8') as file_to_write:
        json.dump(file_contents, file_to_write, indent=4)
        # Without appending, the entire data in the file would be replaced by the data argument.

# Function for reading data 
def read_data(filepath = file_path):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            file_contents = json.load(file)
            return file_contents
    except (json.JSONDecodeError, IOError):
        return {"user_list": []}


# Function to save user to the users.json file.
def save_user(user_dict, filepath=file_path):

    data = read_data(filepath)
    
    username = user_dict.get("username", "unknown")
    
    created_user = {
        f"user_{username}": {
            "password_hash": user_dict.get("password_hash", ""),
            "session": user_dict.get("session", {}),
            "transactions": user_dict.get("transactions", []),
            "income": user_dict.get("income", []),
            "expense": user_dict.get("expense", [])
        }
    }
    
    # Append to the list and write back to the file
    data["user_list"].append(created_user)

    with open(filepath, 'w', encoding='utf-8') as file_to_write:
        json.dump(data, file_to_write, indent=4)

#Function to get user from the users.json file.
def get_user(username, filepath = file_path):
    data = read_data(filepath)
    target_key = f"user_{username}"
    
  
    for user_entry in data.get("user_list", []):
        if target_key in user_entry:
            return user_entry[target_key]
        else:
            return False # Boolean indicating user was not found.

def user_exists(username):
    if get_user(username) == False:
        return False
    else:
        return True

'''Expected data structure:

users = {
    user_list = [
        {username}: {
            password_hash: {password}

            session: {}
            transactions: []
            income: []
            expense: []
        }
    ]
}

Each of the transactions, income and expense lists will (probably) store either dictionaries.
'''