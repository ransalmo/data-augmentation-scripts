import random
import numpy as np
from PIL import Image
import os
import cv2
import uuid
import shutil
import xml.etree.ElementTree as ET


def fixFilenameXML(xmlPath):
    filePath, fileName = os.path.split(xmlPath)
    #change xml metadata
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    for fileNameXML in root.iter('filename'):
        fileNameXML.text = fileNameXML.text.replace(".xml", ".jpg")
    tree.write(xmlPath)
    return


def overlay_image_alpha(img, img_overlay, x, y, alpha_mask):
    """Overlay `img_overlay` onto `img` at (x, y) and blend using `alpha_mask`.

    `alpha_mask` must have same HxW as `img_overlay` and values in range [0, 1].
    """
    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    # Blend overlay within the determined ranges
    img_crop = img[y1:y2, x1:x2]
    img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
    alpha = alpha_mask[y1o:y2o, x1o:x2o, np.newaxis]
    alpha_inv = 1.0 - alpha

    img_crop[:] = alpha * img_overlay_crop + alpha_inv * img_crop


def grabcut_temp(img_orig, rect_final, destiny_filepath):
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
    cv2.imwrite(destiny_filepath, img_orig)


def crop_picture_arr(image, new_height, new_width):
    h, w, _ = image.shape
    crop_img = None
    if new_height >= h and new_width >= w:
        raise ValueError("Does not make sense resize to the same size")
    else:
        crop_img = image[new_height, new_width]
    return crop_img


def resize(image, height, width):
    points = (width, height)
    resized_image = cv2.resize(image, points, interpolation=cv2.INTER_LINEAR)
    return resized_image


def create_new_image_with_backcground(source_folder, destiny_folder, backgrounds_path):
    destiny_annotations_folder = os.path.join(destiny_folder, "annotations")
    if not os.path.exists(os.path.join(source_folder, "annotations")):
        raise ValueError("The annotations folder is mandatory")
    if not os.path.exists(destiny_folder):
        os.makedirs(destiny_folder)
    if not os.path.exists(destiny_annotations_folder):
        os.makedirs(destiny_annotations_folder)
    images = [file for file in os.listdir(source_folder) if file.endswith("jpg") or file.endswith("jpeg")]
    backgrounds = [file for file in os.listdir(backgrounds_path) if file.endswith("jpg") or file.endswith("jpeg")]
    for image in images:
        try:
            background_file = random.choice(backgrounds)
            temp_back = cv2.imread(os.path.join(backgrounds_path, background_file))
            temp_image = cv2.imread(os.path.join(source_folder, image))
            height_back, width_back, _ = temp_back.shape
            height_image, width_image, _ = temp_image.shape
            if height_back >= height_image and width_back >= width_image:
                temp_back = crop_picture_arr(temp_back, height_image, width_image)
            else:
                temp_back = resize(temp_back, height_image, width_image)
            back_ground_temp_path = os.path.join(os.getcwd(), "wkr_background.jpg")
            cv2.imwrite(back_ground_temp_path, temp_back)
            leaf_temp_path = os.path.join(os.getcwd(), "wkr_image.png")
            grabcut_temp(temp_image, [5,5,width_image-5,height_image-5], leaf_temp_path)

            # Prepare inputs
            img = np.array(Image.open(back_ground_temp_path))
            img_overlay_rgba = np.array(
                Image.open(leaf_temp_path))

            # Perform blending
            alpha_mask = img_overlay_rgba[:, :, 3] / 255.0
            img_result = img[:, :, :3].copy()
            img_overlay = img_overlay_rgba[:, :, :3]
            overlay_image_alpha(img_result, img_overlay, 0, 0, alpha_mask)

            base_file_name = "back_aug_"+str(uuid.uuid4().hex)

            # Save result
            Image.fromarray(img_result).save(os.path.join(destiny_folder, base_file_name + ".jpg"))
            # Copy XML and rename it as
            xml_file_name_to_copy = (image.replace(".jpg",".xml")).replace(".jpeg",".xml")
            shutil.copy(os.path.join(source_folder, "annotations", xml_file_name_to_copy),
                        os.path.join(destiny_annotations_folder, xml_file_name_to_copy))
            #modify XML file information to match with the new file
            fixFilenameXML(os.path.join(destiny_annotations_folder, xml_file_name_to_copy))
        except:
            print("Got an error during processing...")
            continue

