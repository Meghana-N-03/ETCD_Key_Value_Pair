
from flask import Flask, render_template, request, jsonify

import etcd3

app = Flask(__name__)

# def list_all_keys():
#     """Connects to etcd and retrieves all keys, returning decoded strings."""
#     try:
#         etcd = etcd3.client()
#         keys_values = etcd.get_all()
#         keys = [key.decode('utf-8') for key, _ in keys_values]  # Extracting only keys
#         print(keys)  # Added for debugging
#         return keys
#     except Exception as e:
#         print(e)  # Added for debugging
#         return []
def list_all_keys():
    """Connects to etcd and retrieves all keys, returning decoded strings."""
    try:
        etcd = etcd3.client()
        keys = []
        for _, metadata in etcd.get_all():
            keys.append(metadata.key.decode('utf-8'))
        return keys
    except Exception as e:
        print("Error:", e)
        return []





def get_value_for_key(key):
    """Connects to etcd, retrieves value for the provided key, and decodes it."""
    try:
        etcd = etcd3.client()
        value, _ = etcd.get(key.encode('utf-8'))
        if value is None:
            return None
        return value.decode('utf-8')
    except Exception as e:
        return None

def put_key_value_pair(key, value):
    """Connects to etcd and puts the key-value pair, returning a success message."""
    try:
        etcd = etcd3.client()
        etcd.put(key.encode('utf-8'), value.encode('utf-8'))
        return f"Key '{key}' with value '{value}' successfully added to etcd"
    except Exception as e:
        return None

def delete_key(key):
    """Connects to etcd and attempts to delete the provided key."""
    try:
        etcd = etcd3.client()
        deleted = etcd.delete(key.encode('utf-8'))
        if deleted:
            return f"Key '{key}' successfully deleted."
        else:
            return f"Key '{key}' doesn't exist."
    except Exception as e:
        return None

# Route to render the index.html template
@app.route('/')
def index():
    keys = list_all_keys()
    print(keys)  # Added for debugging
    return render_template('index.html', keys=keys)

# Route to get the value for a specific key
@app.route('/get', methods=['POST'])
def get_value():
    key = request.form['key']
    value = get_value_for_key(key)
    if value is not None:
        message = f"Value for '{key}': {value}"
    else:
        message = f"Key '{key}' doesn't exist."
    return jsonify(message=message)

# Route to put a key-value pair into etcd
@app.route('/put', methods=['POST'])
def put_value():
    key = request.form['key']
    value = request.form['value']
    message = put_key_value_pair(key, value)
    return jsonify(message=message)

# Route to delete a key
@app.route('/delete', methods=['POST'])
def delete_key_route():
    key = request.form['key']
    message = delete_key(key)
    return jsonify(message=message)

if __name__ == "__main__":
    app.run(debug=True)














