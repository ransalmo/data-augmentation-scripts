# coding=utf-8

import os

import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt

path = os.path.join(os.getcwd(), 'images', 'annotations')

if not os.path.exists(path):
    raise ValueError('The images\\annotations firectory does not exist')
else:
    files = os.listdir(path)
    results = {}
    files = [file for file in files if file.endswith('.XML') or file.endswith('.xml')]
    for file in files:
        objectsDetected = 0
        filePath = os.path.join(path, file)
        tree = ET.parse(filePath)
        root = tree.getroot()
        for member in root.findall('object'):
            label = member[0].text
            if label != 'hoja' and label != 'dano':
                objectsDetected = objectsDetected + 1
        if objectsDetected in results:
            results[objectsDetected] = results[objectsDetected] + 1
        else:
            results[objectsDetected] = 1

    print("Cantidad de objetos, Cantidad de imagenes")
    for key, value in results.items():
        print("{0},{1}".format(key, value))


    plt.bar(list(results.keys()), results.values(), color='g', width=0.9)
    plt.ylabel('Cantidad de imágenes')
    plt.xlabel('Cantidad de objetos anotados (Excluyendo hojas y daños)')
    plt.show()