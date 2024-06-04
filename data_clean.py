
'''
去除文件夹中重复图像
'''


import cv2
import numpy as np
import os


def get_match_num(path_img1,path_img2):
    
    psd_img_1 = cv2.imread(path_img1, cv2.IMREAD_GRAYSCALE)
    psd_img_2 = cv2.imread(path_img2, cv2.IMREAD_GRAYSCALE)

    # 3) SIFT特征计算
    sift = cv2.SIFT_create()

    psd_kp1, psd_des1 = sift.detectAndCompute(psd_img_1, None)
    psd_kp2, psd_des2 = sift.detectAndCompute(psd_img_2, None)
    
    # print(psd_des1,psd_des2)
    # 4) Flann特征匹配
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(psd_des1, psd_des2, k=2)
    goodMatch = []
    for m, n in matches:
        # goodMatch是经过筛选的优质配对，如果2个配对中第一匹配的距离小于第二匹配的距离的1/2，基本可以说明这个第一配对是两幅图像中独特的，不重复的特征点,可以保留。
        if m.distance < 0.50*n.distance:
            goodMatch.append(m)
    # 增加一个维度
    # goodMatch = np.expand_dims(goodMatch, 1)
    return len(goodMatch)

def main(root,thr = 5):
    
    img_list = [i for i in os.listdir(root) if i.endswith('jpg')]
    slow = 0
    fast = slow+1
    while fast<len(img_list) and slow < len(img_list):
        img1_path = os.path.join(root,img_list[slow])
        img2_path = os.path.join(root,img_list[fast])
        match_num = get_match_num(img1_path,img2_path)
        if match_num>thr:
            os.remove(img2_path)
            print(img2_path)
            fast+=1
        else:
            slow = fast
            fast = slow+1
            print("current slow:{} fast:{}".format(slow,fast))


import sys 


if len(sys.argv)<2:
    print("python data_clean.py [root] [thr]")
root = sys.argv[1]
if len(sys.argv) <3:
    thr = 5
elif len(sys.argv) ==3:
    thr = sys.argv[2]
main(root = root)

# a = get_match_num("../202306192135452240.jpg","../202306192135452260.jpg")
# print(a)