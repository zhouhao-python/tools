

import sys
root = sys.argv[1]
# root = "/media/wpy/558e3a8b-7a8f-4603-a6fb-20c87dbd584b/StainDetection/stain_black_pattern_train/stain_pure_0418"
imagepath = f"{root}/images"
labelspath = f"{root}/labels"
import os
import glob

trainimage = f"{imagepath.rsplit(os.sep,1)[0]}/train/images"
trainlabels = f"{imagepath.rsplit(os.sep,1)[0]}/train/labels"
valimage = f"{imagepath.rsplit(os.sep,1)[0]}/val/images"
vallabels = f"{imagepath.rsplit(os.sep,1)[0]}/val/labels"


os.makedirs(trainimage,exist_ok=True)
os.makedirs(trainlabels,exist_ok=True)
os.makedirs(valimage,exist_ok=True)
os.makedirs(vallabels,exist_ok=True)

images = sorted(list(glob.glob(f"{imagepath}/*")))
labels = sorted(list(glob.glob(f"{labelspath}/*")))

all = []
for img,lab in zip(images,labels):
    all.append((img,lab))

n = len(images)

import shutil

import random

random.seed(115)

from sklearn.model_selection import train_test_split
train,val_test = train_test_split(all,train_size=0.8,random_state=19950105)
# val_df,test_df = train_test_split(val_test_df,train_size=0.5,random_state=19950105)


for img,lab in train:
    shutil.copy(img,os.path.join(trainimage,os.path.basename(img)))
    shutil.copy(lab,os.path.join(trainlabels,os.path.basename(lab)))


for img,lab in val_test:
    shutil.copy(img,os.path.join(valimage,os.path.basename(img)))
    shutil.copy(lab,os.path.join(vallabels,os.path.basename(lab)))
    
     