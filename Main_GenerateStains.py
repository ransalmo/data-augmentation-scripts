import syntetic_rust
import os

images_path = ""

xml_path = os.path.join(images_path, "annotations")

classes = ['espora', 'translucido']

result_path = ""

syntetic_rust.StainsGenerator.generate_stains(images_path, xml_path, classes, result_path)
syntetic_rust.FilterNonOptimal.remove_bad_candidates(result_path)