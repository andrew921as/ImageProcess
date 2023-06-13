import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy import stats as st
import statistics as stat


def Rescaling(imageData):
	plt.hist(imageData[imageData>10].flatten(), 100)
	minValue = imageData.min()
	maxValue = imageData.max()
	imageDataRescaled = (imageData - minValue) / (maxValue - minValue)
	# histogram =plt.hist(imageDataRescaled[imageDataRescaled>0.01].flatten(), 100)
	histogram =imageDataRescaled[imageDataRescaled>0.01].flatten()
	return imageDataRescaled, histogram
 

def ZScore(imageData):
	meanValue = imageData[imageData > 10].mean()
	standardDeviationValue = imageData[imageData > 10].std()
	imageDataRescaled = (imageData - meanValue) / (standardDeviationValue)
	# histogram = plt.hist(imageDataRescaled.flatten(), 100)
	histogram =imageDataRescaled.flatten()
	return imageDataRescaled,histogram

def WhiteStripe(imageData):
	hist, binEdges = np.histogram(imageData.flatten(), bins=100)
 	# Encontrar los picos del histograma
	picos, _ = find_peaks(hist, height=100)
	valPicos=binEdges[picos]
	# Imagen reecalada
	imageDataRescaled=imageData/valPicos[1]

	histogram =imageDataRescaled.flatten()
	return imageDataRescaled, histogram

def histogramMatching(imgOrigin,target, k):
    #histogram
    data_target = None
    if target == 1:
      data_target = nib.load("./histogramI/FLAIR.nii.gz").get_fdata()
    elif target == 2:
      data_target = nib.load("./histogramI/IR.nii.gz").get_fdata()
    else:
      data_target = nib.load("./histogramI/T1.nii.gz").get_fdata()
    
    data_orig = imgOrigin

    # Redimensionar los datos en un solo arreglo 1D
    reference_flat = data_target.flatten()
    transform_flat = data_orig.flatten()
    
    reference_landmarks = np.percentile(reference_flat, np.linspace(0, 100, k))
    transform_landmarks = np.percentile(transform_flat, np.linspace(0, 100, k))

    
    piecewise_func = np.interp(transform_flat, transform_landmarks, reference_landmarks)
    transformed_data = piecewise_func.reshape(data_orig.shape)

    # Aplicar el mapeo a los datos de la imagen de origen
    histogram = transformed_data.flatten()

    return transformed_data, histogram
  