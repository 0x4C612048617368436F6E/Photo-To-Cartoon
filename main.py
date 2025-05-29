import cv2
from matplotlib import pyplot as plt

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys

class GUI(QWidget):
    def __init__(self, parent=None):
        super(GUI,self).__init__(parent)
        self.resize(1000,1000)
        self.setWindowTitle("Photo To Cartoon")
        #create a grid layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        label = QLabel("Welcome to the Photo to cartoon Application")

        #self.label.setText()
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        label.setFont(font)

        self.layout.addWidget(label,0,0)
        #self.label.move(50,20)
        #create push button
        button = QPushButton("Select Image")
        #create the signal&slot
        button.clicked.connect(self.handleClickEvent)

        self.layout.addWidget(button,2,0,2,2)

    @staticmethod
    def convertFromMatToQTImage(image:cv2.Mat):
        #in order to represent an image stored as a MAT
        #within QT, need to convert from MAT to QTImage
        

        #step 1 is to check the whether we have a grayscale or RGB image (Obviously RGB)
        if(len(image.shape) == 2):
            #will be grayscale
            height,width = image.shape
            bytes_per_line = width
            qImage = QImage(image.data,width,height,bytes_per_line,QImage.Format_Grayscale8)
            return qImage
        if (len(image.shape) == 3):
            height, width, channels = image.shape
            bytes_per_line = channels*width
            qImage = QImage(image.data,width,height,bytes_per_line,QImage.Format_RGB888)
            return qImage
        
        if (len(image.shape) < 2 or len(image.shape) > 3):
            raise ValueError("Unsupported Image Format")

    def handleClickEvent(self):
        #create slots and signals
        #open file explorer
        fileDialog = QFileDialog(self)
        fileDialog.setDirectory(r'C:/')
        fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        fileDialog.setNameFilter("Images (*.png *.jpg)")
        fileDialog.setViewMode(QFileDialog.ViewMode.List)
        if fileDialog.exec():
            #store just the file path
            fileName = fileDialog.selectedFiles() #stores files in a list
            #call our collect data here in the file 
            print(fileName[0])
    
            #How to load an image represented as Mat 
            #in QT
            #create label for original image
            self.labelOriginal = QLabel(self)
            #create label for cartoon image
            self.label = QLabel(self)
            #load image/convert QImage to QPixmap
            Image = collectData(fileName[0],Testing=False)
            print(type(Image))
            self.pixmap = QPixmap(GUI.convertFromMatToQTImage(collectData(fileName[0],Testing=False)))
            #setting original image
            image = cv2.imread(fileName[0])
            Convertimage = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            self.labelOriginal.setPixmap(QPixmap(GUI.convertFromMatToQTImage(Convertimage)))

            #increase width and heght of label


            #seems like previous image still in memory
            #delete from memory before proceding with 
            #next image
            self.label.setPixmap(self.pixmap)

            self.layout.addWidget(self.label,1,1)
            self.layout.addWidget(self.labelOriginal,1,0)

def edgeDetection(image):
    #convert image to grayscale
    grayScale = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    #mediumBlur
    medianBlur = cv2.medianBlur(grayScale,5)

    th2 = cv2.adaptiveThreshold(medianBlur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    th3 = cv2.adaptiveThreshold(medianBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    return th3

def visualizePlot(image,row,column,index,label):
    plt.subplot(row,column,index)
    plt.imshow(image)
    plt.title(label)

'''def edgeDetection(image):
    #convet image to grayscale
    grayScale = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(image,30,40)#100,150)#178
    #invert edges (pixels)
    invertedges = cv2.bitwise_not(edges)
    convertBack = cv2.cvtColor(invertedges,cv2.COLOR_GRAY2BGR)
    #plot the edges
    #plt.subplot(122)#row column index
    #plt.imshow(invertedges,cmap="gray")
    #plt.title("Edges")
    return convertBack'''

def plotEdgeDetection(image,Testing):
    if Testing:
        visualizePlot(image,1,2,1,"Original")
        imageFiltering(image,Testing)
        plt.show()
    else:
        return imageFiltering(image,Testing)

def colorQuantization():
    #make use of the K-Means clustering algorithm
    pass

def imageFiltering(orginalImage,Testing=True):
    #propagate the edges throughh this section
    bilaterialFilter = cv2.bilateralFilter(orginalImage,25,100,100)
    invert = edgeDetection(orginalImage)
    print(invert.shape[0],invert.shape[1])
    print(invert.dtype)
    convertInvert = cv2.cvtColor(invert,cv2.COLOR_BGR2RGB)
    cartoon = cv2.bitwise_and(bilaterialFilter,convertInvert,mask=None)
    #image,row,column,index,label
    if Testing:
        visualizePlot(cartoon,1,2,2,"cartoon")
    else:
        print(f"Type of cartoon is {type(cartoon)}")
        return cartoon

def collectData(imagePath:str,Testing=True):
    #in our case, data will be (We will integreate QT5 For UI)

    #Only make use of MatPlotLib if Testing is True
    image = cv2.imread(imagePath)
    Convertimage = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    if Testing:
        plotEdgeDetection(Convertimage,Testing)
    else:
        return plotEdgeDetection(Convertimage,Testing)

def main():
    app = QApplication(sys.argv)
    ex = GUI()
    ex.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
#
#collectData("C:/Users/benja/Desktop/cartoonify/dataset/diverseImages/train2014/train2014/davido.jpg")
#collectData("C:/Users/benja/Desktop/cartoonify/dataset/diverseImages/train2014/train2014/2600978dacd7c09f2caefd9e061d2999.1000x1000x1.jpg")

#collectData("C:/Users/benja/Desktop/cartoonify/dataset/diverseImages/train2014/train2014/COCO_train2014_000000005883.jpg")
#collectData("C:/Users/benja/Desktop/cartoonify/dataset/faces/1Gge9Pz7-AQ2JKh2IMrsxbQGnjgs8kh2h.png")          
#collectData("C:/Users/benja/Desktop/cartoonify/dataset/diverseImages/train2014/train2014/COCO_train2014_000000005505.jpg")

#"C:/Users/benja/Desktop/cartoonify/dataset/diverseImages/train2014/train2014/COCO_train2014_000000008979.jpg
         #COCO_train2014_000000008979   
#"COCO_train2014_000000001238.jpg")

#"COCO_train2014_000000000036.jpg")