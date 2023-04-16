import os
import cv2

# 播放文件夹路径
play_folder = '/home/zgq/Documents/calibration415/解析/相机'

# 遍历文件夹
for file_name in os.listdir(play_folder):
    # 判断是否是图片文件
    if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
        # 读取图片
        img = cv2.imread(os.path.join(play_folder, file_name))
        # 显示图片
        cv2.imshow('Image', img)
        while True:
            # 等待按键输入
            key = cv2.waitKey(0)
            # 判断是否按下了 'd' 键
            if key == ord('d'):
                # 删除图片文件
                os.remove(os.path.join(play_folder, file_name))
                print(f'Deleted file {file_name}.')
                break
            # 判断是否按下了 'y' 键
            elif key == ord('y'):
                break
        # 关闭显示窗口
        cv2.destroyAllWindows()
