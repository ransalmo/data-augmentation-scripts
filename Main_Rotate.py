import rotate

source_folder = ""
destiny_folder = ""

rotate.RotateImages.rotate_images(source_folder, destiny_folder, True, 50, [90, 180])
rotate.RotateImages.rotate_images(source_folder, destiny_folder, True, 60, [270])

