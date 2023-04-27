# -*- coding: utf-8 -*-
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import torch
import json
from tsv import TSVFile
import cv2
tsv_file_path = '/home/cqjtu/Documents/cc3m/train-0000.tsv'
tsv_depth_file_path = '/home/cqjtu/Documents/cc3m_depth/train-0000.tsv'


def decode_base64_to_pillow(image_b64):
    return Image.open(BytesIO(base64.b64decode(image_b64))).convert('RGB')


def decode_tensor_from_string(arr_str, use_tensor=True):
    arr = np.frombuffer(base64.b64decode(arr_str), dtype='float32')
    if use_tensor:
        arr = torch.from_numpy(arr)
    return arr


def decode_item_depth(item):
    "This is for decoding TSV for depth data"
    item = json.loads(item)
    item['depth'] = decode_base64_to_pillow(item['depth'])
    return item


def decode_item(item):
    "This is for decoding TSV for box data"
    item = json.loads(item)
    item['image'] = decode_base64_to_pillow(item['image'])

    for anno in item['annos']:
        anno['image_embedding_before'] = decode_tensor_from_string(anno['image_embedding_before'])
        anno['text_embedding_before'] = decode_tensor_from_string(anno['text_embedding_before'])
        anno['image_embedding_after'] = decode_tensor_from_string(anno['image_embedding_after'])
        anno['text_embedding_after'] = decode_tensor_from_string(anno['text_embedding_after'])
    return item



tsvfile = TSVFile(tsv_file_path)
tsvdepthfile = TSVFile(tsv_depth_file_path)
for idx in zip(tsvfile,tsvdepthfile):
    _, item=idx[0]
    _,itemdepth=idx[1]

    itemdepth= decode_item_depth(itemdepth)
    depth_data_id,  depth_img = itemdepth.values()
    np_Dimage = np.array(depth_img)
    np_Dimage = cv2.cvtColor(np_Dimage, cv2.COLOR_RGB2BGR)

    item= decode_item(item)
    data_id,img,filename,caption,ann=item.values()
    bbox=ann[0]['bbox']
    assert (len(bbox)==4)
    label=str(data_id)+':'+caption
    np_image = np.array(img)
    opencv_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
    if label is not None: cv2.putText(opencv_image, label, (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100,0,255), 1)
    if bbox is not None: cv2.rectangle(opencv_image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0,0,255), 2)

    cv2.imshow('original Image',opencv_image)
    cv2.imshow('depth Image',np_Dimage)
    cv2.waitKey(0)
cv2.destroyAllWindow()
