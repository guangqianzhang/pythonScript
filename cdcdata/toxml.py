# txt_to_xml.py
# encoding:utf-8
# 根据一个给定的XML Schema，使用DOM树的形式从空白文件生成一个XML
import json
import os
import shutil
from xml.dom.minidom import Document
import numpy as np
labels_dir = '/home/cqjtu/Documents/dataset/20230626'
VOC_ROOT = '/media/cqjtu/Kaixia/数据堂验收数据/2'
VOCimagedir = 'JPEGImages'
VOCanndir = 'Annotations'
VOCsetdir = 'ImageSets'
VOCPcd = 'Pcd'
calib_file = '/home/cqjtu/Documents/dataset/KITTI2VOC/cdc/calibration_.json'
import vis
import cv2

label_dict = {'Deceleration_zone': 0, 'Manhole_cover': 1}
class_ind = ('Deceleration_zone', 'Manhole_cover')

def load_json(file):
    with open(file, 'r') as f:
        json_data = f.read()
        data = json.loads(json_data)
    return data


def load_calib(calib_file):
    f = open(calib_file, "r", encoding='utf-8')
    calib = json.load(f)

    return calib


def copy_file(source_path, destination_path):
    try:
        shutil.copy2(source_path, destination_path)
        # print("copy done!")
    except FileNotFoundError:
        print("找不到源文件或目标目录。")
    except IOError:
        print("读取或写入文件时出错。")
    except shutil.SameFileError:
        print("源文件和目标文件相同。")


def generate_xml(name, split_lines, img_size, class_ind):
    doc = Document()  # 创建DOM文档对象

    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    title = doc.createElement('folder')
    title_text = doc.createTextNode('cdc')
    title.appendChild(title_text)
    annotation.appendChild(title)

    img_name = name + '.png'

    title = doc.createElement('filename')
    title_text = doc.createTextNode(img_name)
    title.appendChild(title_text)
    annotation.appendChild(title)

    source = doc.createElement('source')
    annotation.appendChild(source)

    title = doc.createElement('database')
    title_text = doc.createTextNode('The cdc Database')
    title.appendChild(title_text)
    source.appendChild(title)

    title = doc.createElement('annotation')
    title_text = doc.createTextNode('cdc')
    title.appendChild(title_text)
    source.appendChild(title)

    size = doc.createElement('size')
    annotation.appendChild(size)

    title = doc.createElement('width')
    title_text = doc.createTextNode(str(img_size[1]))
    title.appendChild(title_text)
    size.appendChild(title)

    title = doc.createElement('height')
    title_text = doc.createTextNode(str(img_size[0]))
    title.appendChild(title_text)
    size.appendChild(title)

    title = doc.createElement('depth')
    title_text = doc.createTextNode(str(img_size[2]))
    title.appendChild(title_text)
    size.appendChild(title)

    for bbox2d, bbox_3d, label in split_lines:
        if label in class_ind:
            object = doc.createElement('object')
            annotation.appendChild(object)

            title = doc.createElement('name')
            title_text = doc.createTextNode(label)
            title.appendChild(title_text)
            object.appendChild(title)

            sorted_coordinates = sorted(bbox2d[0], key=lambda coord: coord[0])
            # 找到最小的 x 坐标值对应的点
            point1 = sorted_coordinates[0]
            # 找到最大的 x 坐标值对应的点
            point2 = sorted_coordinates[-1]

            # 根据 y 坐标值从小到大排序
            sorted_coordinates = sorted(bbox2d[0], key=lambda coord: coord[1])
            # 找到最小的 y 坐标值对应的点
            point3 = sorted_coordinates[0]
            # 找到最大的 y 坐标值对应的点
            point4 = sorted_coordinates[-1]

            bndbox = doc.createElement('bndbox')
            object.appendChild(bndbox)
            title = doc.createElement('xmin')
            title_text = doc.createTextNode(str(int(float(point1[0]))))
            title.appendChild(title_text)
            bndbox.appendChild(title)
            title = doc.createElement('ymin')
            title_text = doc.createTextNode(str(int(float(point3[1]))))
            title.appendChild(title_text)
            bndbox.appendChild(title)
            title = doc.createElement('xmax')
            title_text = doc.createTextNode(str(int(float(point2[0]))))
            title.appendChild(title_text)
            bndbox.appendChild(title)
            title = doc.createElement('ymax')
            title_text = doc.createTextNode(str(int(float(point4[1]))))
            title.appendChild(title_text)
            bndbox.appendChild(title)

    # 将DOM对象doc写入文件
    f = open(VOC_ROOT+VOCanndir+'/' + name + '.xml', 'w')  # create a new xml file
    f.write(doc.toprettyxml(indent=''))
    f.close()


