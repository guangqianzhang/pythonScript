# create_train_test_txt.py
# encoding:utf-8
import json
import pdb
import glob
import os
import random
import math
def load_json(file):
    with open(file, 'r') as f:
        json_data = f.read()
        data = json.loads(json_data)
    return data
def get_sample_value(txt_name, category_name):
    label_path = '/media/cqjtu/PortableSSD/Deceleration_zone/'
    json_path = os.path.join(label_path,txt_name)
    txt_list = glob.glob(json_path+'/*')
    for file in txt_list:
        if '.json' in file:
            try:
                data = load_json(file)
                objs = data['objects']
                name=[]
                for obj in objs:
                    name.append(obj['label'])
                if category_name in name:
                    return ' 1'
                else:
                    return '-1'
            except IOError as ioerr:
                print('File error:'+str(ioerr))

txt_list_path = glob.glob('/home/cqjtu/Documents/dataset/CDC/JPEGImages/*')
txt_list = []

for item in txt_list_path:
    temp1,temp2 = os.path.splitext(os.path.basename(item))
    txt_list.append(temp1)
txt_list.sort()  # name
print(txt_list,'\n\n')

# 有博客建议train:val:test=8:1:1，先尝试用一下
num_trainval = random.sample(txt_list, int(math.floor(len(txt_list)*9/10.0))) # 可修改百分比
num_trainval.sort()
print(len(num_trainval),'\n\n')

num_train = random.sample(num_trainval, int(math.floor(len(num_trainval)*8/9.0))) # 可修改百分比
num_train.sort()
print(len(num_train),'\n\n')

num_val = list(set(num_trainval).difference(set(num_train)))
num_val.sort()
print(len(num_val),'\n\n')

num_test = list(set(txt_list).difference(set(num_trainval)))
num_test.sort()
print(len(num_test),'\n\n')

#pdb.set_trace()

Main_path = '/home/cqjtu/Documents/dataset/CDC/ImageSets/Main/'
train_test_name = ['trainval','train','val','test']
category_name  = {'Deceleration_zone', 'Manhole_cover'}

# 循环写trainvl train val test
for item_train_test_name in train_test_name:
    list_name = 'num_'
    list_name += item_train_test_name
    train_test_txt_name = Main_path + item_train_test_name + '.txt'
    try:
        # 写单个文件
        with open(train_test_txt_name, 'w') as w_tdf:
            # 一行一行写
            for item in eval(list_name):
                w_tdf.write(item+'\n')
        # 循环写person car truck
        for item_category_name in category_name:
            category_txt_name = Main_path + item_category_name + '_' + item_train_test_name + '.txt'
            with open(category_txt_name, 'w') as w_tdf:
                # 一行一行写
                for item in eval(list_name):
                    w_tdf.write(item+' '+ get_sample_value(item, item_category_name)+'\n')
    except IOError as ioerr:
        print('File error:'+str(ioerr))
