import glob
import sys

def image2txt():
    if len(sys.argv)<2:
        print("python image2txt.py [root] [txt]")
        return
    root = sys.argv[1]
    txt  = sys.argv[2]
    
    
    images = glob.glob(f"{root}/*")
   
    with open(f"{txt}","w+") as f:
        for idx,p in enumerate(images):
            if idx!=len(images)-1:
                f.write(p)
                f.write("\n")
            else:
                f.write(p)
                
if __name__ == "__main__":
    image2txt()
