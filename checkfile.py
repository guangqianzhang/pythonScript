#!/usr/bin/env python
# -*- coding:utf-8 -*-
###
# File: /Users/simonliu/Documents/python/clean_annotation/clean_annotation_files.py
# Project: /Users/simonliu/Documents/python/clean_annotation
# Created Date: 2022-06-03 23:18:09
# Author: Simon Liu
# -----
# Last Modified: 2022-06-04 17:02:33
# Modified By: Simon Liu
# -----
# Copyright (c) 2022 SimonLiu Inc.
#
# May the force be with you.
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
###
import sys, os
import glob


def check(path1, path2):
    filelist1 = glob.glob(f"{path1}/*.*")
    filelist2 = glob.glob(f"{path2}/*.*")
    filelist1_ext = os.path.splitext(os.path.basename(filelist1[0]))[1]
    # filelist1_ext = os.path.splitext(os.path.split(filelist1[0])[1])[1] //这种方式也可以
    print("filelist1_ext:", filelist1_ext)
    filelist1 = [os.path.splitext(os.path.basename(f))[0] for f in filelist1 if os.path.isfile(f)]

    filelist2_ext = os.path.splitext(os.path.basename(filelist2[0]))[1]
    # filelist2_ext = os.path.splitext(os.path.split(filelist2[0])[1])[1] //这种方式也可以
    print("filelist2_ext:", filelist2_ext)
    filelist2 = [os.path.splitext(os.path.basename(f))[0] for f in filelist2 if os.path.isfile(f)]

    for f in filelist1:
        if f in filelist2:
            pass
        else:
            print(f"{f}{filelist1_ext}在 {path2} 中找不到对应的文件")

    for f in filelist2:
        if f in filelist1:
            pass
        else:
            print(f"{f}{filelist2_ext}在 {path1} 中找不到对应的文件")


def main():
    img_path = input('请输入图片文件夹位置(输入Q或q退出):')
    if img_path == "Q" or img_path == 'q':
        sys.exit()
    # img_path = "~/Movies/cat_video_frames_picked_224x224"
    img_path = os.path.expanduser(img_path)
    annotation_path = input('请输入标注文件夹位置(输入Q或q退出):')
    if annotation_path == "Q" or annotation_path == 'q':
        sys.exit()
    annotation_path = os.path.expanduser(annotation_path)
    check(img_path, annotation_path)


if __name__ == '__main__':
    main()

