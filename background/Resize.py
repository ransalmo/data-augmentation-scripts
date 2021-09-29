import cv2

def Resize(source_path, destiny_path, height, width):
    img_orig = cv2.imread(source_path)
    points = (width, height)
    resize = cv2.resize(img_orig, points, interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(destiny_path, img_orig)
