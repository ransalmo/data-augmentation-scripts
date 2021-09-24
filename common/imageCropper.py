import cv2
import os
import argparse
import pandas as pd
import xml.etree.ElementTree as ET
import uuid
from PIL import Image
import numpy as np
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

ANNOTATIONS_FOLDER = 'annotations'


def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)


def bndBoxIndex(member):
    for index, property in enumerate(member):
        if property.tag == 'bndbox':
            return index
    return -1


def prettify(elem):
  rough_string = tostring(elem, 'utf-8', method="xml")
  reparsed = minidom.parseString(rough_string)
  return reparsed.toprettyxml(indent="  ")


def getCroppedImage(img_arr, x1, x2, y1, y2):
    crop_img = img_arr[y1 : y2, x1: x2]
    return crop_img


def generateIndividualCrop(sourcePath, x1, y1, x2, y2):
    return "hello"


def generatePascalVOCXML(filePath, imageName, className, imageHeight, imageWidth, x1, y1, x2, y2):
  directoryPath, fileNameXML = os.path.split(filePath)
  xmlPath = filePath
  top = Element('annotation')
  comment = Comment('Autogenerated by the script')
  top.append(comment)
  folderChild = SubElement(top, 'folder')
  folderChild.text = directoryPath
  fileNameChild = SubElement(top, 'filename')
  fileNameChild.text = imageName
  sizeChild = SubElement(top, 'size')
  widthChild = SubElement(sizeChild, 'width')
  widthChild.text = str(imageWidth)
  heightChild = SubElement(sizeChild, 'height')
  heightChild.text = str(imageHeight)
  depthChild = SubElement(sizeChild, 'depth')
  depthChild.text = '3'
  segmentedChild = SubElement(top, 'segmented')
  segmentedChild.text = '0'

  object = SubElement(top, 'object')
  name = SubElement(object, 'name')
  name.text = className
  pose = SubElement(object, 'pose')
  pose.text = "Unspecified"
  truncated = SubElement(object, 'truncated')
  truncated.text = '0'
  difficult = SubElement(object, 'difficult')
  difficult.text = '0'
  bndbox = SubElement(object, 'bndbox')
  xmin = SubElement(bndbox, 'xmin')
  xmin.text = str(x1)
  ymin = SubElement(bndbox, 'ymin')
  ymin.text = str(y1)
  xmax = SubElement(bndbox, 'xmax')
  xmax.text = str(x2)
  ymax = SubElement(bndbox, 'ymax')
  ymax.text = str(int(y2))

  str_xml = prettify(top)
  f = open(xmlPath, "w")
  f.write(str_xml)
  f.close()
  return str_xml


def processImages(images, sourcePath, destinyPath):
    count_original_pictures = len(images)
    processed_images = 1
    processed_annotations = 1
    imagesAnnotations = []
    flatAnnotations = []
    print("Images to extact tiles {0}".format(count_original_pictures))
    for index, imageFile in enumerate(images):
        print("Processing image {0} from {1}".format(index + 1, count_original_pictures))
        imagePath = os.path.join(source, imageFile)
        xmlFile = imageFile.replace(".jpg", ".xml")
        xmlFile = xmlFile.replace(".JPG", ".jpg")
        annotationFile = os.path.join(source, ANNOTATIONS_FOLDER, xmlFile)
        imagesAnnotations.append(getAnnotations(annotationFile))
        processed_images = processed_images + 1
    print("Cropping images...")
    imageBin = None
    imageNp = None
    for index, imageAnnotation in enumerate(imagesAnnotations):
            print("get image array for {0}".format(imageAnnotation[0][0]))
            imageBin = Image.open(os.path.join(sourcePath, imageAnnotation[0][0]))
            imageNp = load_image_into_numpy_array(imageBin)

            currentImage = imageAnnotation[0][0]
            for annotation in imageAnnotation:
                labelClass = annotation[1]
                labelX1 = annotation[2]
                labelY1 = annotation[3]
                labelX2 = annotation[4]
                labelY2 = annotation[5]
                imageCropped = getCroppedImage(imageNp, labelX1, labelX2, labelY1, labelY2)
                cropFileName = labelClass + "_" + str(uuid.uuid4()) + '_' + currentImage
                cropAnnotationFile = cropFileName.replace(".jpg",".xml")
                cropAnnotationFile = cropAnnotationFile.replace(".JPG",".xml")
                imageCropped = cv2.cvtColor(imageCropped, cv2.COLOR_BGR2RGB)
                imageCroppedPath = os.path.join(destinyPath, cropFileName)
                annotationCroppedPath = os.path.join(destinyPath, ANNOTATIONS_FOLDER, cropAnnotationFile)
                cv2.imwrite(imageCroppedPath, imageCropped)
                imageCroppedBin = Image.open(imageCroppedPath)
                cropWidth, cropHeight, = imageCroppedBin.size
                generatePascalVOCXML(annotationCroppedPath, cropFileName, labelClass, cropHeight, cropWidth, 0, 0, cropWidth, cropHeight)


def getAnnotations(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    annotations = []
    for index, member in enumerate(root.findall('object')):
        indexBndBox = bndBoxIndex(member)

        value = (root.find('filename').text,
                 member[0].text,
                 int(member[indexBndBox][0].text),
                 int(member[indexBndBox][1].text),
                 int(member[indexBndBox][2].text),
                 int(member[indexBndBox][3].text)
                 )
        annotations.append(value)

    return annotations


def checkSource(sourcePath, destinyPath):
    if not os.path.exists(sourcePath):
        raise ValueError("The source path do no exist, please correct the given path")

    if not os.path.exists(os.path.join(sourcePath, ANNOTATIONS_FOLDER)):
        raise ValueError("The source path does not have an annotations folder, the content is incomplete")

    if not os.path.exists(destinyPath):
        os.makedirs(destiny)

    if not os.path.exists(os.path.join(destiny, ANNOTATIONS_FOLDER)):
        os.makedirs(os.path.join(destiny, ANNOTATIONS_FOLDER))

    return True


def main(source, destiny):
    if checkSource(source, destiny):
        print("Source content looks valid....")
        # get pictures inside the source folder...
        images = [image for image in os.listdir(source) if image.endswith('.jpg') or image.endswith('.JPG')]
        processImages(images, source, destiny)
    return


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Utility to generate mini images from labeled objects from a bigger one.')
  parser.add_argument('--source', default=os.path.join(os.getcwd(), 'images'), help='source path')
  parser.add_argument('--destiny', default=os.path.join(os.getcwd(),'images','results'))
  args = parser.parse_args()
  source = vars(args)["source"]
  destiny = vars(args)["destiny"]
  print("Source path:{0}".format(source))
  print("Destiny path:{0}".format(destiny))
  main(source, destiny)