#Gui
#Gui
import sys
import os
import numpy as np
import SimpleITK as sitk
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QFileDialog
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#Funciones del programa
from thresholding import isodata, regionGrowing, kMeans, gmm, borders
from preProcesing import Rescaling, ZScore, WhiteStripe, histogramMatching
from denoising import meanFilter,medianFilter,medianFilterBorders
from register import MakeRegister

#Procesamiento de las imagenes
import nibabel as nib
import matplotlib.pyplot as plt

class MiEjemplo(QMainWindow):
  def __init__(self):
      super(MiEjemplo,self).__init__()
      loadUi("PruebasGUI.ui", self)
      self.HisComboBox.addItems(["T1", "FLAIR", "IR"])
      #Haciendo cosas de layouds
      self.horizontalL=QtWidgets.QHBoxLayout(self.frame)
      self.horizontalL.setObjectName("HorizontalL")
      #Fin
      #Agrego un canvas
      self.figure=plt.figure()
      self.canvas = FigureCanvas(self.figure)
      self.horizontalL.addWidget(self.canvas)
      #Fin
      self.searchButton.clicked.connect(self.browsefiles)
      self.uploadButton.clicked.connect(self.uploadImage)
      self.showHisButton.clicked.connect(self.showHistogram)
      self.showBordersButton.clicked.connect(self.showBorders)
      self.showImageButton.clicked.connect(self.showImage)
      self.miPrimerBoton.clicked.connect(self.controlBoton)
      self.downloadButton.clicked.connect(self.dowloadImage)
      self.searchButton_2.clicked.connect(self.browsefileRegister)
      self.registerButton.clicked.connect(self.registerFunction)
      
      self.sliderX.valueChanged.connect(self.axeXControl)
      self.sliderY.valueChanged.connect(self.axeYControl)
      self.sliderZ.valueChanged.connect(self.axeZControl)
      
      self.ejeX.valueChanged.connect(self.axeXControl)
      self.ejeY.valueChanged.connect(self.axeYControl)
      self.ejeZ.valueChanged.connect(self.axeZControl)

      self.rescalingRB.toggled.connect(lambda: self.standarizationControls("rescaling"))
      self.zScoreRB.toggled.connect(lambda: self.standarizationControls("zScore"))
      self.whiteStripeRB.toggled.connect(lambda: self.standarizationControls("white"))
      self.HistMatchRB.toggled.connect(lambda: self.standarizationControls("histo"))
      
      self.normalRB.toggled.connect(lambda: self.rbControls("normal"))  
      self.isodataRB.toggled.connect(lambda: self.rbControls("isodata"))
      self.regionRB.toggled.connect(lambda: self.rbControls("regionG"))
      self.kmeansRB.toggled.connect(lambda: self.rbControls("kMeans"))
      self.gmmRB.toggled.connect(lambda: self.rbControls("GMM"))
        
  image=None
  normalImage=None
  histogram = None
  normalHistogram = None
  imagePath = None
  
  def plotOnCanvas (self,imageAxes):
    self.figure.clear()
    plt.imshow(imageAxes)
    self.canvas.draw()
    
  def plotOnCanvasNormal (self,imageAxes):
    self.figure.clear()
    plt.imshow(imageAxes, cmap='gray')
    self.canvas.draw()
    
  def plotOnCanvasH (self,histogram):
    self.figure.clear()
    plt.hist(histogram,100)
    self.canvas.draw()
  
  def browsefiles(self):
    fileName = QFileDialog.getOpenFileName(self,'Open file', 'C:')
    self.inputLDireccionI.setText(fileName[0])
    self.imagePath = fileName[0]
  
  def browsefileRegister(self):
    fileName = QFileDialog.getExistingDirectory(self,'Open folder', 'C:')
    self.inputLDireccionI_2.setText(fileName)
    
  def dowloadImage(self):
    imageUploaded = nib.load(self.imagePath)
    affine = imageUploaded.affine
    reconstructed_image = nib.Nifti1Image(self.image.astype(np.float32), affine)
    output_path = os.path.join("segmentatedImgs", "segmentated.nii.gz")
    nib.save(reconstructed_image, output_path)
    
    self.inputLDireccionI_2.setEnabled(True)
    self.searchButton_2.setEnabled(True)
    self.registerButton.setEnabled(True)
    self.ImageDownLabel.setText("Image Downloaded")
  
  def volumes(self,imagePath):
    imageNoData= nib.load(imagePath)
    image_data_FLAIR=imageNoData.get_fdata()
    for i in range (self.KsSpinB.value()+1):
      count= np.count_nonzero(image_data_FLAIR.astype(np.int32) == i)
      tamaño_voxel = np.abs(imageNoData.affine.diagonal()[:3])
      volumen_en_mm3 = count * np.prod(tamaño_voxel)
      self.listItem.addItem("Label"+str(i)+": "+str(count)+", Volumen: "+str(volumen_en_mm3))
    
  def registerFunction(self):
    if (os.path.exists(self.inputLDireccionI_2.text()+"/FLAIR.nii.gz")):
      fixedImagePath= self.inputLDireccionI_2.text()
      movingImagePath=(self.imagePath)
      movingSegmentate = "segmentatedImgs/segmentated.nii.gz"
      #movingSegmentate = "segmentatedImgs/gaussian_segmentation.nii.gz"
      #finalimagePath = rigid_register(fixedImagePath,movingImagePath,movingSegmentate)
      finalimagePath = MakeRegister(fixedImagePath,movingImagePath,movingSegmentate)
   
      self.savedImaLabel.setText("Images registered in "+finalimagePath)
      self.volumes(finalimagePath)
  def uploadImage(self):
    if (os.path.exists(self.inputLDireccionI.text())):
        imageUploaded = nib.load(self.inputLDireccionI.text()).get_fdata()
        
        if (self.HisComboBox.currentText() == "FLAIR"):
          targ = 1
        elif (self.HisComboBox.currentText() == "IR"):
          targ = 2
        else:
          targ = 3
        imageStandarised=None
        histogram = None
        
        if self.rescalingRB.isChecked():
          imageStandarised, histogram= Rescaling(imageUploaded)
        if self.zScoreRB.isChecked():
          imageStandarised, histogram= ZScore(imageUploaded)
        if self.whiteStripeRB.isChecked():
          imageStandarised, histogram= WhiteStripe(imageUploaded)
        if self.HistMatchRB.isChecked():
          k = self.histogramSpinB.value()
          imageStandarised, histogram= histogramMatching(imageUploaded, targ,k)
        
        self.normalHistogram = histogram     
        
        
        if self.meanFilterRB.isChecked():
          self.image= meanFilter(imageStandarised)
        if self.medianFilterRB.isChecked():
          self.image= medianFilter(imageStandarised)
        if self.medianBorderFilterRB.isChecked():
          self.image= medianFilterBorders(imageStandarised)
        if self.noneFilterRB.isChecked():
          self.image= imageStandarised
          
        self.normalImage = self.image
        
        valueY = self.ejeY.value()
        imageAxes = self.image[:, valueY, :]
  
        self.sliderX.setMaximum(self.image.shape[0]-1)
        self.sliderY.setMaximum(self.image.shape[1]-1) 
        self.sliderZ.setMaximum(self.image.shape[2]-1)
        
        self.plotOnCanvasNormal(imageAxes)
        
        self.ImageDownLabel.setText(" ")
        self.savedImaLabel.setText(" ")
        # self.ax.imshow(imageAxes)
        # self.imageLayoud.addWidget(plt.plot(self.ax.imshow(imageAxes)))
        # img = Image.fromarray(imageAxes, mode="L")
        # qt_img = ImageQt.ImageQt(img)  
        # self.imageMRI.show(imageAxes)
        # self.imageMRI.set_axis_off()
  
  def showHistogram(self):
    self.plotOnCanvasH(self.normalHistogram)
  
  def showBorders(self):
    self.image = borders(self.normalImage)
    imageAxes = self.myAxesI()
    self.plotOnCanvas(imageAxes)
  
  def showImage(self):
    self.image=self.normalImage
    imageAxes = self.myAxesI()
    self.plotOnCanvas(imageAxes)
  
  def convert_numpy_to_qimage(self, image):
    """Convierte una imagen de formato numpy a QImage."""
    height, width = image.shape
    #bytes_per_line =  3*width
    qimage_format = QImage.Format_Indexed8
    #qimage_format = QImage.Format_RGB888
    # Convertimos la imagen de NumPy a una cadena de bytes
    image_bytes = image.astype(np.uint8).tobytes()

    # Creamos una QImage a partir de la cadena de bytes
    qimage = QImage(image_bytes, width, height, qimage_format)

    return qimage
      
  def axeXControl(self,event):
      self.ejeX.setValue(event)
      self.sliderY.setMinimum(-1)
      self.sliderZ.setMinimum(-1)
      #self.sliderX.setMinimum(0)
      self.sliderX.setValue(event)
      self.sliderY.setValue(-1)
      self.sliderZ.setValue(-1)
      valueX = self.ejeX.value()
      imageAxes = self.image[valueX, :, :]
      if self.normalRB.isChecked():
        self.plotOnCanvasNormal(imageAxes)
      else:
        self.plotOnCanvas(imageAxes)
      
  def axeYControl(self,event):
      self.ejeY.setValue(event)
      self.sliderX.setMinimum(-1)
      self.sliderZ.setMinimum(-1)
      #self.sliderY.setMinimum(0)
      self.sliderY.setValue(event)
      self.sliderX.setValue(-1)
      self.sliderZ.setValue(-1)
      valueY = self.ejeY.value()
      imageAxes = self.image[:, valueY, :]
      if self.normalRB.isChecked():
        self.plotOnCanvasNormal(imageAxes)
      else:
        self.plotOnCanvas(imageAxes)
    
  def axeZControl(self,event):
      self.ejeZ.setValue(event)
      self.sliderY.setMinimum(-1)
      self.sliderX.setMinimum(-1)
      #self.sliderZ.setMinimum(0)
      self.sliderZ.setValue(event)
      self.sliderY.setValue(-1)
      self.sliderX.setValue(-1)
      valueZ = self.ejeZ.value()
      imageAxes = self.image[:, :, valueZ]
      if self.normalRB.isChecked():
        self.plotOnCanvasNormal(imageAxes)
      else:
        self.plotOnCanvas(imageAxes)
  # def axesControl(self,axe):
  #   if(axe == "ejeX"):
  #     self.ejeY.setValue(-1)
  #     self.ejeZ.setValue(-1)
  #   if(axe == "ejeY"):
  #     self.ejeX.setValue(-1)
  #     self.ejeZ.setValue(-1)
  #   if(axe == "ejeZ"):
  #     self.ejeY.setValue(-1)
  #     self.ejeX.setValue(-1)
  
  def rbControls(self,rbName):
    if rbName == "normal":
      self.toleLabel.setEnabled(False)
      self.tauLabel.setEnabled(False)
      self.toleSpinB.setEnabled(False)
      self.tauSpinB.setEnabled(False)
      self.labeStartP.setEnabled(False)
      self.startPX.setEnabled(False)
      self.startPY.setEnabled(False)
      self.startPZ.setEnabled(False)
      self.xSpinB.setEnabled(False)
      self.ySpinB.setEnabled(False)
      self.zSpinB.setEnabled(False)
      self.labelIterations.setEnabled(False)
      self.iterationsSpinB.setEnabled(False)
      self.labelKs.setEnabled(False)
      self.KsSpinB.setEnabled(False)
      
    if rbName == "isodata":
      self.toleLabel.setEnabled(True)
      self.tauLabel.setEnabled(True)
      self.toleSpinB.setEnabled(True)
      self.tauSpinB.setEnabled(True)
      self.labeStartP.setEnabled(False)
      self.startPX.setEnabled(False)
      self.startPY.setEnabled(False)
      self.startPZ.setEnabled(False)
      self.xSpinB.setEnabled(False)
      self.ySpinB.setEnabled(False)
      self.zSpinB.setEnabled(False)
      self.labelIterations.setEnabled(False)
      self.iterationsSpinB.setEnabled(False)
      self.labelKs.setEnabled(False)
      self.KsSpinB.setEnabled(False)
    if rbName == "regionG":
      self.toleLabel.setEnabled(True)
      self.tauLabel.setEnabled(False)
      self.toleSpinB.setEnabled(True)
      self.tauSpinB.setEnabled(False)
      self.labeStartP.setEnabled(True)
      self.startPX.setEnabled(True)
      self.startPY.setEnabled(True)
      self.startPZ.setEnabled(True)
      self.xSpinB.setEnabled(True)
      self.ySpinB.setEnabled(True)
      self.zSpinB.setEnabled(True)
      self.labelIterations.setEnabled(False)
      self.iterationsSpinB.setEnabled(False)
      self.labelKs.setEnabled(False)
      self.KsSpinB.setEnabled(False)
    if rbName == "kMeans":
      self.toleLabel.setEnabled(False)
      self.tauLabel.setEnabled(False)
      self.toleSpinB.setEnabled(False)
      self.tauSpinB.setEnabled(False)
      self.labeStartP.setEnabled(False)
      self.startPX.setEnabled(False)
      self.startPY.setEnabled(False)
      self.startPZ.setEnabled(False)
      self.xSpinB.setEnabled(False)
      self.ySpinB.setEnabled(False)
      self.zSpinB.setEnabled(False)
      self.labelIterations.setEnabled(True)
      self.iterationsSpinB.setEnabled(True)
      self.labelKs.setEnabled(True)
      self.KsSpinB.setEnabled(True)
    if rbName == "GMM":
      self.toleLabel.setEnabled(False)
      self.tauLabel.setEnabled(False)
      self.toleSpinB.setEnabled(False)
      self.tauSpinB.setEnabled(False)
      self.labeStartP.setEnabled(False)
      self.startPX.setEnabled(False)
      self.startPY.setEnabled(False)
      self.startPZ.setEnabled(False)
      self.xSpinB.setEnabled(False)
      self.ySpinB.setEnabled(False)
      self.zSpinB.setEnabled(False)
      self.labelIterations.setEnabled(True)
      self.iterationsSpinB.setEnabled(True)
      self.labelKs.setEnabled(True)
      self.KsSpinB.setEnabled(True)
  
  def standarizationControls (self,rbName):
    if rbName == "histo":
      self.histogramSpinB.setEnabled(True)
      self.HisComboBox.setEnabled(True)
    else:
      self.histogramSpinB.setEnabled(False)
      self.HisComboBox.setEnabled(False)
    
  def controlBoton(self):  
    self.inputLDireccionI_2.setEnabled(False)
    self.searchButton_2.setEnabled(False)
    self.registerButton.setEnabled(False)
              
    if self.normalRB.isChecked():
      self.image = self.normalImage
      myIAxes =self.myAxesI()      
      self.plotOnCanvasNormal(myIAxes)         
    if self.isodataRB.isChecked():
      valueTolerance = self.toleSpinB.value()
      valueTau = self.tauSpinB.value()
      self.image = self.normalImage >= isodata(self.normalImage,valueTolerance,valueTau)      
      myIAxes =self.myAxesI()
      self.plotOnCanvas(myIAxes)
    if self.kmeansRB.isChecked():
      iterations = self.iterationsSpinB.value()
      ks = self.KsSpinB.value()
      self.image = kMeans(self.normalImage,iterations,ks)      
      myIAxes =self.myAxesI()
      self.plotOnCanvas(myIAxes)
    if self.gmmRB.isChecked():
      iterations = self.iterationsSpinB.value()
      ks = self.KsSpinB.value()
      self.image = gmm(self.normalImage,ks,iterations)      
      myIAxes =self.myAxesI()
      self.plotOnCanvas(myIAxes)
    if self.regionRB.isChecked():
      tolerance = self.toleSpinB.value()
      x = self.xSpinB.value()
      y = self.ySpinB.value()
      z = self.zSpinB.value()
      self.image = regionGrowing(self.normalImage,x,y,z,tolerance)      
      myIAxes =self.myAxesI()
      self.plotOnCanvas(myIAxes)
    self.ImageDownLabel.setText(" ")
    self.savedImaLabel.setText(" ")

  def myAxesI(self):
    valueX = self.ejeX.value()
    valueY = self.ejeY.value()
    valueZ = self.ejeZ.value()
    imageAxes = None
    if(valueX>=0):
        imageAxes = self.image[valueX, :, :]
    elif(valueY>=0):
        imageAxes = self.image[:, valueY, :]
    elif(valueZ>=0):
        imageAxes = self.image[:, :, valueZ]
    return imageAxes
   
if __name__=='__main__':
  app=QApplication(sys.argv)
  GUI = MiEjemplo()
  GUI.show()
  sys.exit(app.exec_())



