import ilumination
import edge_enhacement
import motion_blur
import contrast

source_folder = ""
destiny_folder = ""

print("Contrast")
contrast.Contrast.generate_contrtast_pictures(source_folder, destiny_folder)
print("Motion blur horizontal")
motion_blur.MotionBlur.generate_motion_blur_pictures(source_folder, destiny_folder)
print("Motion blur vertical")
motion_blur.MotionBlur.generate_motion_blur_pictures(source_folder, destiny_folder, horizontal=False)
print("Edge enhacement")
edge_enhacement.EdgeEnhacement.generate_edge_enhacement_pictures(source_folder, destiny_folder)
print("Ilumination")
ilumination.IIumination.generate_gamma_corrected_images(source_folder, destiny_folder)
print("Rotate images")







