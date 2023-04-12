import os
from rm_temp_files import clean_temp_files

clean_temp_files()

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results_dir = os.path.join(parent_dir, "results")

# clean the results folder if it exists
if os.path.exists(results_dir):
    for folder in os.listdir(results_dir):
        for file in os.listdir(os.path.join(results_dir, folder)):
            os.remove(os.path.join(results_dir, folder, file))
        os.rmdir(os.path.join(results_dir, folder))
