import numpy as np
from enum import Enum
from scipy.interpolate import RectBivariateSpline

class Effect(Enum):

    rotate90 = 'rotate90'
    rotate180 = 'rotate180'
    rotate270 = 'rotate270'
    flipHorizontally = 'flipHorizontally'
    flipVertically = 'flipVertically'
    transpose = 'transpose'

class Homography:
    def __init__(self, **kwargs):
        if "homographyMatrix" in kwargs.keys():
            if kwargs["homographyMatrix"].shape != (3,3):
                raise ValueError("HomographyMatrix has wrong dimension.")
            elif kwargs["homographyMatrix"].dtype != "float64":
                raise ValueError("HomographyMatrix has wrong datatype.")
            self.forwardMatrix = kwargs["homographyMatrix"]
            self.inverseMatrix = np.linalg.inv(kwargs["homographyMatrix"])
        else:
            if "sourcePoints" in kwargs.keys() and "targetPoints" in kwargs.keys() or "effect" in kwargs.keys():
                if kwargs["sourcePoints"].shape != (4,2) and kwargs["targetPoints"].shape != (4,2):
                    raise ValueError("SourcePoints or targetPoints has wrong dimension.")
                elif kwargs["sourcePoints"].dtype != "float64" or kwargs["targetPoints"].dtype != "float64":
                    raise ValueError("SourcePoints or targetPoints has wrong type.")
            else:
                raise ValueError("Missing inputs.")
            if "effect" in kwargs.keys():
                if kwargs["effect"] != None and not isinstance(kwargs["effect"], Effect):#kwargs["effect"] not in Effect.__members__:
                        raise TypeError("Effect is out of range.")
                self.computeHomography(kwargs["sourcePoints"],  kwargs["targetPoints"], kwargs["effect"])
            else:
                self.computeHomography(kwargs["sourcePoints"],  kwargs["targetPoints"])


    def computeHomography(self, sourcePoints, tagetPoints, effect = None):
        b_temp=tagetPoints
        A_temp=sourcePoints
        if effect == Effect.rotate90:
            A_temp=np.array([sourcePoints[2],sourcePoints[0],sourcePoints[3],sourcePoints[1]])
        if effect == Effect.rotate180:
            A_temp=np.array([sourcePoints[3],sourcePoints[2],sourcePoints[1],sourcePoints[0]])
        if effect == Effect.rotate270:
            A_temp=np.array([sourcePoints[1],sourcePoints[3],sourcePoints[0],sourcePoints[2]])
        if effect == Effect.flipHorizontally:
            A_temp=np.array([sourcePoints[2],sourcePoints[3],sourcePoints[0],sourcePoints[1]])
        if effect == Effect.flipVertically:
            A_temp=np.array([sourcePoints[1],sourcePoints[0],sourcePoints[3],sourcePoints[2]])
        if effect == Effect.transpose:
            A_temp=np.array([sourcePoints[0],sourcePoints[2],sourcePoints[1],sourcePoints[3]])


        ind=0
        A=[]
        b=[]
        while ind < len(sourcePoints):
            A.append(np.append([A_temp[ind][0],A_temp[ind][1],1,0,0,0, (-1)*b_temp[ind][0]*A_temp[ind][0],(-1)*b_temp[ind][0]*A_temp[ind][1]],
                    [0,0,0,A_temp[ind][0],A_temp[ind][1],1,(-1)*b_temp[ind][1]*A_temp[ind][0],(-1)*b_temp[ind][1]*A_temp[ind][1]]))
            b.append(b_temp[ind][0])
            b.append(b_temp[ind][1])
            ind +=1
        A_arr=np.array(A).reshape(8,8)
        b_arr=np.array(b).reshape(8,1)
        forwardMatrix_temp=np.linalg.solve(A_arr, b_arr)
        self.forwardMatrix=np.append(forwardMatrix_temp,1.0).reshape(3,3)
        self.inverseMatrix=np.linalg.inv(self.forwardMatrix)

class Transformation:
    def __init__(self, sourceImage, homography=None):
        self.homography= None
        if homography != None:
            if not isinstance(homography, Homography) or not isinstance(sourceImage, np.ndarray):
                raise TypeError("Wrong data type for homography or sourceImage")
            self.homography = homography
        else:
            if not isinstance(sourceImage, np.ndarray):
                raise TypeError("Wrong data type for sourceImage")

        self.sourceImage = sourceImage


    def setupTransformation(self, targetPoints, effect=None):
        self.source_shape=self.sourceImage.shape #?????? need change

        sourcePoints=np.array([[0.,0.],[0.,self.source_shape[1]-1],[self.source_shape[0]-1,0],[self.source_shape[0]-1, self.source_shape[1]-1]])
        self.targetPoints=targetPoints
        #if self.homography == None:

        getHomo=Homography(sourcePoints=sourcePoints,targetPoints=targetPoints,effect=effect)
        self.homography=getHomo.forwardMatrix

    def transformImageOnto(self, containerImage):
        if not isinstance(containerImage,np.ndarray):
            raise TypeError("Wrong data type for containerImage")

        Homo_inv=Homography(homographyMatrix=self.homography).inverseMatrix

        x_min=min(self.targetPoints[0][0],self.targetPoints[1][0],self.targetPoints[2][0],self.targetPoints[3][0])
        x_max=max(self.targetPoints[0][0],self.targetPoints[1][0],self.targetPoints[2][0],self.targetPoints[3][0])
        y_min=min(self.targetPoints[0][1],self.targetPoints[1][1],self.targetPoints[2][1],self.targetPoints[3][1])
        y_max=max(self.targetPoints[0][1],self.targetPoints[1][1],self.targetPoints[2][1],self.targetPoints[3][1])

        x_axis=np.arange(0,self.sourceImage.shape[1])
        y_axis=np.arange(0,self.sourceImage.shape[0])

        obj=RectBivariateSpline(y_axis, x_axis,self.sourceImage, kx=1, ky=1) #spling the x axis and y-axis

        for ver in np.arange(y_min,y_max+1):
            for hor in np.arange(x_min,x_max+1):

                cor=np.array([[hor],[ver],[1]])
                cor_inv=np.dot(Homo_inv,cor)
                pt = np.array([[cor_inv[0]/cor_inv[2]],[cor_inv[1]/cor_inv[2]],[cor_inv[2]/cor_inv[2]]])#get (x,y)
                pt = np.round(pt, 3)

                if pt[0]>=0 and pt[0] <= self.source_shape[0] - 1 and pt[1]>=0 and pt[1] <= self.source_shape[1] - 1 :#check whether in the range
                    pixel=obj.ev(pt[0], pt[1],dx=0,dy=0)

                    containerImage[ver][hor] = pixel.round().astype(np.uint8)


        return containerImage


