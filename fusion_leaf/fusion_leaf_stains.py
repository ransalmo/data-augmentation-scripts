import random
import numpy as np
from PIL import Image
import os
import cv2
import uuid
import shutil
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom


def prettify(elem):
  rough_string = tostring(elem, 'utf-8', method="xml")
  reparsed = minidom.parseString(rough_string)
  return reparsed.toprettyxml(indent="  ")


def generate_pascal_voc_xml(path_to_save, image_name, main_class_name, image_height, image_width, main_x1, main_y1, main_x2, main_y2, other_bnd_boxes):
  if not os.path.exists(path_to_save):
      os.makedirs(path_to_save)
  xmlPath = os.path.join(path_to_save, image_name).replace('.jpg', '.xml')
  top = Element('annotation')
  comment = Comment('Autogenerated by the script')
  top.append(comment)
  folderChild = SubElement(top, 'folder')
  folderChild.text = path_to_save
  fileNameChild = SubElement(top, 'filename')
  fileNameChild.text = image_name
  sizeChild = SubElement(top, 'size')
  widthChild = SubElement(sizeChild, 'width')
  widthChild.text = str(image_width)
  heightChild = SubElement(sizeChild, 'height')
  heightChild.text = str(image_height)
  depthChild = SubElement(sizeChild, 'depth')
  depthChild.text = '3'
  segmentedChild = SubElement(top, 'segmented')
  segmentedChild.text = '0'

  object = SubElement(top, 'object')
  name = SubElement(object, 'name')
  name.text = main_class_name
  pose = SubElement(object, 'pose')
  pose.text = "Unspecified"
  truncated = SubElement(object, 'truncated')
  truncated.text = '0'
  difficult = SubElement(object, 'difficult')
  difficult.text = '0'
  bndbox = SubElement(object, 'bndbox')
  xmin = SubElement(bndbox, 'xmin')
  xmin.text = str(main_x1)
  ymin = SubElement(bndbox, 'ymin')
  ymin.text = str(main_y1)
  xmax = SubElement(bndbox, 'xmax')
  xmax.text = str(main_x2)
  ymax = SubElement(bndbox, 'ymax')
  ymax.text = str(int(main_y2))

  for other_bnd_box in other_bnd_boxes:
      object = SubElement(top, 'object')
      name = SubElement(object, 'name')
      name.text = other_bnd_box[0]
      pose = SubElement(object, 'pose')
      pose.text = "Unspecified"
      truncated = SubElement(object, 'truncated')
      truncated.text = '0'
      difficult = SubElement(object, 'difficult')
      difficult.text = '0'
      bndbox = SubElement(object, 'bndbox')
      xmin = SubElement(bndbox, 'xmin')
      xmin.text = str(other_bnd_box[1])
      ymin = SubElement(bndbox, 'ymin')
      ymin.text = str(other_bnd_box[2])
      xmax = SubElement(bndbox, 'xmax')
      xmax.text = str(other_bnd_box[3])
      ymax = SubElement(bndbox, 'ymax')
      ymax.text = str(int(other_bnd_box[4]))

  str_xml = prettify(top)
  f = open(xmlPath, "w")
  f.write(str_xml)
  f.close()
  return str_xml


def generate_binary_image(original_image_path):
    try:
        original_image = cv2.imread(original_image_path)
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        #127
        (thresh, black_and_white_image) = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
        return black_and_white_image
    except:
        print("Failed with the original image path: {0}".format(original_image_path))


