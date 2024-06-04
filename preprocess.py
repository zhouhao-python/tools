import cv2
import numpy as np 
from glob import glob 
import os
import tqdm

class HandleImage:
    def __init__(self,root,brightalpha,brightbeta):
        self.root = root
        self.imagepaths = sorted(list(glob(f"{root}{os.sep}*jpg")))
        self.imagebasename = [os.path.basename(i) for i in self.imagepaths]
        self.brightalpha = brightalpha;
        self.brightbeta  = brightbeta;
        
    @staticmethod
    def equalizedOneImage(image):
        '''直方图均值化

        Args:
            image (_type_): _description_

        Returns:
            _type_: _description_
        '''
        if len(image.shape)== 3 or image.shape[-1] == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image
        equalizedImage = cv2.equalizeHist(gray_image)
        return equalizedImage
    
    @staticmethod
    def equalizedOneImageHalf(image):
        '''
        直方图均值化下半部分图像
        Args:
            image (_type_): _description_

        Returns:
            _type_: _description_
        '''
        if len(image.shape)== 3 or image.shape[-1] == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image
        h, w = gray_image.shape
        gray_imagedown = gray_image[h//3*1:,...]
        gray_imageup = gray_image[:h//3*1,...]
        equalizedImage = cv2.equalizeHist(gray_imagedown)
        
        return np.concatenate((gray_imageup,equalizedImage),axis=0)
    

    def handleimages(self,equalized = True,laplacianed = True,alpha = 0.5,isconcatenate = True,changebright = False):
        if equalized:
            equalizedoutput = self.root+"equalized"
            self.equalizedoutput = equalizedoutput
            os.makedirs(equalizedoutput,exist_ok= True)
        if laplacianed:
            laplacianedoutput = self.root+"laplacianed"
            self.laplacianedoutput = laplacianedoutput
            os.makedirs(laplacianedoutput,exist_ok= True)
        if changebright:
            changebrightoutput = self.root+"bright"
            self.changebrightoutput = changebrightoutput
            os.makedirs(changebrightoutput,exist_ok= True)
        for idx,path in tqdm.tqdm(enumerate(self.imagepaths)):
            img = cv2.imread(path)
            if changebright:
                changebrightimage = cv2.addWeighted(img,self.brightalpha,img,0,self.brightbeta)
                # changebrightimage = self.changeBright(img)
                changebrightimage = self.concatenate2image(img,changebrightimage)
                # cv2.imwrite(os.path.join(changebrightoutput,os.path.basename(path)),changebrightimage)
            if equalized:
                equalizedImage = self.equalizedOneImageHalf(img)
                equalizedImage = cv2.addWeighted(img, 1 - alpha, cv2.cvtColor(equalizedImage, cv2.COLOR_GRAY2BGR), alpha, 0)
                cv2.imwrite(os.path.join(equalizedoutput,os.path.basename(path)),equalizedImage)
                resultImage = equalizedImage
            if equalized and laplacianed:
                laplacianedimage = self.laplacianedImage(equalizedImage)
                laplacianedimage = cv2.addWeighted(img, 1 - alpha, cv2.cvtColor(laplacianedimage, cv2.COLOR_GRAY2BGR), alpha, 0)
                resultImage = laplacianedimage
            if (equalized or laplacianed) and isconcatenate:
                concatenatedimage = self.concatenate2image(img,resultImage)
                self.concatenateoutput = self.root+"concatenate"
                os.makedirs(self.concatenateoutput,exist_ok= True)
                cv2.imwrite(os.path.join(self.concatenateoutput,os.path.basename(path)),concatenatedimage)

    def changeBright(self,img):
        import cv2
        import numpy as np

        height, width, _ = img.shape

        mesh = np.meshgrid(np.linspace(0, width, 4, dtype=np.int64), np.linspace(0, height, 4, dtype=np.int64))
        xx,yy = map(lambda x:x.astype(np.int64),mesh)
        result = np.zeros((height, width, 3), dtype=np.uint8)
        
        for idx in range(9):
            x = idx//3
            y = idx%3
            cell_img = img[yy[x][y]:yy[x+1][y+1], xx[x][y]:xx[x+1][y+1],:]
            if idx == 6 or idx == 8:
                print(yy[x][y],yy[x+1][y+1], xx[x][y],xx[x+1][y+1])
                # cell_img = cv2.addWeighted(cell_img,self.brightalpha,cell_img,0,self.brightbeta)
                if True:
                    alpha = 0.3
                    cell_img_TMP = cv2.cvtColor(cell_img,cv2.COLOR_BGR2GRAY)
                    cell_img_TMP = self.equalizedOneImage(cell_img_TMP)
                    cell_img = cv2.addWeighted(cell_img, 1 - alpha, cv2.cvtColor(cell_img_TMP, cv2.COLOR_GRAY2BGR), alpha, 0)
            result[yy[x][y]:yy[x+1][y+1], xx[x][y]:xx[x+1][y+1],:] = cell_img  

        return result
    @staticmethod
    def laplacianedImage(image):
        ''' 拉普拉斯边缘增强

        Args:
            image (_type_): _description_

        Returns:
            _type_: _description_
        '''
        if len(image.shape)== 3 or image.shape[-1] == 3:
            
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
        return cv2.convertScaleAbs(laplacian)
        
    @staticmethod
    def concatenate2image(image1,image2):
        assert image1.shape == image2.shape, "image1.shape must == image2.shape!!!"
        return np.concatenate((image1,image2),axis=1)
    

import sys


if len(sys.argv)<1:
    print("python preprocess.py [path]")
    exit()
root = sys.argv[1]
handleimage = HandleImage(root,brightbeta=50,brightalpha=1.0)
handleimage.handleimages(equalized = True,laplacianed = False,alpha = 0.3,isconcatenate = True,changebright = True)