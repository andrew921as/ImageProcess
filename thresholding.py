
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

def regionGrowing (image, x, y, z, tol):
	# Region Growing
        segmentation = np.zeros_like(image)
        if segmentation[x,y,z] == 1:
            return
        valor_medio_cluster = image[x,y,z]
        segmentation[x,y,z] = 1
        vecinos = [(x, y, z)]
        while vecinos:
            x, y, z = vecinos.pop()
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    for dz in [-1,0,1]:
                        #vecino
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if nx >= 0 and nx < image.shape[0] and \
                            ny >= 0 and ny < image.shape[1] and \
                            nz >= 0 and nz < image.shape[2]:
                            if np.abs(valor_medio_cluster - image[nx,ny,nz]) < tol and \
                                segmentation[nx,ny,nz] == 0:
                                segmentation[nx,ny,nz] = 1
                                vecinos.append((nx, ny, nz))
        return segmentation

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

def borders(image_data):
	dfdx = np.zeros_like(image_data)
	dfdy = np.zeros_like(image_data)
	dfdz = np.zeros_like(image_data)
	for x in range(1, image_data.shape[0]-2) :
		for y in range(1, image_data.shape[1]-2) :
			for z in range(1, image_data.shape[2]-2) :
				dfdx[x, y, z] = image_data[x+1, y, z]-image_data[x-1, y, z]
				dfdy[x, y, z] = image_data[x, y+1, z]-image_data[x, y-1, z]
				dfdz[x, y, z] = image_data[x, y, z+1]-image_data[x, y, z-1]
	magnitude = np.sqrt(np.power(dfdx, 2) + np.power(dfdy, 2) + np.power(dfdz, 2))
	return magnitude
