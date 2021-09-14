import cv2
import numpy
import os


def generate_edge_enhacement_pictures(source_path, destiny_path):
    files = [file for file in os.listdir(source_path) if file.endswith(".jpg") or file.endswith(".jpeg")]
    for file in files:
        original_img = cv2.imread(os.path.join(source_path, file))
        kernel = generate_kernel()
        output = cv2.filter2D(original_img, -1, kernel)
        filename, file_extension = os.path.splitext(file)
        cv2.imwrite(os.path.join(destiny_path, filename + "_enha" + file_extension), output)


def generate_kernel():
    kernel_sharpen = numpy.array([[-1, -1, -1, -1, -1],
                                 [-1, 2, 2, 2, -1],
                                 [-1, 2, 8, 2, -1],
                                 [-1, 2, 2, 2, -1],
                                 [-1, -1, -1, -1, -1]]) / 8.0
    return kernel_sharpen


def test():
    generate_edge_enhacement_pictures(os.path.join(os.getcwd(), "test"), os.path.join(os.getcwd(), "test"))


if __name__ == '__main__':
    test()
