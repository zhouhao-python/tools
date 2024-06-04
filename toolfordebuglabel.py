import os 
import shutil
import sys


if len(sys.argv)<1:
    print("python toolfordebuglabel.py [root]")
    pass

root = sys.argv[1]
tar = f"{root}/wrong"

source  = f"{root}/labels"

out = f"{root}/wronglabels"
os.makedirs(out,exist_ok= True)

tarn = os.listdir(tar)
tarn = [i.rsplit(".",1)[0] for i in tarn]
sourcen = os.listdir(source)

for i in sourcen:
    if i.rsplit(".",1)[0] in tarn:
        shutil.copy(os.path.join(source,i),os.path.join(out,i))
                 
