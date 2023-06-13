import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

def meanFilter (image):
	filteredImage= np.zeros_like(image)
	for x in range(1, image.shape[0]-2) :
		for y in range(1, image.shape[1]-2) :
			for z in range(1, image.shape[2]-2) :
				avg = 0
				for dx in range(-1, 1) :
					for dy in range(-1, 1) :
						for dz in range(-1, 1) :
							avg = avg + image[x+dx, y+dy, z+dz]

				filteredImage[x+1, y+1, z+1] = avg / 27
    
	return filteredImage
  
def medianFilter (image):
	filteredImage = np.zeros_like(image)
	for x in range(1, image.shape[0]-2) :
		for y in range(1, image.shape[1]-2) :
			for z in range(1, image.shape[2]-2) :
				neightbours = []
				for dx in range(-1, 1) :
					for dy in range(-1, 1) :
						for dz in range(-1, 1) :
							neightbours.append(image[x+dx, y+dy, z+dz])

				median = np.median(neightbours)
				filteredImage[x+1, y+1, z+1] = median
    
	return filteredImage

def medianFilterBorders (image):
  # Median Filter with borders
	threshold = 2500
	filtered_image = np.zeros_like(image)

	for x in range(1, image.shape[0] - 2):
		for y in range(1, image.shape[1] - 2):
			for z in range(1, image.shape[2] - 2):
        # Compute the derivatives in x, y, and z directions
				dx = image[x + 1, y, z] - image[x - 1, y, z]
				dy = image[x, y + 1, z] - image[x, y - 1, z]
				dz = image[x, y, z + 1] - image[x, y, z - 1]

        # Compute the magnitude of the gradient
				magnitude = np.sqrt(dx * dx + dy * dy + dz * dz)

                    # Separate pixels based on the current threshold
				below_threshold = magnitude[magnitude < threshold]
				above_threshold = magnitude[magnitude >= threshold]

				# if below_threshold.size > 0 and above_threshold.size > 0:
        #             # Calculate the new threshold as the average of below_threshold and above_threshold
				# 	threshold = (np.mean(below_threshold) + np.mean(above_threshold)) / 2
				# elif below_threshold.size > 0:
				# 	threshold = np.mean(below_threshold)
				# elif above_threshold.size > 0:
				# 	threshold = np.mean(above_threshold)
				# else:
				# 	threshold = threshold
				threshold = (np.mean(below_threshold) + np.mean(above_threshold)) / 2

				if magnitude < threshold:
					neighbours = []
					for dx in range(-1, 2):
						for dy in range(-1, 2):
							for dz in range(-1, 2):
								neighbours.append(image[x + dx, y + dy, z + dz])
					median = np.median(neighbours)
					filtered_image[x, y, z] = median
				else:
					filtered_image[x, y, z] = image[x, y, z]
	return filtered_image