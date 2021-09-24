import argparse
import os
import shutil
import xml.etree.ElementTree as ET


def fixFilenameXML(xmlPath):
    filePath, fileName = os.path.split(xmlPath)
    # change xml metadata
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    for fileNameXML in root.iter('filename'):
        fileNameXML.text = fileNameXML.text.replace(".xml", ".jpg")
    tree.write(xmlPath)
    return


def fixCoordinatesXML(xmlPath):
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    print(xmlPath)
    for bndBoxXML in root.iter('bndbox'):
        children = bndBoxXML.getchildren()
        xmin = children[0].text
        ymin = children[1].text
        xmax = children[2].text
        ymax = children[3].text
        print("Coordenadas originales {0} {1} {2} {3}".format(xmin, ymin, xmax, ymax))

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

        children[0].text = str(xmin)
        children[1].text = str(ymin)
        children[2].text = str(xmax)
        children[3].text = str(ymax)

        print("Coordenadas nuevas {0} {1} {2} {3}".format(xmin, ymin, xmax, ymax))
    tree.write(xmlPath)

    return


def main(args):
    if not os.path.exists(args.path):
        raise ValueError("The source folder doesn't exist, please check the path")
    files = [file for file in os.listdir(args.path) if file.endswith(".xml") or file.endswith(".XML")]
    filesToProcess = len(files)
    print("Files to process: {0}".format(filesToProcess))
    for index, file in enumerate(files):
        filePath = os.path.join(args.path, file)
        print("Processing rotating image {0}".format(index + 1))
        fixCoordinatesXML(filePath)
        # fixFilenameXML(filePath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="folder path were images are located",
                        default=os.path.join(os.getcwd(), "images", "annotations"))
    args = parser.parse_args()
    main(args)
