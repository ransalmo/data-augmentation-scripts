import fusion_leaf.fusion_leaf_stains

leaf_source_folder = "/Users/randysalas/Desktop/data/healthy"

stains_source_folder = "/Users/randysalas/Desktop/data/strains"

destiny_folder = "/Users/randysalas/Desktop/data/generated"

to_generate = 2500

fusion_leaf.fusion_leaf_stains.generate_synthetic_images(leaf_source_folder,
                                                         stains_source_folder, destiny_folder, to_generate=to_generate)

print("Done")

