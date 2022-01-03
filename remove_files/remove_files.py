import os
import shutil
import csv
from pathlib import Path


def remove_files_from(indexes, path):
    files = sorted([file for file in os.listdir(path) if file.endswith(".JPG") or file.endswith(".jpg")])
    for pos in range(0,len(files)):
        if str(pos+1) in indexes:
            print("The file {0} has to be deleted, index {1}".format(files[pos], pos+1))
            image_path = os.path.join(path, files[pos])
            xml_path = os.path.join(path, "annotations", files[pos].replace(".jpg",".xml").replace(".JPG",".xml"))
            print(image_path)
            print(xml_path)
            os.remove(image_path)
            os.remove(xml_path)



def read_csv(path):
    to_return = []
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            to_return.append(row[0])
    return to_return


if __name__ == "__main__":
    indexes = read_csv("/Users/randysalas/Desktop/data/to_exclude.csv")
    remove_files_from(indexes, "/Users/randysalas/Desktop/data/train_back")
