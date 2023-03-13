import os, sys
import filecmp
import shutil
from tqdm import tqdm
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument('path1', help='copyto abspath left')
    parser.add_argument('path2', help='copy abspath right')
    parser.add_argument('--excp', help='excpet dir')
    args = parser.parse_args()
    print(f'check the files copied from {args.path2} to {args.path1}')
    # dir1='/media/zgq/Elements/data/nuscenes/samples/CAM_BACK_LEFT'
    # dir2='/media/zgq/Elements/data/nuscenes/test/v1.0-test_blobs/samples/CAM_BACK_LEFT'
    result = compare(args.path1, args.path2)
    if len(result) == 0:
        print('copy all done')


def compare(path1, path2):
    diffiles = []
    dircomp = filecmp.dircmp(path1, path2)

    if len(dircomp.common_dirs) > 0:
        for item in dircomp.common_dirs:
            if not item == 'CAM_BACK':
                compare(os.path.join(path1, item), os.path.join(path2, item))
    else:
        i = 0
        pathlist = path1.split('/')
        for file in dircomp.right_list:
            if not file in dircomp.common_files:
                i += 1
                # print(file)
                diffiles.append(file)
        print(f' {i} files copy fail  in {pathlist[-1]}')
        print(f'{pathlist[-1]} has all : {len(dircomp.right_list)}')
        print(f'{pathlist[-1]} had copied:{len(dircomp.common_files)}')
        if not len(dircomp.right_list) == len(dircomp.common_files):

            if (float(len(dircomp.right_list))/(len(dircomp.common_files)+1))>2:
                copyflag = input('there more than a half, whether copy the files...y/n')
            else:
                print('begin to copy>>>>>>>')
                for img in tqdm(diffiles, bar_format="{l_bar}{bar:15}{r_bar}"):
                    source = os.path.join(path2, img)
                    assert os.path.isabs(source)
                    target = os.path.join(path1, img)
                    # print(f'copying {img} to {target}>>>>>>')
                    shutil.copy(source, target)
                    # diffiles.remove(img)
                    # print(f'left {len(diffiles)}')
            # elif copyflag == 'n':
            #     pass
                compare(path1, path2)
        else:
            print(f'copy well done in {pathlist[-1]}')
    return diffiles


if __name__ == '__main__':
    main()
# 比较复制后的两个文件内容并重新复制遗漏的文件
# ls -l |grep "^-"|wc -l 参看文件个数
# rsync -avzh /path/to/source/ /path/to/destination/ --checksum