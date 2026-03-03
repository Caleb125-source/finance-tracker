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
def read_data(filepath=file_path):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # If file has [] (a list), convert to expected dict structure
            if isinstance(data, list):
                return {"user_list": data}

            # If file has dict but missing user_list, add it
            if isinstance(data, dict) and "user_list" not in data:
                data["user_list"] = []

            return data

    except (FileNotFoundError, json.JSONDecodeError, IOError):
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
def get_user(username, filepath=file_path):
    data = read_data(filepath)
    target_key = f"user_{username}"

    for user_entry in data.get("user_list", []):
        if target_key in user_entry:
            return user_entry[target_key]

    return None

def user_exists(username):
    return get_user(username) is not None

# Transaction functions
transaction_file_path = os.path.join(my_path, "../data/transactions.json")

def add_transaction(username, txn_dict, filepath=None):
    if filepath is None:
        filepath = transaction_file_path
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            all_txns = json.load(f)
        if not isinstance(all_txns, list):
            all_txns = []
    except (FileNotFoundError, json.JSONDecodeError):
        all_txns = []

    # Only keep this user's transactions + new one
    all_txns.append({**txn_dict, "username": username})

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(all_txns, f, indent=4)


def get_transactions(username, filepath=None):
    if filepath is None:
        filepath = transaction_file_path
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            all_txns = json.load(f)
        if not isinstance(all_txns, list):
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    return [t for t in all_txns if t.get("username") == username]


def delete_transaction(username, index, filepath=None):
    if filepath is None:
        filepath = transaction_file_path
    user_txns = get_transactions(username, filepath)

    if index < 0 or index >= len(user_txns):
        return False

    # Find and remove the specific transaction from the full list
    target = user_txns[index]

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            all_txns = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    all_txns.remove(target)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(all_txns, f, indent=4)

    return True