def is_valid_position(binary_image, coordinates):
    x1, y1, x2, y2 = coordinates
    height, width = binary_image.shape
    if x1 >= width or x2 >= width or y1 >= height or y2 >= height:
        return False
    crop_image = binary_image[y1:y2, x1:x2]
    avg_color_per_row = np.average(crop_image, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    return True if avg_color == 0 else False


"rectangle comes in form [x1, y1, x2, y2]"
def is_overlap(rectangle1, rectangle2):
    if (rectangle1[0] >= rectangle2[2]) or \
            (rectangle1[2] <= rectangle2[0]) or \
            (rectangle1[3] <= rectangle2[1]) or \
            (rectangle1[1] >= rectangle2[3]):
        return False
    else:
        return True


def overlaps(to_find, coordinates):
    for coordinate in coordinates:
        if is_overlap(to_find, coordinate):
            return True
    return False


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


def calculate_max_x_y(image_arr, box_height, box_width):
    good_fit_positions = []
    width, height = image_arr.shape
    check_arr = image_arr.tolist()
    np.seterr(divide='ignore')
    for y in range(0, height, box_height):
        for x in range(0, width, box_width):
            try:
                sub_img = image_arr[y:box_height+y, x:box_width+x]
                avg_color_per_row = np.mean(sub_img, axis=0)
                avg_color = np.mean(avg_color_per_row, axis=0)
                if avg_color == 0:
                    good_fit_positions.append([x, y])
            except:
                pass
    return good_fit_positions


def generate_synthetic_images(leaf_source_folder, stains_source_folder, destiny_folder, to_generate = 200, max_stains = 15, max_tries = 20):
    leaf_files = [file for file in os.listdir(leaf_source_folder) if not file.startswith('.') and file.endswith("jpg") or file.endswith("jpeg") and not file.startswith(".")]
    stains_files = [file for file in os.listdir(stains_source_folder) if not file.startswith('.') and file.endswith("png") and not file.startswith(".")]
    annotations_path = os.path.join(destiny_folder, "annotations")
    max_tries = 5
    if not os.path.exists(destiny_folder):
        os.makedirs(destiny_folder)
    if not os.path.exists(annotations_path):
        os.makedirs(annotations_path)

    for i in range(to_generate):
        print("Generating image {0}".format(i))
        base_name = "syntetic_" + str(uuid.uuid4().hex)
        new_image_name = base_name + ".jpg"
        new_xml_file = base_name + ".xml"
        used_rectangles = []
        bound_boxes = []
        tries = 0
        leaf_file = random.choice(leaf_files)
        binary_leaf = generate_binary_image(os.path.join(leaf_source_folder, leaf_file))
        print("Saving binary image for testing")
        cv2.imwrite(os.path.join(destiny_folder,"binary.png"),binary_leaf)
        height, width = binary_leaf.shape

        main_x1 = 5
        main_y1 = 5
        main_x2 = width - 5
        main_y2 = height - 5
        # copy leaf file
        print("Copy new leaf file")
        shutil.copyfile(os.path.join(leaf_source_folder, leaf_file), os.path.join(destiny_folder, new_image_name))
        stains_to_generate = random.randrange(1, max_stains)
        print("Stains to generate: {0}".format(stains_to_generate))
        for k in range(stains_to_generate):
            print("Stain to generate number: {0}".format(k))
            tries = 0
            while True:
                stain_file = random.choice(stains_files)
                stain_image = cv2.imread(os.path.join(stains_source_folder, stain_file))
                stain_height, stain_width, _ = stain_image.shape
                valid_positions = calculate_max_x_y(binary_leaf, stain_width, stain_height)
                print("Valid positions generated")
                if len(valid_positions) == 0:
                    print("No valid positions skipping")
                    break
                print("Selecting s random position")
                x1, y1 = random.choice(valid_positions)
                print("Positions selected: {0} {1}".format(x1, y1))
                print("checking if overlaps")
                valid = is_valid_position(binary_leaf, [x1, y1, x1 + stain_width, y1 + stain_height])
                if overlaps([x1, y1, x1 + stain_width, y1 + stain_height], used_rectangles) or not valid:
                    print("Overlap or invalid position detected")
                    tries = tries + 1
                    print("Incrementing tries count to {0}".format(tries))
                elif tries == max_tries:
                    print("skipping...")
                    break
                else:
                    print("Blending images")
                    class_name = stain_file.split("_")[0]
                    used_rectangles.append([x1, y1, x1 + stain_width, y1 + stain_height])
                    bound_boxes.append([class_name, x1, y1, x1 + stain_width, y1 + stain_height])
                    new_leaf_image_arr = np.array(Image.open(os.path.join(destiny_folder, new_image_name)))
                    img_overlay_rgba = np.array(Image.open(os.path.join(stains_source_folder, stain_file)))

                    # Perform blending
                    alpha_mask = img_overlay_rgba[:, :, 3] / 255.0
                    img_result = new_leaf_image_arr[:, :, :3].copy()
                    img_overlay = img_overlay_rgba[:, :, :3]
                    overlay_image_alpha(img_result, img_overlay, x1, y1, alpha_mask)
                    Image.fromarray(img_result).save(os.path.join(destiny_folder, new_image_name))
                    print("Blending done")
                    break

        # generate xml
        print("Generating xml for image: {0}".format(new_image_name))
        generate_pascal_voc_xml(annotations_path, new_image_name, "hoja", height, width, main_x1, main_y1, main_x2, main_y2, bound_boxes)
        print("Image {0} generated, image number {1}".format(i, k))


