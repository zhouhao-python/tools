'''
处理点bottom 在360以上的数据
'''
import sys
import cv2

labelpath = sys.argv[1]
if len(sys.argv)<2:
    print("python handlelabels.py [labespath]")
# path = "/media/wpy/558e3a8b-7a8f-4603-a6fb-20c87dbd584b/StainDetection/finish0409/train/labels"

import glob
import os 


HEIGHT = 720 
WIGHT  = 1280


labels = glob.glob(f"{labelpath}/*.txt")
labelsnum = len(labels)
print(f"labelsnum:{labelsnum}")

def xywh_to_ltrb(x, y, w, h, image_width, image_height):
    left = max(0, (x - w / 2) * image_width)
    top = max(0, (y - h / 2) * image_height)
    right = min(image_width, (x + w / 2) * image_width)
    bottom = min(image_height, (y + h / 2) * image_height)
    return int(left), int(top), int(right), int(bottom)

def remove_rectangle(imagepath,rectangle):
    image = cv2.imread(imagepath)
    for loc in rectangle:
        left,top,right,bottom = loc
        image[top:bottom,left:right] = 0
    cv2.imwrite(f"{imagepath}",image);
    
mask = {}
deletenum = 0
cache = {}
for i in labels:
    # print(i)
    name = os.path.basename(i).rsplit(".",1)[0]
    imgp  = labelpath.replace("labels","images")
    imgpath = f"{imgp}/{name}.jpg"
    newmeaage = []
    with open(f"{i}","r") as f:
        message = f.readlines() 
        if len(message) == 0:
            cache[i] = []
            continue
        for m in message:
            m0 = m.rstrip().split()
            # print(m0)
            x,y,w,h = map(float,m0[1:])
            left,top,right,bottom = xywh_to_ltrb(x,y,w,h,WIGHT,HEIGHT)
            if bottom>360:
                newmeaage.append(m)
            else:
                if mask.get(imgpath) == None:
                    mask[imgpath] = [(left,top,right,bottom)]
                else:
                    mask[imgpath].append((left,top,right,bottom))
                deletenum+=1
    cache[i] = newmeaage
    f.close()
    
print("**"*10+f"deletenum:{deletenum}"+"**"*10)

for path,message in cache.items():
    with open(f"{path}","w") as f:
        for m in message:
            f.write(m)
    f.close()
    
'''
calibrate
'''
count = 0
for i in labels:
    # print(i)
    newmeaage = []
    with open(f"{i}","r") as f:
        
        message = f.readlines() 
        if len(message) == 0:
            cache[i] = []
            continue
        for m in message:
            m0 = m.rstrip().split()
            # print(m0)
            x,y,w,h = map(float,m0[1:])
            left,top,right,bottom = xywh_to_ltrb(x,y,w,h,HEIGHT,WIGHT)
            if bottom>360:
                ...
            else:
                count += 1
    f.close()
    
print(count)
assert  count == 0,"calibrate success!!!"

for imagepath,rectangle in mask.items():
    remove_rectangle(imagepath,rectangle)
print("finish!!!")
