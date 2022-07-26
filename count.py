import os

images_synthetic_background = [file for file in os.listdir("/Volumes/Randy/data/backgroundsV2_filters") if not file.startswith(".") and (file.endswith(".jpg") or file.endswith(".jpeg"))]
images_synthetic = [file for file in os.listdir("/Volumes/Randy/data/synteticv2_filters") if not file.startswith(".") and (file.endswith(".jpg") or file.endswith(".jpeg"))]
images_original = [file for file in os.listdir("/Volumes/Randy/data/original_train") if not file.startswith(".") and (file.endswith(".jpg") or file.endswith(".jpeg"))]
strains = [file for file in os.listdir("/Volumes/Randy/data/strains") if not file.startswith(".") and (file.endswith(".png"))]
backgrounds = [file for file in os.listdir("/Volumes/Randy/data/backgrounds") if not file.startswith(".") and (file.endswith(".jpg") or file.endswith(".jpeg"))]
full = [file for file in os.listdir("/Volumes/Randy/data/trainV2") if not file.startswith(".") and (file.endswith(".jpg") or file.endswith(".jpeg"))]
healthy = [file for file in os.listdir("/Volumes/Randy/data/healthy") if not file.startswith(".") and (file.endswith(".jpg") or file.endswith(".jpeg"))]

print("Cantidad de manchas utilizadas: {0}".format(len(strains)))
print("Cantidad de imagenes conjunto de entrenamiento original: {0}".format(len(images_original)))
print("Cantidad de imagenes conjunto de entrenamiento sintetico: {0}".format(len(images_synthetic)))
print("Cantidad de imagenes conjunto de entrenamiento con fondo sintético: {0}".format(len(images_synthetic_background)))
print("Cantidad de imagenes conjunto de entrenamiento aumentado: {0}".format(len(full)))
print("Cantidad de imagenes sanas: {0}".format(len(healthy)))

