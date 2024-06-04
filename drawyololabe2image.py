import os 
from glob import glob
import cv2
from tqdm import tqdm


def drawfn(labelpath,imorg):
    orgh,orgw,_ = imorg.shape
    # print(imorg.shape)
    # print(labelpath)
    if labelpath == None:
        return imorg
    x,y,h,w = 0,0,0,0
    with open(labelpath,"r") as f:
        label = f.read()
        # print("label",label)
        label = label.split("\n")
        # print("labelsplit",label)
        for i in range(len(label)):
            if label[i] != "":
                clsname,x,y,w,h = label[i].split()
                n = names[int(clsname)]
                x,y,w,h = float(x)*orgw,float(y)*orgh,float(w)*orgw,float(h)*orgh
                x0,y0 = int(x-w//2),int(y-h//2)
                x1,y1 = int(x+w//2),int(y+h//2)
                cv2.rectangle(imorg,(x0, y0), (x1,y1), (255, 0, 0),2);
                cv2.putText(imorg,n,(x0,y0),fontFace = cv2.FONT_HERSHEY_SIMPLEX,\
                    fontScale = 1,color= (0,111,0),thickness = 2)
        
        f.close()
        return imorg


import sys 
root = sys.argv[1]
# root = "/media/wpy/558e3a8b-7a8f-4603-a6fb-20c87dbd584b/StainDetection/finish0424_histogram/val"
names  = ["stain"]
imagepath = f"{root}/images"
labelpath = f"{root}/labels"

images = sorted(list(glob(f"{imagepath}/*")),key = lambda x:os.path.basename(x).rsplit(".",1)[0])
labels = sorted(list(glob(f"{labelpath}/*")),key = lambda x:os.path.basename(x).rsplit(".",1)[0])

outfile = f"{root}/drawedimage"
os.makedirs(outfile,exist_ok= True)
imagesname = [os.path.basename(i).rsplit(".",1)[0] for i in images]
labelsname = {}
for i in labels:
    labelsname[os.path.basename(i).rsplit(".",1)[0]] = i 


labels = []
for i in imagesname:
    if i in labelsname:
        labels.append(labelsname[i])
    else:
        labels.append(None)
# print(imagesname)
# labels = [i if os.path.basename(i).rsplit(".",1)[0] in imagesname else None for i in labels]

print(len(images),len(labels))
# os.makedirs(outfile,exist_ok= True)

for img,lab in tqdm(zip(images,labels)):
    imgs = cv2.imread(img)
    drawedImg = drawfn(lab,imgs)
    
    cv2.imwrite(f"{outfile}/{os.path.basename(img)}",drawedImg)



                            
                            
            
            