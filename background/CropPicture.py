import cv2

def crop_picture(source_path, destiny_path, new_height, new_width):
    image = cv2.imread(source_path)
    h, w, _ = image.shape
    if new_height >= h and new_width >= w:
        raise ValueError("Does not make sense resize to the same size")
    else:
        crop_img = image[new_height, new_width]
        cv2.imwrite(destiny_path, crop_img)