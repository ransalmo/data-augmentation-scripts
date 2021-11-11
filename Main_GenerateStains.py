import syntetic_rust.segmentation.segmentation
import syntetic_rust.stains_generator
import syntetic_rust.filter_non_optimal
import os


images_path = "/Users/randysalas/Documents/Roya/Test 9 Oct/images"
xml_path = os.path.join(images_path, "annotations")
classes = ['espora', 'translucido']
result_path = "/Users/randysalas/Documents/Roya/Stains2"
print("Croping stains to use")
syntetic_rust.stains_generator.generate_stains(images_path, xml_path, classes, result_path)
print("Removing non ideal candidates")
syntetic_rust.filter_non_optimal.remove_bad_candidates(result_path)

