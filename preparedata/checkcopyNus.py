import os, sys
import filecmp
import shutil
from tqdm import tqdm
from argparse import ArgumentParser
import shutil


def main():
    parser = ArgumentParser()
    parser.add_argument('file1', help='copyto abspath left')
    parser.add_argument('file2', help='copy abspath right')
    parser.add_argument('--excp', help='excpet dir')
    args = parser.parse_args()
    print(f'check the files copied from {args.file1} to {args.file2}')
    # dir1='/media/zgq/Elements/data/nuscenes/samples/CAM_BACK_LEFT'
    # dir2='/media/zgq/Elements/data/nuscenes/test/v1.0-test_blobs/samples/CAM_BACK_LEFT'
    result = compare(args.file1, args.file2)
    # print(f'there {count} in file2')
    difsw,difsa=result
    if len(difsw) == 0 and len(difsa)==0:
        print('copy all done')
    else:
        print(result)
        with open('reslut.txt', 'w') as file:
            file.write(result)
        # for file in result:
        #     path = '\\'.join(file.split('/')[1:])
        #     sourcepath=os.path.join('F:\\data',path)
        #     shutil.copy(sourcepath ,os.path.join(os.getcwd(),path))


def compare(file1: str, file2: str):
    diffiles = []

    linuxsw = []
    linuxsa = []
    winsw = []
    winsa = []

    species_lists = ['CAM_BACK', 'CAM_BACK_LEFT', 'CAM_BACK_RIGHT', 'CAM_FRONT', 'CAM_FRONT_LEFT', 'CAM_FRONT_RIGHT',
                     'LIDAR_TOP', 'RADAR_BACK_LEFT', 'RADAR_BACK_RIGHT', 'RADAR_BACK_RIGHT', 'RADAR_FRONT',
                     'RADAR_FRONT_LEFT', 'RADAR_FRONT_RIGHT']
    win = {}
    linux = {}
    win.setdefault('sweeps', dict.fromkeys(species_lists, []))
    win.setdefault('samples', dict.fromkeys(species_lists, []))
    linux.setdefault('sweeps', dict.fromkeys(species_lists, []))
    linux.setdefault('samples', dict.fromkeys(species_lists, []))

    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

        for l in lines1:
            path = '/'.join(l.split('\\'))
            # path = ('./' + str.join('/', (path.split('/')[3:])))
            # # path=str.join('/', (path.split('/')[3:]))
            # wintolinux.append(path)

            file = path.split('/')[-1]
            win[path.split('/')[4]][path.split('/')[5]].append(file)

        for l in lines2:
            # path = '/'.join(l.split('/')[1:])
            path = l
            file = l.split('/')[-1]
            if 's' in path.split('/')[2]:
                linux[path.split('/')[2]][path.split('/')[3]].append(file)


    for esp in species_lists:
        print(esp)
        # print(sorted(win['samples'][esp])-sorted(linux['samples'][esp]))
        difsa = [file for file in tqdm(win['samples'][esp]) if file not in linux['samples'][esp]]
        print('difsa{} {}'.format(esp,len(difsa)))
        print(difsa)

        difsw = [file for file in tqdm(win['sweeps'][esp]) if file not in linux['sweeps'][esp]]
        print('difsw {} {}'.format(esp,len(difsw)))
        print(difsw)

        difsas=[]
        difsws=[]
        difsas.extend(difsa)
        difsws.extend(difsw)
    return zip(difsws,difsas)


if __name__ == '__main__':
    main()
# 比较复制后的两个文件内容并重新复制遗漏的文件
# ls -l |grep "^-"|wc -l 参看文件个数
# rsync -avzh /path/to/source/ /path/to/destination/ --checksum

# dir /B /S /A-D "C:\path\to\folder" > "C:\path\to\output.txt" windows
#  find /path/to/folder -type f > /path/to/output.txt   linux
