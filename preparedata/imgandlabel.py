from PIL import Image
import os
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument('path1', help='img path left')
    parser.add_argument('path2', help='label path right')
    parser.add_argument('--imageH',default=480, help='the height of image')
    parser.add_argument('--imageW',default=640, help='the width of image')

    args = parser.parse_args()
    print(f'check the image from {args.path1} to label  {args.path2}')
    # 图像目录和标签列表文件路径
    image_dir = args.path1
    label_file = args.path2
    if args.imageH is None and args.imageW is None:
        imageH = args.imageH
        imageW = args.imageW
    else:
        imageH = 224
        imageW = 224
    # 读取标签列表
    with open(label_file, 'r') as f:
        label_list = f.read().splitlines()

    # 比较图像和标签列表
    for filename in os.listdir(image_dir):
        if filename.endswith('.png'):  # 假设图像格式为JPG
            image_path = os.path.join(image_dir, filename)
            image = Image.open(image_path)
            if (image.format.lower() != 'png' or
                    image.size[0] != imageH or
                    image.size[1] != imageW or
                    filename not in label_list):
                print('文件{}与标签列表不匹配'.format(filename))


if __name__ == '__main__':
    main()
