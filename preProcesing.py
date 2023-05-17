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

def histogramMatching(imgOrigin,target):
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
    flat_orig = data_orig.flatten()
    flat_target = data_target.flatten()

    # Calcular los histogramas acumulativos
    hist_orig, bins = np.histogram(flat_orig, bins=256, range=(0, 255), density=True)
    hist_orig_cumulative = hist_orig.cumsum()
    hist_target, _ = np.histogram(flat_target, bins=256, range=(0, 255), density=True)
    hist_target_cumulative = hist_target.cumsum()

    # Mapear los valores de la imagen de origen a los valores de la imagen objetivo
    lut = np.interp(hist_orig_cumulative, hist_target_cumulative, bins[:-1])

    # Aplicar el mapeo a los datos de la imagen de origen
    data_matched = np.interp(data_orig, bins[:-1], lut) 
    histogram = data_matched.flatten()
    # Crear una nueva imagen con los datos estandarizados
    # image_matched = nib.Nifti1Image(data_matched, imgOrigin.affine,imgOrigin.header)
    # data = image_matched.get_fdata()
    return data_matched, histogram
  