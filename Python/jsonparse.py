import json
import os

# --- 1. Define the file path ---
# os.path.join makes this compatible across Windows/Linux/Mac
FILE_PATH = os.path.join(os.path.dirname(__file__), 'sample_data.json')

def parse_json_file(file_path):
    """
    Opens, reads, and parses a JSON file into a Python dictionary.
    """
    # --- 2. Open and Load the JSON ---
    try:
        with open(file_path, 'r') as file:
            # The json.load() function reads the file handle and 
            # converts the JSON structure into a Python dictionary.
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON in {file_path}. Check for syntax errors.")
        return None


def extract_vm_names(data):
    """
    Navigates the dictionary structure to extract a list of VM names.
    """
    if data is None:
        return []

    # --- 3. Navigate the Dictionary Structure ---
    # JSON objects become Python Dictionaries.
    # JSON arrays become Python Lists.

    vm_list = data.get("VirtualMachines", [])
    
    # Check if the list is valid before proceeding
    if not isinstance(vm_list, list):
        print("Error: 'VirtualMachines' key is not a list as expected.")
        return []

    # --- 4. Iterate Over the List (the Array) ---
    vm_names = []
    for vm in vm_list:
        # Each item in the list is a dictionary (a VM object)
        name = vm.get("Name", "Unknown VM")
        vm_names.append(name)
        
        # Example of accessing a nested key (Tags dictionary)
        vm_owner = vm.get("Tags", {}).get("Owner", "No Owner Tag")
        print(f"Found VM: {name}, Owner: {vm_owner}")

    return vm_names


# --- Main Execution Block ---
if __name__ == "__main__":
    # 1. Parse the file
    parsed_data = parse_json_file(FILE_PATH)
    
    if parsed_data:
        print("\n--- Successfully Parsed Data ---")
        # Example of accessing a top-level key
        request_id = parsed_data.get("RequestID")
        print(f"Request ID: {request_id}")
        
        # 2. Extract specific values
        names = extract_vm_names(parsed_data)
        
        print("\n--- Final List ---")
        print(f"Total VM Names extracted: {names}")