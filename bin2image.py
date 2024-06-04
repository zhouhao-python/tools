import cv2
import numpy as np
import struct
import glob
import sys
import os
from tqdm import tqdm as dm
from datetime import datetime

HEIGHT = 720
WIGHT = 1280

def bin2image():
    # 判断传进来的参数
    if len(sys.argv) < 2:
        print('bin2image [path] [outtype]')
        return 
    if len(sys.argv) < 3:
        outtype = 'jpg'
    else:
        outtype = sys.argv[2]
    # 处理文件夹和目录
    root = sys.argv[1]
    output = root + '_output'
    os.makedirs(output, exist_ok = True)
    bins = os.listdir(root)
    bins = sorted(bins,key = lambda x:int(x.split('out')[-1].split('w')[0]))
    bins = [os.path.join(root,i) for i in bins]

    print(len(bins))
    # 进度条的加载
    for path in dm(bins):
        with open(path,'rb') as f:
            data = f.read()
        f.close()
        int_values = []
        for byte in data:
            value = struct.unpack('B',bytes([byte]))[0]
            int_values.append(value)
        if len(int_values) != WIGHT*HEIGHT:continue
        image = np.array(int_values).reshape(HEIGHT,WIGHT).astype(np.uint8)
        current_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        cv2.imwrite(f'{os.path.join(output,current_time + f".{outtype}")}',image)
        
        
if __name__ == '__main__':
    bin2image()



