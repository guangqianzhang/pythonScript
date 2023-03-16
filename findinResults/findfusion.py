import os, sys
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from argparse import ArgumentParser
from PIL import Image
import threading
import shutil


def main():
    # parser = ArgumentParser()
    # parser.add_argument('file', help='')
    # parser.add_argument('--re', help='')
    #
    # args = parser.parse_args()
    mutex = threading.Lock()
    file_c=''
    beams=32
    dir3='/home/jzl/zgq/camera'
    dir1=f'/home/jzl/zgq/f{beams}'
    dir2 =f'/home/jzl/zgq/l{beams}'
    score = [0.1, 0.2, 0.3]

    def create_dir(file_path):
        if os.path.exists(file_path) is False:
            os.makedirs(file_path)
    def inputargs(file):
        nn = -1
        while True:
            inputf = input('which chose for ..')
            if inputf is not None:
                with open('record.txt', 'a') as f:
                    f.write(file_c + f'/{inputf}\n')
            if inputf=='t':
                diro=f'/media/jzl/Ubuntu 18.0/zgq/fusion/{beams}'
                for i in score:
                    f = f'{i}-'+file_c+'.png'

                    lidardir = os.path.join(diro,str(i))
                    lidarfile=os.path.join(lidardir,f)
                    create_dir(lidardir)
                    file = os.path.join(dir3,f'viz{i}', f'lidar{i}', file_c + '.png')
                    shutil.copy(file, lidarfile)
                    for ind in range(6):
                        imgdir=os.path.join(diro,str(i))
                        imgf=f'camera-{ind}-'+file_c+'.png'
                        imgsave=os.path.join(imgdir,imgf)
                        create_dir(imgdir)
                        file = os.path.join(dir3, f'viz{i}', f'camera-{ind}', file_c + '.png')
                        shutil.copy(file, imgsave)

    t1 = threading.Thread(target=inputargs, args=(file_c,))
    t1.start()

    listFiles = os.listdir(dir3+'/viz0.1/lidar0.1')
    for file in listFiles:
        mutex.acquire()
        file_c=file.split('.')[0]
        mutex.release()
        plt.figure(num=file_c, figsize=(15, 8))

        def showimg(dir,indx):
            img = os.path.join(dir, f'viz{score[indx]}',f'lidar{score[indx]}', file_c + '.png')
            img = Image.open(img)
            if f'f{beams}' in dir:
                plt.subplot(1, 3, indx + 1)
                plt.axis('off')  # 关掉坐标轴为 off
                plt.title(f'f{beams}-{score[indx]}')  # 图像题目
                plt.imshow(img)
            elif f'l{beams}' in dir:
                plt.subplot(2, 5, indx + 7)
                plt.axis('off')  # 关掉坐标轴为 off
                plt.title(f'l{beams}-{score[indx]}')  # 图像题目
                plt.imshow(img)
            elif 'camera' in dir:
                plt.subplot(1,3,indx+1)
                plt.axis('off')
                plt.title(f'cam-{score[indx]}')
                plt.imshow(img)

        for indx in range(len(score)):
            try:
                showimg(dir3,indx)
                # showimg(dir2,indx)
            except:
                pass
        plt.show()







if __name__ == '__main__':
    main()


