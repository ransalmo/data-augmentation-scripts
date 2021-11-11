import shutil
import os

source = "/Users/randysalas/Desktop/images/backgrounds_clean"

destiny = "/Users/randysalas/Desktop/images/renamed"

files = os.listdir(source)

for index, file in enumerate(files):
    shutil.copyfile(os.path.join(source, file), os.path.join(destiny, str(index)+".jpg"))