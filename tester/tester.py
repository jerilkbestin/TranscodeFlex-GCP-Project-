# want to create a code that will have the following functionalities:
# 1. have a array of video file names
# 2. randomly select a number between 1 and 6
# 3. randomly select the above number of video file names from the array
# 4. randomly select a time between 10 to 300 seconds
# 5. call process_upload() function for each of the selected video file names

import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import time
import uuid


# Google Cloud credentials setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/jeril/disproj/spheric-rhythm-414505-7469436e6688.json"

# Define the source and destination directories
source_dir = './input'
dest_dir = './output'

# List all files in the source directory
all_files = os.listdir(source_dir)



def copy_file(file):
    session_id = str(uuid.uuid4())  # Generate a new session ID
    d_file_name = session_id + '-SID-' + file
    shutil.copy(os.path.join(source_dir, file), os.path.join(dest_dir, d_file_name))
    return file



def copy_files_with_delay(files):
    """Function to copy a batch of files with a random delay before starting the next batch."""
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit files for copying and track progress
        future_to_file = {executor.submit(copy_file, file_name): file_name for file_name in files}
        for future in as_completed(future_to_file):
            file_name = future_to_file[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error copying file {file_name}: {e}")
            else:
                print(f"File {file_name} copied successfully.")


def random_video_files():
    while True:
        num_files = random.randint(1, 6)
        selected_files = random.sample(all_files, num_files)
        print(f"Selected files: {selected_files}")
        copy_files_with_delay(selected_files)
        time_to_sleep = random.randint(10, 600)
        print(f"Sleeping for {time_to_sleep} seconds.")
        time.sleep(time_to_sleep)

random_video_files()