
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def isodata(image, tol, ta):	
		tau = ta
		istrue=True
		while istrue:
			#print(tau)

			segmentation = image >= tau
			mBG = image[np.multiply(image > 10, segmentation == 0)].mean()
			mFG = image[np.multiply(image > 10, segmentation == 1)].mean()

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

def kMeans (image, iterations ):
	k1 = np.amin(image)
	k2 = np.mean(image)
	k3 = np.amax(image)


	for i in range(0,iterations):
		d1 = np.abs(k1 - image)
		d2 = np.abs(k2 - image)
		d3 = np.abs(k3 - image)

		segmentation = np.zeros_like(image)
		segmentation[np.multiply(d1 < d2, d1 < d3)] = 0
		segmentation[np.multiply(d2 < d1, d2 < d3)] = 1
		segmentation[np.multiply(d3 < d1, d3 < d2)] = 2

		k1 = image[segmentation == 0].mean()
		k2 = image[segmentation == 1].mean()
		k3 = image[segmentation == 2].mean()
		return segmentation

