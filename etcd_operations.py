import etcd3

def list_all_keys():
    """Connects to etcd and retrieves all keys, returning decoded strings."""
    try:
        etcd = etcd3.client()
        keys = etcd.get_all()
        return [key.decode('utf-8') for key, _ in keys]
    except Exception as e:
        print(f"Error listing keys: {e}")
        return []

def get_value_for_key(key):
    """Connects to etcd, retrieves value for the provided key, and decodes it."""
    try:
        etcd = etcd3.client()
        value, _ = etcd.get(key.encode('utf-8'))
        if value is None:
            print(f"Key '{key}' doesn't exist.")
            return None
        return value.decode('utf-8')
    except Exception as e:
        print(f"Error getting value: {e}")
        return None

def put_key_value_pair(key, value):
    """Connects to etcd and puts the key-value pair, returning a success message."""
    try:
        etcd = etcd3.client()
        etcd.put(key.encode('utf-8'), value.encode('utf-8'))
        return f"Key '{key}' with value '{value}' successfully added to etcd"
    except Exception as e:
        print(f"Error putting key-value pair: {e}")
        return None

def delete_key(key):
    """Connects to etcd and attempts to delete the provided key."""
    try:
        etcd = etcd3.client()
        deleted = etcd.delete(key.encode('utf-8'))
        if deleted:
            return f"Key '{key}' successfully deleted."
        else:
            print(f"Key '{key}' doesn't exist.")
    except Exception as e:
        print(f"Error deleting key: {e}")
        return None


# Example usage:
# List all keys
print("All keys:", list_all_keys())

# Get value for a specific key
while True:
    key_to_get = input("Enter the key to get value: ")
    value = get_value_for_key(key_to_get)
    if value is not None:
        print(f"Value for '{key_to_get}': {value}")
        break

# Put a key-value pair into etcd
key_to_put = input("Enter the key to put: ")
value_to_put = input("Enter the value to put: ")
print(put_key_value_pair(key_to_put, value_to_put))

# Delete a key if it exists
while True:
    key_to_delete = input("Enter the key to delete: ")
    result = delete_key(key_to_delete)
    if result:
        print(result)
        break
