import fusion_leaf.fusion_leaf_stains

leaf_source_folder = "/Users/randysalas/Documents/Roya/Healthy2"

stains_source_folder = "/Users/randysalas/Documents/Roya/Stains2"

destiny_folder = "/Users/randysalas/Documents/Roya/Fake2"

to_generate = 200

fusion_leaf.fusion_leaf_stains.generate_synthetic_images(leaf_source_folder,
                                                         stains_source_folder, destiny_folder, to_generate=to_generate)

print("Done")