def topixs(bbox_3d, labels):
    calib = load_calib(calib_file)
    l2c = np.array(calib["Extrinsic"])
    intri = np.array(calib["Intrinsic"])
    intrinisic = np.eye(4)
    intrinisic[:3, :3] = intri
    coords = []
    coords3d=[]
    tilte = []
    if bbox_3d is not None and len(bbox_3d) > 0:
        # print(f'bbox shape:{bbox_3d.shape}')
        # label= [labels[i] for i in range(labels.shape[0])]
        bbox = [bbox_3d[i:i + 1, :, :] for i in range(bbox_3d.shape[0])]
        for label_, box_ in zip(labels, bbox):
            coords_ = np.concatenate(
                [box_.reshape(-1, 3), np.ones((8, 1))], axis=-1
            )
            coords_ = l2c @ coords_.T
            coords_ = intrinisic @ coords_

            coords_ = coords_.reshape(-1, 4, 8)

            indices = np.all(coords_[:, 2] > 0, axis=1)
            coords_ = coords_[indices]

            indices = np.argsort(-np.min(coords_[..., 2], axis=1))
            coords_ = coords_[indices]

            coords_ = coords_.reshape(-1, 8).T
            if 0  not in coords_.shape:
                coords_[:, 2] = np.clip(coords_[:, 2], a_min=1e-5, a_max=1e5)
                coords_[:, 0] /= coords_[:, 2]
                coords_[:, 1] /= coords_[:, 2]

                coords_ = coords_[..., :2].reshape(-1, 8, 2)

            coords.append(coords_)
            coords3d.append(box_)
            tilte.append(class_ind[label_])

    return coords, coords3d, tilte


# #source code
if __name__ == '__main__':


    # cur_dir=os.getcwd()  # current path
    # labels_dir=os.path.join(cur_dir,'labels') # get the current path and build a new path.and the result is'../yolo_learn/labels'
    # txt_list = glob.glob('/media/cqjtu/PortableSSD/Deceleration_zone/*')

    for parent, dirnames, filenames in os.walk(labels_dir):  # 分别得到根目录，子目录和根目录下文件
        name = os.path.basename(parent)
        img_size = None
        bboxs = None
        for file_name in filenames:
            if '.json' in file_name:
                full_path = os.path.join(parent, file_name)  # 获取文件全路径
                try:
                    data = load_json(full_path)
                    bbox_2d, bbox_3d, label = vis.get_gt_bbox(data)
                    bboxs, bbox_3d, label  = topixs(bbox_3d, label)
                    objs = data['objects']
                    num_obj = len(objs)
                    if num_obj>1:
                        print(f'{num_obj} objs({label}) in file {file_name}')


                except IOError as ioerr:
                    print('File error:' + str(ioerr))
                    print(f'err open in  file:{full_path}')

            if '.png' in file_name:
                image_name = file_name
                image_path = os.path.join(parent, image_name)
                img_size = cv2.imread(image_path).shape
                name = os.path.basename(parent)
                copy_file(image_path, os.path.join(os.path.join(VOC_ROOT, VOCimagedir), f'{name}.png'))
            if '.pcd' in file_name:
                pcd_name = file_name
            if img_size is not None and name is not None and bboxs is not None:
                generate_xml(name, zip(bboxs, bbox_3d, label), img_size, class_ind)
print('all txts has converted into xmls')
