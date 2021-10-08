import fusion_leaf.fusion_leaf_stains

leaf_source_folder = "/Users/randysalas/Documents/Roya/Healthy"

stains_source_folder = "/Users/randysalas/Documents/Roya/Stains"

destiny_folder = "/Users/randysalas/Documents/Roya/Fake"

to_generate = 50

fusion_leaf.fusion_leaf_stains.generate_synthetic_images(leaf_source_folder,
                                                         stains_source_folder, destiny_folder, to_generate=to_generate)

