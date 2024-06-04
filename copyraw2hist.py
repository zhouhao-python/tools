'''_summary_
直方图均值化 
'''

import os
import shutil
import sys


tarpath = sys.argv[1]
source = sys.argv[2]

sources = os.listdir(source)
tarimgs = os.listdir(tarpath)

print(len(sources),len(tarimgs))


count = 0
for i in sources:
    if i in tarimgs:
        shutil.copy(os.path.join(source,i),os.path.join(tarpath,i))
        count+=1
print(f"finish:{count}")