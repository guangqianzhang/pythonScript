import os, sys
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from argparse import ArgumentParser
from PIL import Image
import threading



def main():
    # parser = ArgumentParser()
    # parser.add_argument('file', help='')
    # parser.add_argument('--re', help='')
    #
    # args = parser.parse_args()
    mutex = threading.Lock()
    file_c=''
    beams=32
    dir1=f'/home/jzl/zgq/f{beams}'
    dir2 =f'/home/jzl/zgq/l{beams}'
    score = [0.1, 0.3, 0.4]


    def inputargs(file):
        while True:
            inputf = input('which chose for ..')
            if inputf is not None:
                with open('record.txt', 'a') as f:
                    f.write(file_c + f'/{inputf}\n')
    t1 = threading.Thread(target=inputargs, args=(file_c,))
    t1.start()

    listFiles = os.listdir(dir1+'/gt')
    for file in listFiles:
        mutex.acquire()
        file_c=file.split('.')[0]
        mutex.release()

        plt.figure(num=file_c, figsize=(15, 8))

        img_gt=Image.open(os.path.join(dir1+'/gt',file))
        # plt.subplot(2, 4, 1)
        # plt.axis('off')  # 关掉坐标轴为 off
        # plt.title(f'{beams}-gt')  # 图像题目
        # plt.imshow(img_gt)

        def showimg(dir,indx):
            img = os.path.join(dir, f'lidar{score[indx]}', file_c + '.png')
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

        for indx in range(len(score)):
            try:
                showimg(dir1,indx)
                # showimg(dir2,indx)
            except:
                pass
        plt.show()







if __name__ == '__main__':
    main()


