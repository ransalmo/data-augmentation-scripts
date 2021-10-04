import cv2
import numpy as np
import os
import uuid


def grabcut(img_orig, rect_final, destiny_filepath, crop_image = False):
    mask = np.zeros(img_orig.shape[:2],np.uint8)
    x,y,w,h = rect_final
    mask[y:y+h, x:x+w] = 1

    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    cv2.grabCut(img_orig,mask,rect_final,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img_orig = img_orig*mask2[:,:,np.newaxis]

    tmp = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
    b, g, r = cv2.split(img_orig)
    rgba = [b, g, r, alpha]
    img_orig = cv2.merge(rgba, 4)

    if crop_image:
        img_orig = img_orig[y:y+h, x:x+w]

    cv2.imwrite(destiny_filepath, img_orig)
    return os.path.split(destiny_filepath)[1]

def batch_segmentation(source_folder, destiny_folder):
    if not os.path.exists(source_folder) or not os.path.exists(destiny_folder):
        raise ValueError("The destiny or the source folder are invalid")
    else:
        files = os.listdir(source_folder)
        files = [file for file in files if file.endswith(".jpg")]
        for file in files:
            image = cv2.imread(os.path.join(source_folder, file))
            h, w, _ = image.shape
            rectangle = [1,1,w-5,h-5]
            file_path = os.path.join(destiny_folder, uuid.uuid4().hex + ".png")
            image_generated = grabcut(img_orig=image, rect_final=rectangle, destiny_filepath=file_path)
            print(image_generated)


