import os 

import sys 

labelpath = sys.argv[1]
if len(sys.argv)<2:
    print("python makemul2single.py [path]")
    exit()

labels = os.listdir(labelpath)

cache = {}


def makemul2single(message):
    result = []
    for m in message:
        if m[0] == "1":
            result.append('0'+m[1:])
        else:
            result.append(m)
    return result    
    
for i in labels:
    p = os.path.join(labelpath,i)
    with open(p,'r') as f:
        message = f.readlines()
        
        result = makemul2single(message)
        cache[p] = result
    f.close()

        
for k,v in cache.items():
    with open(k,"w") as f:
        for i in v:
            f.write(i)
    f.close()