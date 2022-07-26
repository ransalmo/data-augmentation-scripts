import background.create_new_with_other_background

import os

images_path = "/Volumes/Randy/data/original_train"

backgrounds_path = "/Volumes/Randy/data/backgrounds"

result_path = "/Volumes/Randy/data/backgroundsV2"

for i in range(5):
    background.create_new_with_other_background.create_new_image_with_background(images_path, result_path, backgrounds_path)
    print("Step {0} done".format(i+1))

print("Done")