class ColorTransformation(Transformation):
    def __init__(self, sourceImage, homography=None):
        Transformation.__init__(self, sourceImage, homography)
        if len(sourceImage.shape)!=3:
            raise ValueError("Sourceimage is not a color image.")
        elif sourceImage.shape[2]!=3:
            raise ValueError("Sourceimage is not a color image.")
        self.sourceImage = sourceImage
    def transformImageOnto(self, containerImage):
        Homo_inv=Homography(homographyMatrix=self.homography).inverseMatrix

        x_min=min(self.targetPoints[0][0],self.targetPoints[1][0],self.targetPoints[2][0],self.targetPoints[3][0])
        x_max=max(self.targetPoints[0][0],self.targetPoints[1][0],self.targetPoints[2][0],self.targetPoints[3][0])
        y_min=min(self.targetPoints[0][1],self.targetPoints[1][1],self.targetPoints[2][1],self.targetPoints[3][1])
        y_max=max(self.targetPoints[0][1],self.targetPoints[1][1],self.targetPoints[2][1],self.targetPoints[3][1])

        x_axis=np.arange(0,self.sourceImage.shape[1])
        y_axis=np.arange(0,self.sourceImage.shape[0])

        y,x,z = self.sourceImage.shape
        r=np.empty([y,x])
        b=np.empty([y,x])
        g=np.empty([y,x])

        r=self.sourceImage[:,:,0]
        b=self.sourceImage[:,:,1]
        g=self.sourceImage[:,:,2]

        obj_r=RectBivariateSpline(y_axis, x_axis,r, kx=1, ky=1)#spling the x axis and y-axis
        obj_b=RectBivariateSpline(y_axis, x_axis,b, kx=1, ky=1)
        obj_g=RectBivariateSpline(y_axis, x_axis,g, kx=1, ky=1)

        for ver in np.arange(y_min,y_max+1):
            for hor in np.arange(x_min,x_max+1):
                cor=np.array([[hor],[ver],[1]])
                cor_inv=np.dot(Homo_inv,cor)
                pt=np.array([[cor_inv[0]/cor_inv[2]],[cor_inv[1]/cor_inv[2]],[cor_inv[2]/cor_inv[2]]])#get (x,y)
                pt=np.round(pt,3)
                if pt[0]>=0 and pt[0]<=self.source_shape[0] - 1 and pt[1]>=0 and pt[1]<=self.source_shape[1]-1 :#check whether in the range

                    pixel_r=obj_r.ev(pt[0], pt[1],dx=0,dy=0)
                    pixel_b=obj_b.ev(pt[0], pt[1],dx=0,dy=0)
                    pixel_g=obj_g.ev(pt[0], pt[1],dx=0,dy=0)

                    containerImage[ver][hor][0]=pixel_r.round().astype(np.uint8)
                    containerImage[ver][hor][1]=pixel_b.round().astype(np.uint8)
                    containerImage[ver][hor][2]=pixel_g.round().astype(np.uint8)


        return containerImage

if __name__=="__main__":
    #Homography(homographyMatrix=np.array([[1.2,2,3],[1,1,1],[5,5,5]]))
   # x={"sourcePoints":np.array([[1.,2.],[1.,1.],[5.,5.], [5.,6.]]), "targetPoints":np.array([[2.,3.],[5.,1.],[4.,5.],[7.,3.]]), "effect": Effect.rotate90}
   # Homography( **x )
#    arr=np.array([[1.2,2.3],[1.5,1.1],[5.5,5.5], [5.5,5.5]])
    #print (type(arr))
#    source_image=np.random.rand(4,7)
#    targetPoints=np.random.rand(4,2)
    #print(source_image)
    #Transformation(source_image, None).setupTransformation(targetPoints, None)
#    pt=np.empty([3,3,2])
#    print(pt)
    #img = np.ones([10, 10, 3])
    #print (img)
    #print(len(img.shape))
    #targetPoints = np.array([[600, 50], [1550, 500], [50, 400], [800, 1150.0]])
    #print(targetPoints.dtype)

    #sourceImage = imread("TestImages/knight.png")
    #print(sourceImage.dtype)
    #img = np.ones([10, 10, 3], dtype=np.uint8)
    #print(type(img))
    #a = np.arange(6).reshape((3, 2))
    #print(a)
    mat = np.array([[1.2, 2.3, 4.5], [9.0, 4.4, 5.5], [0.0, 0.0, 1.0]])
    h = Homography(homographyMatrix=mat)