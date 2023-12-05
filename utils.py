import os

def create_folder(folder_name, path=None):
    try:
        if path is None:
            path = os.getcwd()  # Domyślna ścieżka to aktualny katalog roboczy

        new_folder_path = os.path.join(path, folder_name)

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
