#Gui
#Gui
import sys
import os
import numpy as np
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#Funciones del programa
from thresholding import isodata, regionGrowing, kMeans, borders
from preProcesing import Rescaling, ZScore, WhiteStripe, histogramMatching
from denoising import meanFilter,medianFilter,medianFilterBorders

#Procesamiento de las imagenes
import nibabel as nib
import matplotlib.pyplot as plt

class MiEjemplo(QMainWindow):
  def __init__(self):
      super(MiEjemplo,self).__init__()
      loadUi("PruebasGUI.ui", self)
      #Haciendo cosas de layouds
      self.horizontalL=QtWidgets.QHBoxLayout(self.frame)
      self.horizontalL.setObjectName("HorizontalL")
      #Fin
      #Agrego un canvas
      self.figure=plt.figure()
      self.canvas = FigureCanvas(self.figure)
      self.horizontalL.addWidget(self.canvas)
      #Fin
      self.uploadButton.clicked.connect(self.uploadImage)
      self.showHisButton.clicked.connect(self.showHistogram)
      self.showBordersButton.clicked.connect(self.showBorders)
      self.showImageButton.clicked.connect(self.showImage)
      self.miPrimerBoton.clicked.connect(self.controlBoton)
      
      self.sliderX.valueChanged.connect(self.axeXControl)
      self.sliderY.valueChanged.connect(self.axeYControl)
      self.sliderZ.valueChanged.connect(self.axeZControl)
      
      self.ejeX.valueChanged.connect(self.axeXControl)
      self.ejeY.valueChanged.connect(self.axeYControl)
      self.ejeZ.valueChanged.connect(self.axeZControl)

      self.normalRB.toggled.connect(lambda: self.rbControls("normal"))  
      self.isodataRB.toggled.connect(lambda: self.rbControls("isodata"))
      self.regionRB.toggled.connect(lambda: self.rbControls("regionG"))
      self.kmeansRB.toggled.connect(lambda: self.rbControls("kMeans"))
        
  image=None
  normalImage=None
  histogram = None
  normalHistogram = None
  
  def plotOnCanvas (self,imageAxes):
    self.figure.clear()
    plt.imshow(imageAxes)
    self.canvas.draw()
    
  def plotOnCanvasH (self,histogram):
    self.figure.clear()
    plt.hist(histogram,100)
    self.canvas.draw()
  
  def uploadImage(self):
    if (os.path.exists("./Images/"+self.inputLDireccionI.text()+".gz")):
        imageUploaded = nib.load("./Images/"+self.inputLDireccionI.text()+".gz").get_fdata()
        if (self.inputLDireccionI.text() == "FLAIR.nii"):
          targ = 1
        elif (self.inputLDireccionI.text() == "IR.nii"):
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
          imageStandarised, histogram= histogramMatching(imageUploaded, targ)
        
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
        
        self.plotOnCanvas(imageAxes)
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
  
  def controlBoton(self):  
              
    if self.normalRB.isChecked():
      self.image = self.normalImage
      myIAxes =self.myAxesI()      
      self.plotOnCanvas(myIAxes)         
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
    if self.regionRB.isChecked():
      tolerance = self.toleSpinB.value()
      x = self.xSpinB.value()
      y = self.ySpinB.value()
      z = self.zSpinB.value()
      self.image = regionGrowing(self.normalImage,x,y,z,tolerance)      
      myIAxes =self.myAxesI()
      self.plotOnCanvas(myIAxes)

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



