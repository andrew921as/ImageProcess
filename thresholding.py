
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def isodata(image, tol, ta):	
		tau = ta/100
		istrue=True
		while istrue:
			#print(tau)

			segmentation = image >= tau
			mBG = image[np.multiply(image > 0.001, segmentation == 0)].mean()
			mFG = image[np.multiply(image > 0.001, segmentation == 1)].mean()

			tau_post = 0.5 * (mBG + mFG)

			if np.abs(tau - tau_post) < tol:
				istrue=False
				return tau
			if (not tau_post) :
				istrue=False
				return tau
			else:
				tau = tau_post

def regionGrowing (image, point):
  return "hola"

def kMeans (image, iterations,ks ):
	# Inicialización de valores k
	k_values = np.linspace(np.amin(image), np.amax(image), ks)
	for i in range(iterations):
		d_values = [np.abs(k - image) for k in k_values]
		segmentationr = np.argmin(d_values, axis=0)

		for k_idx in range(ks):
			k_values[k_idx] = np.mean(image[segmentationr == k_idx])

	return segmentationr
	# k1 = np.amin(image)
	# k2 = np.mean(image)
	# k3 = np.amax(image)


	# for i in range(0,iterations):
	# 	d1 = np.abs(k1 - image)
	# 	d2 = np.abs(k2 - image)
	# 	d3 = np.abs(k3 - image)

	# 	segmentation = np.zeros_like(image)
	# 	segmentation[np.multiply(d1 < d2, d1 < d3)] = 0
	# 	segmentation[np.multiply(d2 < d1, d2 < d3)] = 1
	# 	segmentation[np.multiply(d3 < d1, d3 < d2)] = 2

	# 	k1 = image[segmentation == 0].mean()
	# 	k2 = image[segmentation == 1].mean()
	# 	k3 = image[segmentation == 2].mean()
	# 	return segmentation

