import sys
from PySide.QtGui import *
from HomographyGUI import *
from Homography import *
from PIL import Image

class HomographyAPP(QMainWindow, Ui_homography):

    def __init__(self, parent=None):
        super(HomographyAPP, self).__init__(parent)
        self.setupUi(self)

        self.pt_list=[self.pt1, self.pt2, self.pt3, self.pt4]
        self.InitialState()

        self.SourcePath=""
        self.TargetPath=""
        self.state=""
        self.check=0
        self.pt_click=[]

        self.LoadSource.clicked.connect(self.SourceLoad)
        self.LoadTarget.clicked.connect(self.TargetLoad)
        self.AcquirePoints.clicked.connect(self.PointAc)
        self.Save.clicked.connect(self.SavePic)
        self.Transform.clicked.connect(self.TransformPic)
        self.Reset.clicked.connect(self.ResetEverything)

    def InitialState(self):
        self.SourceImage.setDisabled(True)
        self.TargetImage.setDisabled(True)
        self.AcquirePoints.setDisabled(True)
        for pt in self.pt_list:
            pt.setDisabled(True)
        self.label.setDisabled(True)
        self.Effect.setDisabled(True)
        self.Transform.setDisabled(True)
        self.Reset.setDisabled(True)
        self.Save.setDisabled(True)

    def ReadyState(self):
        self.SourceImage.setDisabled(False)
        self.TargetImage.setDisabled(False)
        self.AcquirePoints.setDisabled(False)

        for pt in self.pt_list:
            pt.setDisabled(False)
        self.label.setDisabled(False)
        self.Effect.setDisabled(False)
        self.Transform.setDisabled(False)
        self.Reset.setDisabled(False)
        self.Save.setDisabled(False)

    def TransformedState(self):
        self.InitialState()
        self.pt1.clear()
        self.pt2.clear()
        self.pt3.clear()
        self.pt4.clear()
        del self.pt_click[:]

    def SourceLoad(self):
        self.SourcePath, _ = QFileDialog.getOpenFileName(self, caption='Open png file ...', filter="png files (*.png)")
        self.SourceScene = QGraphicsScene(self)
        self.SourceScene.addPixmap(QPixmap(self.SourcePath))
        self.SourceImage.setScene(self.SourceScene)
        self.SourceImage.fitInView(self.SourceScene.sceneRect())

        self.SourceImg = Image.open(self.SourcePath)
        if self.state=="Transform":
            self.TransformedState()
        if self.SourcePath != "" and self.TargetPath != "":
            self.AcquirePoints.setDisabled(False)
            self.label.setDisabled(False)

    def TargetLoad(self):
        self.TargetPath, _ = QFileDialog.getOpenFileName(self, caption='Open png file ...', filter="png files (*.png)")
        self.TargetScene = QGraphicsScene(self)
        self.TargetScene.addPixmap(QPixmap(self.TargetPath))
        self.TargetImage.setScene(self.TargetScene)
        self.TargetImage.fitInView(self.TargetScene.sceneRect())
        self.TargetImg = Image.open(self.TargetPath)
        self.TargetArray = np.array(self.TargetImg)

        self.TransformedState()
        if self.SourcePath != "" and self.TargetPath != "":
            self.AcquirePoints.setDisabled(False)




    def PointAc(self):
        self.label.setDisabled(False)
        self.LoadSource.setDisabled(True)
        self.LoadTarget.setDisabled(True)
        self.SourceImage.setDisabled(False)
        self.TargetImage.setDisabled(False)
        for pt in self.pt_list:
            pt.setDisabled(False)

        self.TargetScene.mouseReleaseEvent=self.mouseReleaseEvent
        self.TargetScene.keyPressEvent=self.keyPressEvent

        if self.check==0:
            self.AcquirePoints.setCheckable(True)
            self.AcquirePoints.toggle()
            self.check=1
        else:
            self.AcquirePoints.setCheckable(False)
            self.check=0

            self.LoadSource.setDisabled(False)
            self.LoadTarget.setDisabled(False)

            if len(self.pt_click) != 4:

                self.pt1.clear()
                self.pt2.clear()
                self.pt3.clear()
                self.pt4.clear()
                del self.pt_click[:]
                self.label.setDisabled(False)
                for pt in self.pt_list:
                    pt.setDisabled(False)
                self.AcquirePoints.setDisabled(False)
            else:
                self.ReadyState()


    def mouseReleaseEvent(self, QMouseEvent):
        try:
            x = round(QMouseEvent.scenePos().x(), 1)
            y = round(QMouseEvent.scenePos().y(), 1)
            pt=(x,y)
            self.pt_click.append(pt)
            if len(self.pt_click) == 1:
                self.pt1.setText(str(x)+", "+str(y))
            if len(self.pt_click) == 2:
                self.pt2.setText(str(x)+", "+str(y))
            if len(self.pt_click) == 3:
                self.pt3.setText(str(x)+", "+str(y))
            if len(self.pt_click) == 4:
                self.pt4.setText(str(x)+", "+str(y))
            if  len(self.pt_click) > 4:
                del self.pt_click[-1]
        except:
            pass




    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Backspace:
            try:
                if len(self.pt_click) == 1:
                    self.pt1.clear()
                if len(self.pt_click) == 2:
                    self.pt2.clear()
                if len(self.pt_click) == 3:
                    self.pt3.clear()
                if len(self.pt_click) == 4:
                    self.pt4.clear()
                del self.pt_click[-1]
            except:
                pass

    def SavePic(self):
        filepath,_ = QFileDialog.getSaveFileName(self, caption = 'Save png file ...', filter = 'png files (*.png)')
        img = Image.fromarray(self.TargetArray)
        img.save(filepath + '.png')

    def TransformPic(self):
        self.state="Transform"
        self.AcquirePoints.setDisabled(True)
        for pt in self.pt_list:
            pt.setDisabled(True)

        effect=None
        print(self.Effect.currentText())
        if  self.Effect.currentIndex() == 0:
            print("pass nothing")
            effect = None
        if self.Effect.currentIndex() == 1:
            print("pass 90")
            effect = Effect.rotate90
        if self.Effect.currentIndex() == 2:
            print("pass 180")
            effect = Effect.rotate180
        if self.Effect.currentIndex() == 3:
            print("pass 270")
            effect = Effect.rotate270
        if self.Effect.currentText() == 'Flip Horizontally':
            print("flip H")
            effect = Effect.flipHorizontally
        if self.Effect.currentText() == 'Flip Vertically':
            print("Flip V")
            effect = Effect.flipVertically
        if self.Effect.currentText() == 'Transpose':
            print("Transpose")
            effect = Effect.transpose
        print(effect)
        self.SourceArray = np.array(self.SourceImg)
        self.TargetArray = np.array(self.TargetImg)
        print(self.TargetArray.shape)

        if len(self.SourceArray.shape) == 2:
            transformer = Transformation(self.SourceArray, None)
            transformer.setupTransformation(np.array(self.pt_click), effect)
            self.TargetArray = transformer.transformImageOnto(self.TargetArray)
        elif len(self.SourceArray.shape) == 3:
            transformer = ColorTransformation(self.SourceArray, None)
            transformer.setupTransformation(np.array(self.pt_click), effect)
            self.TargetArray = transformer.transformImageOnto(self.TargetArray)

        img = Image.fromarray(self.TargetArray)
        img.save("output.png")
        self.TargetScene = QGraphicsScene(self)
        self.TargetScene.addPixmap(QPixmap('output.png'))
        self.TargetImage.setScene(self.TargetScene)
        self.TargetImage.fitInView(self.TargetScene.sceneRect())

    def ResetEverything(self):
        self.AcquirePoints.setDisabled(False)
        for pt in self.pt_list:
            pt.setDisabled(False)
        self.TargetScene = QGraphicsScene(self)
        self.TargetScene.addPixmap(QPixmap(self.TargetPath))
        self.TargetImage.setScene(self.TargetScene)
        self.TargetImage.fitInView(self.TargetScene.sceneRect())


if __name__ == "__main__":
 currentApp = QApplication(sys.argv)
 currentForm = HomographyAPP()

 currentForm.show()
 currentApp.exec_()