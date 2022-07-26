import os
import shutil

images_path = "/Volumes/Randy/data/backgroundsV2"
annotations_path = os.path.join(images_path, "annotations")

images = [file for file in os.listdir(images_path) if not file.startswith(".") and (file.endswith("jpg") or file.endswith("jpeg"))]

annotations = [file for file in os.listdir(annotations_path) if not file.startswith(".") and (file.endswith("xml") or file.endswith("XML"))]


for image in images:
    xml_file = image.replace(".jpg", ".xml").replace(".jpeg",".xml")
    if not os.path.exists(os.path.join(annotations_path, xml_file)):
        os.remove(os.path.join(images_path, image))
        print("Incomplete file {0} removed".format(image))

for annotation in annotations:
    image = image.replace(".xml", ".jpg")
    if not os.path.exists(os.path.join(images_path, image)):
        os.remove(os.path.join(annotations_path, annotation))
        print("Incomplete file {0} removed".format(annotation))
