import ilumination.ilumination
import edge_enhacement.edge_enhacement
import motion_blur.motion_blur
import contrast.contrast

# source_folder = "/Volumes/Randy/data/synteticv2"
# destiny_folder = "/Volumes/Randy/data/synteticv2_filters"

source_folder = "/Volumes/Randy/data/original_train"
destiny_folder = "/Volumes/Randy/data/original_train_filters"

print("Contrast")
contrast.contrast.generate_contrtast_pictures(source_folder, destiny_folder)
print("Motion blur horizontal")
motion_blur.motion_blur.generate_motion_blur_pictures(source_folder, destiny_folder)
print("Motion blur vertical")
motion_blur.motion_blur.generate_motion_blur_pictures(source_folder, destiny_folder, horizontal=False)
print("Edge enhacement")
edge_enhacement.edge_enhacement.generate_edge_enhacement_pictures(source_folder, destiny_folder)
print("Ilumination")
ilumination.ilumination.generate_gamma_corrected_images(source_folder, destiny_folder)
print("Done!!!")







