import requests
import os

# 下载链接
url = "http://region-3.seetacloud.com:58762/jupyter/files/autodl-pub/nuScenes/Fulldatasetv1.0/Trainval/v1.0-trainval03_blobs.tgz?_xsrf=2%7Cc4b77ecb%7C44cb48063d871ded000f58d156788451%7C1679896006"

# 下载文件名
filename = "v1.0-trainval03_blobs.tgz"

# 下载文件路径
path = "./"

# 如果文件已存在，删除它
if os.path.exists(os.path.join(path, filename)):
    os.remove(os.path.join(path, filename))

# 开始下载
r = requests.get(url, stream=True)

# 获取文件总大小
total_size = int(r.headers.get('Content-Length', 0))
block_size = 1024 # 1 Kibibyte

# 开始下载，同时检查下载是否中断
with open(os.path.join(path, filename), 'wb') as f:
    for data in r.iter_content(block_size):
        f.write(data)
        # 检查下载是否中断
        if total_size > 0 and f.tell() > total_size:
            print("下载中断，正在继续下载...")
            r = requests.get(url, stream=True, headers={'Range': 'bytes=%d-' % f.tell()})
            for data in r.iter_content(block_size):
                f.write(data)

print("下载完成！")
