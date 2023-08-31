import numpy as np
import matplotlib.pyplot as plt

categories = ['car', 'bus', 'pedestrian', 'traffic cone', 'truck']
legend = ['pseudo', 'original', 'x2', 'x3', 'x5']

# 设置全局字体
# plt.rcParams['font.family'] = 'serif'
# plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
# plt.rcParams['font.size'] = 10

data_sets = [
    [0.255, 0, 0.183, 0.291, 0],  # 第一组数据
    [0.313, 0.019, 0.354, 0.309, 0.014],  # 第二组数据
    [0.322, 0.097, 0.316, 0.355, 0.036],  # 第三组数据
    [0.333, 0.191, 0.309, 0.357, 0.155],
    [0.309, 0.151, 0.242, 0.326, 0.158]
]  # 每个类别的不同数据组

# 设置颜色列表，每个类别对应一个颜色
colors = ['royalblue', 'darkorange', 'darkgrey', 'orange', 'cornflowerblue']

# 设置图的尺寸
plt.figure()  # 宽度为8英寸，高度为6英寸

# 创建子图
fig, ax = plt.subplots(figsize=(16, 6))
width = 0.15

# 为每个类别的数据点绘制柱状图
for i in range(len(categories)):
    ax.bar([x + i * width for x in range(len(data_sets[i]))], data_sets[i],
           width=width, label=legend[i], color=colors[i])

# 在柱状图上绘制水平虚线作为基线
# plt.axhline(y=20, color='gray', linestyle='dashed', linewidth=1)
# 为每个分组添加不同长度的基线
fontsize = 12
fontfamily='serif'
for i, v in enumerate(data_sets):
    ax.axhline(y=data_sets[1][i], color='gray', linestyle='dashed',
               linewidth=3, xmin=width * ((1 + i * 5) / 4) + 0.01,
               xmax=width * ((1 + i * 5) / 4 + 1) + 0.01)
    ax.text(i, data_sets[1][i] + 0.01, str(data_sets[1][i]),
            ha='center', va='center', fontsize=fontsize,fontfamily=fontfamily, color='black')

# 隐藏坐标轴边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# ax.spines['bottom'].set_visible(False)
# ax.spines['left'].set_visible(False)

# 添加标题和标签
# plt.title('Sample Bar Chart for Tech Paper')
plt.xlabel('categories', fontsize=14, fontfamily='Times New Roman')
plt.ylabel('AP', fontsize=14, fontfamily='Times New Roman')

# 添加图例
plt.legend()

# 设置x轴刻度
ax.set_xticks([x + width * 2 for x in range(len(data_sets[0]))])
ax.set_xticklabels(categories, fontsize=14, fontfamily='monospace')

# 移动图例到右上角
ax.legend(loc='upper right', fontsize=14)

# 显示图像
plt.show()
