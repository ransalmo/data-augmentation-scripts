import cv2
import numpy
import os


def generate_motion_blur_pictures(source_path, destiny_path, filter_size=30, horizontal=True):
    files = [file for file in os.listdir(source_path) if file.endswith(".jpg") or file.endswith(".jpeg")]
    for file in files:
        original_img = cv2.imread(os.path.join(source_path, file))
        if horizontal:
            kernel = generate_horizontal_kernel(filter_size)
        else:
            kernel = generate_vertical_kernel(filter_size)
        output = cv2.filter2D(original_img, -1, kernel)

        im_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

        filename, file_extension = os.path.splitext(file)
        cv2.imwrite(os.path.join(destiny_path, filename + "_blur" + file_extension), output)


def generate_horizontal_kernel(size):
    kernel = numpy.zeros((size, size))
    kernel[int((size - 1) / 2), :] = numpy.ones(size)
    kernel = kernel / size
    return kernel


def generate_vertical_kernel(size):
    kernel = numpy.zeros((size, size))
    kernel[:, int((size - 1) / 2)] = numpy.ones(size)
    kernel = kernel / size
    return kernel


def test():
    generate_motion_blur_pictures(os.path.join(os.getcwd(), "test"), os.path.join(os.getcwd(), "test"), horizontal=False)


if __name__ == '__main__':
    test()
