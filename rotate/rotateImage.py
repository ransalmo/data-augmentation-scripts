import cv2
import imutils
import math
import argparse
import os
import shutil
import xml.etree.ElementTree as ET



def rotatePoint(x, y, angle, height, width):
    x = int(x)
    y = int(y)

    xCalc = math.cos(math.radians(angle)) * x - math.sin(math.radians(angle)) * y
    yCalc = math.sin(math.radians(angle)) * x + math.cos(math.radians(angle)) * y
    if xCalc < 0:
        xCalc = xCalc + height
    if yCalc < 0:
        yCalc = yCalc + width

    return [xCalc, yCalc]


def rotateImage(path, destinyPath, degree, prefix = "rotated_270_"):
    image = cv2.imread(path)
    filePath, fileName = os.path.split(path)
    newFileName = prefix + "_" + fileName
    newPath = os.path.join(destinyPath, newFileName)
    rotatedImage = imutils.rotate_bound(image, int(degree))
    cv2.imwrite(newPath, rotatedImage)
    return


def renameXML(originalPath, newPath, imageFile):
    filePath, fileName = os.path.split(originalPath)
    try:
        shutil.copy(originalPath, newPath)
        #change xml metadata
        tree = ET.parse(newPath)
        root = tree.getroot()
        for fileNameXML in root.iter('filename'):
            fileNameXML.text = imageFile
        tree.write(newPath)
    except:
        print("Problemas procesando el archivo {0}".format(originalPath))


def modifyCoordinatesXML(xmlPath, angle):
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    width = 0
    height = 0
    print(xmlPath)
    angle = int(angle)
    for sizeXML in root.iter('size'):
        sizeChildren = sizeXML.getchildren()
        width = sizeChildren[0].text
        height = sizeChildren[1].text
        if angle == 90 or angle == 270:
            sizeChildren[0].text = height
            sizeChildren[1].text = width
        tree.write(xmlPath)
    for bndBoxXML in root.iter('bndbox'):
        children = bndBoxXML.getchildren()
        xmin = children[0].text
        ymin = children[1].text
        xmax = children[2].text
        ymax = children[3].text
        print("Coordenadas originales {0} {1} {2} {3}".format(xmin, ymin, xmax, ymax))
        xmin, ymin = rotatePoint(xmin, ymin, angle, int(height), int(width))
        xmax, ymax = rotatePoint(xmax, ymax, angle, int(height), int(width))

        if int(ymax) < int(ymin):
            print("Coordinates swapping y")
            temp = ymin
            ymin = ymax
            ymax = temp

        if int(xmax) < int(xmin):
            print("Coordinates swapping x")
            temp = xmin
            xmin = xmax
            xmax = temp


        children[0].text = str(round(xmin))
        children[1].text = str(round(ymin))
        children[2].text = str(round(xmax))
        children[3].text = str(round(ymax))

        print("Coordenadas nuevas {0} {1} {2} {3}".format(children[0].text, children[1].text, children[2].text, children[3].text))
        tree.write(xmlPath)

    return


def main(args):
    if args.degrees not in ["90","180","270","360"]:
        raise ValueError('The specified degree is not supported')
    prefix_text = "rotated_" + str(args.degrees) + "_"
    if not os.path.exists(args.path):
        raise ValueError("The source folder doesn't exist, please check the path")
    if not os.path.exists(args.destiny):
        os.makedirs(args.destiny)
    if not os.path.exists(os.path.join(args.destiny,'annotations')):
        os.makedirs(os.path.join(args.destiny,'annotations'))
    files = [file for file in os.listdir(args.path) if file.endswith(".jpg") or file.endswith(".JPG")]
    filesToProcess = len(files)
    print("Files to process: {0}".format(filesToProcess))
    for index, file in enumerate(files):
        filePath = os.path.join(args.path, file)
        print("Processing rotating image {0}".format(index + 1))
        rotateImage(filePath, args.destiny, args.degrees, prefix_text)
        print("Generating new XML for image {0}".format(index + 1))
        originalXMLPath = os.path.join(args.path, 'annotations',file.replace('.jpg','.xml').replace('.JPG','.xml'))
        newXMLFile = prefix_text + "_" + file.replace('.jpg','.xml')
        newXMLPath = os.path.join(args.destiny, 'annotations', newXMLFile)
        renameXML(originalXMLPath, newXMLPath, newXMLFile)
        modifyCoordinatesXML(newXMLPath, args.degrees)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="folder path were images are located", default= os.path.join(os.getcwd(), "images"))
    parser.add_argument("--degrees", help="degrees to rotate 90-180-270-360", default="90")
    parser.add_argument("--destiny", help="destiny path for new images and annotations", default=os.path.join(os.getcwd(), "results"))
    args = parser.parse_args()
    main(args)
