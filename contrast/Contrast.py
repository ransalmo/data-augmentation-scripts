import cv2
import os


def generate_contrtast_pictures(source_path, destiny_path):
    files = [file for file in os.listdir(source_path) if file.endswith(".jpg") or file.endswith(".jpeg")]
    for file in files:
        original_img = cv2.imread(os.path.join(source_path, file))
        img_yuv = cv2.cvtColor(original_img, cv2.COLOR_BGR2YUV)
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
        filename, file_extension = os.path.splitext(file)
        cv2.imwrite(os.path.join(destiny_path, filename + "_contrast" + file_extension), output)


def test():
    generate_contrtast_pictures(os.path.join(os.getcwd(), "test"), os.path.join(os.getcwd(), "test"))


if __name__ == '__main__':
    test()
