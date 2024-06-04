import os
import tqdm

# CLASSNAMEHASHMAP = {0:"Waterstain",1:"Waterstain",2:"Waterstain",
#                     3:"Waterstain",4:"Waterstain",5:"Waterstain"}

CLASSNAMEHASHMAP = {0:"stain",1:"coke",2:"milk",
                    3:"edibleoil",4:"oyster",5:"soysauce"}


ORGW = 1280;
ORGH = 720;

class GT2YOLO():
    def __init__(self,drpath,outpath,orgw,orgh):
        self.drpath = drpath;
        self.outpath = outpath
        self.orgw = orgw
        self.orgh = orgh;
        os.makedirs(self.outpath,exist_ok= True)
        
    def xywh2xyxy(self,x,y,w,h):
        x,y,w,h = x*self.orgw,y*self.orgh,w*self.orgw,h*self.orgh
        x0,y0 = int(x-w//2),int(y-h//2)
        x1,y1 = int(x+w//2),int(y+h//2)
        return (x0,y0,x1,y1)
    
    def dirGt2yolo(self):
        sources = os.listdir(self.drpath)
        for txt in tqdm.tqdm(sources):
            self.oneGt2Yolo(txt)
        print("conversion finish!!!");
        
        
    def oneGt2Yolo(self,txt):
        with open(os.path.join(self.drpath,txt),"r",) as f:
            result = []
            message = f.readlines()
            message = list(map(str.rstrip,message))
            message = [i.split() for i in message]
            for idx,m in enumerate(message):
                cls,x,y,w,h = int(m[0]),float(m[1]),float(m[2]),\
                    float(m[3]),float(m[4])
                claname = CLASSNAMEHASHMAP.get(cls)
                assert claname is not None, "classhashmap error!!"
                x0,y0,x1,y1 = self.xywh2xyxy(x,y,w,h)
                result.append("{} {} {} {} {}".format(claname,x0,y0,x1,y1));
        f.close()
        with open(os.path.join(self.outpath,txt),"w",) as f:
            for idx,l in enumerate(result):
                f.write(l)
                f.write("\n");
        f.close()
                

if __name__ == "__main__":
    import sys
    if len(sys.argv)<3:
        print("python gt2yolo.py [gtpath] [outpath]")
        exit()
    gtpath = sys.argv[1]
    outpath = sys.argv[2]
    
    gt2yolo = GT2YOLO(drpath=gtpath,outpath=outpath,orgh=ORGH,orgw=ORGW);
    gt2yolo.dirGt2yolo();
        
        
    