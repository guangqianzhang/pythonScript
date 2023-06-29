import shutil

import numpy as np
import json
import matplotlib.pyplot as plt
import cv2
try:
    import open3d as o3d
except:
    pass
import argparse
import os

label_dict = {'Deceleration_zone': 0,'Manhole_cover':1}
color_map = {0: (255, 120, 180),1: (0, 0, 255)}
line_seq = [(0, 1), (0, 3), (0, 4), (1, 2), (1, 5), (3, 2), (3, 7), (4, 5), (4, 7), (2, 6), (5, 6), (6, 7)]

coords_zero=[]
no_2d=[]


def parse_args():
    parser = argparse.ArgumentParser(description='Render')
    parser.add_argument('--updir', type=str,
                        default="/media/cqjtu/Kaixia/数据堂验收数据/20230626bad")
    parser.add_argument('--img_file', type=str,
                        default="/home/cqjtu/Documents/dataset/20230626/1682763028.151671886/1682763028.160784721.png")
    parser.add_argument('--lidar_file', type=str, default=None)
    parser.add_argument('--json_file', type=str,
                        default='/home/cqjtu/Documents/dataset/20230626/1682763028.151671886/1682763028.151671886.json')
    parser.add_argument('--calib_file', type=str, default='calibration_.json')
    parser.add_argument('--save_file', type=str, default="./asd/")

    parser.add_argument('--render_lidar_bbox', type=bool, default=False)
    parser.add_argument('--render_bbox_in_img', type=bool, default=True)
    parser.add_argument('--render_lidar_in_img', type=bool, default=True)

    args = parser.parse_args()
    return args


def load_data(img_file, lidar_file):
    sample_img = cv2.imread(img_file)
    if lidar_file is not None:
        pcd = o3d.io.read_point_cloud(lidar_file)

        points = np.array(pcd.points)
    else:
        points=None
    return sample_img, points


def load_gt_data(json_file):
    f = open(json_file, "r", encoding='utf-8')
    gt_data = json.load(f)
    return gt_data


def load_calib(calib_file):
    f = open(calib_file, "r", encoding='utf-8')
    calib = json.load(f)

    return calib


def get_corner(bbox_3d):
    center = np.array([bbox_3d["center"]["x"],
                       bbox_3d["center"]["y"],
                       bbox_3d["center"]["z"]]).reshape(1, -1)

    hlw = np.array([bbox_3d["dimensions"]["height"],
                    bbox_3d["dimensions"]["length"],
                    bbox_3d["dimensions"]["width"]]).reshape(1, -1)



    corners_norm = np.stack(np.unravel_index(np.arange(8), [2] * 3), axis=1)
    corners_norm = corners_norm[[0, 1, 3, 2, 4, 5, 7, 6]]
    corners_norm = corners_norm - np.array([0.5, 0.5, 0.5])

    corners = hlw * corners_norm



    yaw = np.pi/2+ bbox_3d["rotation"]["z"]
    rot_sin = np.sin(yaw)
    rot_cos = np.cos(yaw)
    rot_mat_T = np.array([
        [rot_cos, -rot_sin, 0],
        [rot_sin, rot_cos, 0],
        [0, 0, 1],
    ])

    corners = (rot_mat_T @ corners.T).T
    corners += center

    return corners


def get_gt_bbox(data):
    objects = data['objects']

    bboxs_2d = []
    bboxs_3d = []
    labels = []
    for object in objects:
        bbox_2d = object["box2d"]
        bbox_3d = get_corner(object["box3d"])

        label = object["label"]
        bboxs_2d.append(bbox_2d)
        bboxs_3d.append(bbox_3d)
        labels.append(label_dict[label])

    return np.stack(bboxs_2d), np.stack(bboxs_3d), np.stack(labels)


def render_lidar(lidar, bboxes, labels, save_file, xlim=(-50, 50), ylim=(-50, 50), radius=10, thickness=10):
    fig = plt.figure(figsize=(xlim[1] - xlim[0], ylim[1] - ylim[0]))

    ax = plt.gca()
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect(1)
    ax.set_axis_off()

    if lidar is not None:
        plt.scatter(
            lidar[:, 0],
            lidar[:, 1],
            s=radius,
            c="white",
        )
    if bboxes is not None and len(bboxes) > 0:
        coords = bboxes[:, [0, 3, 7, 4, 0], :2]

        for index in range(coords.shape[0]):
            plt.plot(
                coords[index, :, 0],
                coords[index, :, 1],
                linewidth=thickness,
                color=np.array(color_map[labels[index]]) / 255
            )

    save_file = os.path.join(save_file, "lidar.png")
    fig.savefig(
        save_file,
        dpi=20,
        facecolor="black",
        format="png",
        bbox_inches="tight",
        pad_inches=0,
    )
    plt.close()


