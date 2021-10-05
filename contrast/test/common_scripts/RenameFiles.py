import os
import uuid
import shutil


def rename_files(target_path):
    # set the path to copy the files
    target_path = "/Users/randysalas/Desktop/Backgrounds"

    files = [file for file in os.listdir(target_path) if os.path.isfile(os.path.join(target_path, file)) and (file.endswith(".jpg" or file.endswith(".png")))]
    new_folder = os.path.join(target_path, str(uuid.uuid4()))
    os.mkdir(new_folder)

    for index, file in enumerate(files):
        old_file_name_path = os.path.join(target_path, file)
        new_file_name = str(index)
        new_file_path = os.path.join(new_folder, new_file_name + ".jpg")
        print("Copying file {0} to {1}".format(old_file_name_path, new_file_path))
        shutil.copy(old_file_name_path, new_file_path)

