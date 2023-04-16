import os
import math
import shutil

# 相机文件夹和雷达文件夹的路径
camera_folder = '/home/zgq/Documents/calibration415/analyze/selected'
lidar_folder = '/home/zgq/Documents/calibration415/analyze/lidar'

# 新的雷达文件夹路径
lidar_new_folder = '/home/zgq/Documents/calibration415/analyze/lidar_new_folder_path2'

# 创建新的雷达文件夹
if not os.path.exists(lidar_new_folder):
    os.makedirs(lidar_new_folder)

# 读取相机文件夹中的文件列表
camera_files = os.listdir(camera_folder)
copy_count=0
# 遍历相机文件夹中的每一个文件
for camera_file in camera_files:
    # 解析相机文件的时间戳
    camera_timestamp = os.path.splitext(camera_file)[0]
    camera_timestamp = float(camera_timestamp)
    
    # 在雷达文件夹中查找与相机文件时间戳相近的文件
    lidar_files = os.listdir(lidar_folder)
    nearest_lidar_file = None
    min_time_diff = 5
    
    for lidar_file in lidar_files:
        # 解析雷达文件的时间戳
        lidar_timestamp = os.path.splitext(lidar_file)[0]
        lidar_timestamp = float(lidar_timestamp)
        
        # 计算时间戳之间的差距
        time_diff = abs(camera_timestamp - lidar_timestamp)
        # print(time_diff)
        # 如果时间差小于当前最小时间差，则更新最小时间差和对应的雷达文件
        if time_diff < min_time_diff:
            min_time_diff = time_diff
            nearest_lidar_file = lidar_file
    
    # 拷贝最近的雷达文件到新的雷达文件夹中
    lidar_path = os.path.join(lidar_folder, nearest_lidar_file)
    lidar_new_path = os.path.join(lidar_new_folder, nearest_lidar_file)
    shutil.copy2(lidar_path, lidar_new_path)
    copy_count+=1

    
    # 打印相机文件和对应的最近的雷达文件
    print(camera_file, nearest_lidar_file)
print(f"have copied {copy_count} files")
