import os, sys
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from argparse import ArgumentParser
from PIL import Image
import threading
import re
import matplotlib as mpl
import shutil
def main():
    # parser = ArgumentParser()
    # parser.add_argument('file', help='')
    # parser.add_argument('--re', help='')
    #
    # args = parser.parse_args()
    mutex = threading.Lock()
    file_c=''
    beams=16
    dir1=f'/home/jzl/zgq/f{beams}'
    txt_file='/media/jzl/Ubuntu 18.0/zgq/1.txt'
    dir2 =f'/home/jzl/zgq/l{beams}'
    score = [0.1, 0.3, 0.5, 0.7]


    beamsflag=False
    files16=[]
    files32=[]
    indxes=[]
    flag_l=False
    with open(txt_file,'r') as rf:
        # lines=rf.readlines()
        for line in rf:
            if '/' in line:
                line = line.split('/')
                file = line[0]
                s = line[1].split(' ')
                score_f=[]
                score_l=[]
                match = re.match(r"([a-z]+)([0-9]+)([a-z]+)([0-9]+)", s[0], re.I)
                if match:
                    items = match.groups()
                    try:
                        if items[0]=='f':
                            item=list(items[1])
                            for x in item:
                                file_png = os.path.join(dir1, f'lidar{int(x)/10}', file + '.png')
                                files32.append(file_png)
                        if items[2]=='l':
                            item = list(items[3])
                            for x in item:
                                file_png = os.path.join(dir2, f'lidar{int(x) / 10}', file + '.png')
                                files32.append(file_png)
                        elif  items[2]=='f':
                            item = list(items[3])
                            for x in item:
                                file_png = os.path.join(dir1, f'lidar{int(x)/ 10}', file + '.png')
                                files32.append(file_png)

                    except:
                        pass

                else:
                    match = re.match(r"([a-z]+)([0-9]+)", s[0], re.I)

                    if match:
                        items = match.groups()
                        try:
                            if items[0] == 'f':
                                item = list(items[1])
                                for x in item:
                                    file_png = os.path.join(dir1, f'lidar{int(x) / 10}', file + '.png')
                                    files32.append(file_png)
                            if items[2] == 'l':
                                item = list(items[3])
                                for x in item:
                                    file_png = os.path.join(dir2, f'lidar{int(x) / 10}', file + '.png')
                                    files32.append(file_png)
                            elif items[2] == 'f':
                                item = list(items[3])
                                for x in item:
                                    file_png = os.path.join(dir1, f'lidar{int(x) / 10}', file + '.png')
                                    files32.append(file_png)

                        except:
                            pass
    fig,axes = plt.subplots(11,4,figsize=(110,40))
    plt.subplots_adjust(left=None,bottom=None,right=None,top=None,wspace=0.15,hspace=0.15)
    indx=0
    for file in files32:
        def showimg(path,indx):
            img = Image.open(path)
            plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.15, hspace=0.15)
            plt.subplot(4, 4, indx)
            plt.axis('off')  # 关掉坐标轴为 off
            plt.title(path.split('/')[-1].split('-')[-1])  # 图像题目
            plt.imshow(img)
        dirs=file.split('/')[-1].split('-')[-1].split('.')[0]
        filesave=os.path.join(f'/media/jzl/Ubuntu 18.0/zgq/lidar/{beams}',dirs)
        if not os.path.exists(filesave):
            os.mkdir(filesave)

        indx+=1
        ff=f'-{indx}-' + file.split('/')[-1].split('-')[-1]
        shutil.copy(file,os.path.join(filesave,ff))
        showimg(file,indx)

    plt.show()







if __name__ == '__main__':
    main()


