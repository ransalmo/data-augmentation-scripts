import os
import numpy as np
import cv2
import random


def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


def generate_gamma_corrected_images(source_path, destiny_path):
    files = [file for file in os.listdir(source_path) if file.endswith(".jpg") or file.endswith(".jpeg")]
    for file in files:
        random_gamma = random.uniform(1.0, 4.0)
        original_img = cv2.imread(os.path.join(source_path, file))
        output = adjust_gamma(original_img, random_gamma)
        filename, file_extension = os.path.splitext(file)
        cv2.imwrite(os.path.join(destiny_path, filename + "_light" + file_extension), output)


def test():
    generate_gamma_corrected_images(os.path.join(os.getcwd(), "test"), os.path.join(os.getcwd(), "test"))


if __name__ == '__main__':
    test()