#Gui
#Gui
import sys
import os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication
from thresholding import isodata, regionGrowing

#Procesamiento de las imagenes
import nibabel as nib
import matplotlib.pyplot as plt

class MiEjemplo(QMainWindow):
  def __init__(self):
      super(MiEjemplo,self).__init__()
      loadUi("PruebasGUI.ui", self)
      self.miPrimerBoton.clicked.connect(self.controlBoton)
      self.ejeX.valueChanged.connect(lambda: self.axesControl("ejeX"))
      self.ejeY.valueChanged.connect(lambda: self.axesControl("ejeY"))
      self.ejeZ.valueChanged.connect(lambda: self.axesControl("ejeZ"))
      self.normalRB.toggled.connect(lambda: self.rbControls("normal"))  
      self.isodataRB.toggled.connect(lambda: self.rbControls("isodata"))  
  
  def axesControl(self,axe):
    if(axe == "ejeX"):
      self.ejeY.setValue(-1)
      self.ejeZ.setValue(-1)
    if(axe == "ejeY"):
      self.ejeX.setValue(-1)
      self.ejeZ.setValue(-1)
    if(axe == "ejeZ"):
      self.ejeY.setValue(-1)
      self.ejeX.setValue(-1)
  
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
  
  def controlBoton(self):
      if (os.path.exists(self.inputLDireccionI.text()+".gz")):
        imageData = nib.load(self.inputLDireccionI.text()+".gz").get_fdata()
        valueX = self.ejeX.value()
        valueY = self.ejeY.value()
        valueZ = self.ejeZ.value()
        if(valueX>=0):
            imageAxes = imageData[valueX, :, :]
        elif(valueY>=0):
            imageAxes = imageData[:, valueY, :]
        elif(valueZ>=0):
            imageAxes = imageData[:, :, valueZ]    
              
        if self.normalRB.isChecked():      
          plt.imshow(imageAxes)
          plt.show()
          
        if self.isodataRB.isChecked():
          valueTolerance = self.toleSpinB.value()
          valueTau = self.tauSpinB.value()
          segmentated = imageAxes >= isodata(imageAxes,valueTolerance,valueTau)
          # if(valueX>=0):
          #   imageAxes = segmentated[valueX, :, :]
          # elif(valueY>=0):
          #   imageAxes = segmentated[:, valueY, :]
          # elif(valueZ>=0):
          #   imageAxes = segmentated[:, :, valueZ]        
          plt.imshow(segmentated)
          plt.show()
          
      else:
        None
   
if __name__=='__main__':
  app=QApplication(sys.argv)
  GUI = MiEjemplo()
  GUI.show()
  sys.exit(app.exec_())


