import rotate.rotate

source_folder = "/Users/randysalas/Documents/Roya/Images"
destiny_folder = "/Users/randysalas/Documents/Roya/Rotated"

rotate.rotate.rotate_images(source_folder, destiny_folder, True, 50, [90, 180])
rotate.rotate.rotate_images(source_folder, destiny_folder, True, 60, [270])

