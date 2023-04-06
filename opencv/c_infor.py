import cv2

cap = cv2.VideoCapture(1)  # 打开默认相机

while True:
    ret, frame = cap.read()  # 读取一帧图像

    if not ret:  # 如果没有读取到图像，则退出循环
        break
    frame = cv2.rotate(frame, cv2.ROTATE_180)  # 旋转图片

    # 在图像上添加文本
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Resolution: {}x{}".format(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                                  int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))),
                (10, 30), font, 1, (0, 255, 0), 2)
    cv2.putText(frame, "FPS: {}".format(int(cap.get(cv2.CAP_PROP_FPS))), (10, 60), font, 1, (0, 255, 0), 2)

    # 显示图像窗口
    cv2.imshow('camera', frame)

    # 按下't'键保存图像
    if cv2.waitKey(1) == ord('t'):
        cv2.imwrite('camera_image.png', frame)

    # 按下'q'键退出程序
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()  # 释放相机资源
cv2.destroyAllWindows()  # 关闭��有窗口