def render_in_img(img, lidar,box2d, bboxes, labels, calib, save_file, name,thickness=2):
    canvas = img.copy()
    canvas = cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR)

    l2c = np.array(calib["Extrinsic"])
    intri = np.array(calib["Intrinsic"])
    intrinisic = np.eye(4)
    intrinisic[:3, :3] = intri

    if lidar is not None:
        lidar = np.concatenate((lidar, np.ones((lidar.shape[0], 1))), axis=1)
        coords = l2c @ lidar.T
        coords = intrinisic @ coords
        coords = coords.reshape(4, -1)

        indices = coords[2] > 0

        coords = coords.T[indices]
        print(len(coords))
        if len(coords)<0:
            coords_zero.append(coords)
            print('pixes do not on the C')
        coords[:, 2] = np.clip(coords[:, 2], a_min=1e-5, a_max=1e5)
        coords[:, 0] /= coords[:, 2]
        coords[:, 1] /= coords[:, 2]

        kept = (coords.T[0] > 0) & (coords.T[1] > 0) & (coords.T[0] < 1600) & (coords.T[1] < 1200)

        coords = coords[kept][:, :2].astype(np.int)

        for coord in coords:
            cv2.circle(canvas, (coord), 0, (50, 200, 180), 3)

    if bboxes is not None and len(bboxes) > 0:
        bbox = [bbox_3d[i:i + 1, :, :] for i in range(bbox_3d.shape[0])]
        for label_, box_ in zip(labels, bbox):
            coords = np.concatenate(
                [box_.reshape(-1, 3), np.ones((8, 1))], axis=-1
            )
            coords = l2c @ coords.T
            coords = intrinisic @ coords

            coords = coords.reshape(-1, 4, 8)

            indices = np.all(coords[:, 2] > 0, axis=1)
            coords = coords[indices]
            # labels = labels[indices]

            indices = np.argsort(-np.min(coords[..., 2], axis=1))
            coords = coords[indices]
            # labels = labels[indices]
            if 0 in coords.shape:
                print(f'pixes do not on the C {coords.shape}')
                coords_zero.append(name)
            else:
                coords = coords.reshape(-1, 8).T
                print(coords.shape)
                coords[:, 2] = np.clip(coords[:, 2], a_min=1e-5, a_max=1e5)
                coords[:, 0] /= coords[:, 2]
                coords[:, 1] /= coords[:, 2]

                coords = coords[..., :2].reshape(-1, 8, 2)

            try:
                box2d= box2d[0]['camera1']['coordinates']
                for key in box2d:
                    box2d[key] = int(box2d[key])

                cv2.line(
                    canvas,
                    ( (box2d['x']),  (box2d['y'])),
                    ( (box2d['width'])+  (box2d['x'])  ,box2d['height']+  box2d['y']),
                (225,225,0),
                thickness,
                cv2.LINE_AA,
                )
            except:
                no_2d.append(name)
                print(f'box2d error {name}')

            for index in range(coords.shape[0]):
                for start, end in line_seq:
                    cv2.line(
                        canvas,
                        coords[index, start].astype(np.int_),
                        coords[index, end].astype(np.int_),
                        color_map[labels[index]],
                        thickness,
                        cv2.LINE_AA,
                    )


    canvas = canvas.astype(np.uint8)
    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
    save_file = os.path.join(save_file, f"{name}.png")
    cv2.imwrite(save_file, canvas)



no_2dfilestxt='noed.txt'
if __name__ == '__main__':
    args = parse_args()

    if not os.path.exists(args.save_file):
        os.mkdir(args.save_file)
    calib = load_calib(args.calib_file)
    if os.path.isdir(args.updir):
        for parent, dirnames, filenames in os.walk(args.updir):  # 分别得到根目录，子目录和根目录下文件
            name = os.path.basename(parent)
            img_size = None
            bboxs = None
            for file_name in filenames:
                if '.json' in file_name:
                    args.json_file = os.path.join(parent, file_name)  # 获取文件全路径
                if '.png' in file_name:
                    args.img_file=os.path.join(parent, file_name)

            img, lidar = load_data(args.img_file, args.lidar_file)

            if args.json_file is not None:
                gt_data = load_gt_data(args.json_file)
                bbox_2d, bbox_3d, label = get_gt_bbox(gt_data)
            else:
                bbox_2d, bbox_3d, label = None, None, None

            if args.render_lidar_bbox:
                render_lidar(lidar, bbox_3d, label, args.save_file)

            if args.render_bbox_in_img == False:
                bbox_3d = None
            if args.render_lidar_in_img == False:
                lidar = None
            print(name)
            render_in_img(img, lidar, bbox_2d,bbox_3d, label, calib, args.save_file,name)

            f = open(no_2dfilestxt, "a")
            for line in no2dfiles:
                f.write(line + '\n')
                path = os.path.dirname(os.path.abspath(line))
                try:
                    shutil.move(path, args.updir+'/badfile')
                except:
                    print(f'bad move {path}')

