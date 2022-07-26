import fusion_leaf.fusion_leaf_stains

leaf_source_folder = "/Volumes/Randy/data/healthy"

stains_source_folder = "/Volumes/Randy/data/strains"

destiny_folder = "/Volumes/Randy/data/synteticv2"

to_generate = 2500

fusion_leaf.fusion_leaf_stains.generate_synthetic_images(leaf_source_folder,
                                                         stains_source_folder, destiny_folder, to_generate=to_generate)

print("Done")

