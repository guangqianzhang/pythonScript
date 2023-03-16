#! encoding: utf-8
from PIL import Image
import matplotlib.pyplot as plt
import os.path as osp
from argparse import ArgumentParser
import argparse
def main():
    parser = ArgumentParser()
    parser.add_argument('file',help='pkl file')
    parser.add_argument('--result',help='result file')
    parser.add_argument('--score',nargs='+',help='the 3 score')
    parser.add_argument('--dir',type=str,help='')

    def parse_tuple(tuple_str):
        try:
            values = tuple(map(int, tuple_str.strip('()').split(',')))
            return tuple(values)
        except ValueError:
            raise argparse.ArgumentTypeError('Invalid tuple')
    parser.add_argument('--size',type=parse_tuple)

    args=parser.parse_args()

    # 打开四张图片
    image_type='.png'
    if args.dir is None:
        dir='/home/zgq/Documents/jzlby/3216'
    else:
        dir=args.dir

    if args.score is None:
        score=[0.4,0.3,0.2]
    else:
        score=args.score
    if args.size is None:
        size = (300, 400)
    else:
        size=args.size
    img1 = Image.open('/home/zgq/Documents/jzlby/gt/'+args.file+image_type)
    img2 = Image.open(osp.join(dir,f'lidar{score[0]}',args.file+image_type))
    img3 = Image.open(osp.join(dir,f'lidar{score[1]}',args.file+image_type))
    img4 = Image.open(osp.join(dir,f'lidar{score[2]}',args.file+image_type))

    def center_crop(image, size):

        width, height = image.size
        left = (width - size[0]) // 2
        top = (height - size[0]) // 2
        right = (width + size[1]) // 2
        bottom = (height + size[1]) // 2
        return image.crop((left, top, right, bottom))

    # 调整图片大小为相同尺寸

    img1 = center_crop(img1,size)
    img2 = center_crop(img2,size)
    img3 = center_crop(img3,size)
    img4 = center_crop(img4,size)

    # 绘制图像
    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(12, 9))

    # 第一行
    axs[0, 0].imshow(img1)
    axs[0, 0].axis("off")
    axs[0, 0].set_title('gt')

    axs[0, 1].imshow(img2)
    axs[0, 1].axis("off")
    axs[0, 1].set_title(f'score{score[0]}')

    axs[0, 2].imshow(img3)
    axs[0, 2].axis("off")
    axs[0, 2].set_title(f'score{score[1]}')

    axs[0, 3].imshow(img4)
    axs[0, 3].axis("off")
    axs[0, 3].set_title(f'score{score[2]}')

    # # 第二行
    # axs[1, 0].imshow(img2)
    # axs[1, 0].axis("off")
    # axs[1, 1].imshow(img3)
    # axs[1, 1].axis("off")
    # axs[1, 2].imshow(img4)
    # axs[1, 2].axis("off")
    # axs[1, 3].imshow(img1)
    # axs[1, 3].axis("off")
    #
    # # 第三行
    # axs[2, 0].imshow(img3)
    # axs[2, 0].axis("off")
    # axs[2, 1].imshow(img4)
    # axs[2, 1].axis("off")
    # axs[2, 2].imshow(img1)
    # axs[2, 2].axis("off")
    # axs[2, 3].imshow(img2)
    # axs[2, 3].axis("off")

    plt.show()
if __name__=='__main__':
    main()