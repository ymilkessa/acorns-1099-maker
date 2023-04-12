import os


def clean_temp_files():
    files_dir = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "files")

    for file in os.listdir(files_dir):
        if file.endswith(".txt"):
            os.remove(os.path.join(files_dir, file))
