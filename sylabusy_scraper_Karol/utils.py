import os


def create_folder(folder_name):
    try:
        # Get the current working directory
        current_directory = os.getcwd()

        # Create a path for the new folder in the current directory
        new_folder_path = os.path.join(current_directory, folder_name)

        # Check if the folder already exists; if not, create it
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            print(f"Folder '{folder_name}' created successfully at: {new_folder_path}")
        else:
            print(f"Folder '{folder_name}' already exists at: {new_folder_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def remove_char(input_string, char_to_remove):
    result = ""
    for char in input_string:
        if char != char_to_remove:
            result += char
    return result
