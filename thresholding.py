
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

