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