import cv2
import numpy
import os

def image_colorfulness(image):
	# split the image into its respective RGB components
	(B, G, R) = cv2.split(image.astype("float"))
	# compute rg = R - G
	rg = numpy.absolute(R - G)
	# compute yb = 0.5 * (R + G) - B
	yb = numpy.absolute(0.5 * (R + G) - B)
	# compute the mean and standard deviation of both `rg` and `yb`
	(rbMean, rbStd) = (numpy.mean(rg), numpy.std(rg))
	(ybMean, ybStd) = (numpy.mean(yb), numpy.std(yb))
	# combine the mean and standard deviations
	stdRoot = numpy.sqrt((rbStd ** 2) + (ybStd ** 2))
	meanRoot = numpy.sqrt((rbMean ** 2) + (ybMean ** 2))
	# derive the "colorfulness" metric and return it
	return stdRoot + (0.3 * meanRoot)

def remove_bad_candidates(path_to_filter, file_extension = "png"):
	files = [file for file in os.listdir(path_to_filter) if file.endswith(file_extension)]
	for file in files:
		image = cv2.imread(os.path.join(path_to_filter, file))
		result = image_colorfulness(image)
		if result == 0.0:
			print("Removing the image is not useful")
			os.remove(os.path.join(path_to_filter, file))


remove_bad_candidates(os.path.join(os.getcwd(),'fusion_results'))