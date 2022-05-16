import time
import cv2
import snake
import video_capture
import mvsdk
import numpy as np

Video = video_capture.Video_capture(0, 960, 600)
snake_ = snake.Snake(Video.COLS)
# time_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
# sfourcc = cv2.VideoWriter_fourcc(*'XVID')#视频存储的格式
# out = cv2.VideoWriter('./video/' + time_name + '.avi', sfourcc, 60, (Video.COLS, Video.ROWS))#视频存储

# cap = cv2.VideoCapture(0)
# snake_ = snake.Snake()
while True:
    # 获取相机图像
    pRawData, FrameHead = mvsdk.CameraGetImageBuffer(Video.hCamera, 200)
    mvsdk.CameraImageProcess(Video.hCamera, pRawData, Video.pFrameBuffer, FrameHead)
    mvsdk.CameraReleaseImageBuffer(Video.hCamera, pRawData)
    frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(Video.pFrameBuffer)
    frame = np.frombuffer(frame_data, dtype=np.uint8)
    frame = frame.reshape((FrameHead.iHeight, FrameHead.iWidth, 1 if FrameHead.uiMediaType == mvsdk.CAMERA_MEDIA_TYPE_MONO8 else 3) )
    
    frame = cv2.flip(frame, 1) 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (int(Video.COLS / 3), int(Video.ROWS / 3)))
    ret, conrners = cv2.findChessboardCorners(gray, (3, 3))
    center = [0, 0]
    if ret == True:
        for i in range(0, len(conrners)):
            # cv2.circle(frame, (int(conrners[i][0][0]), int(conrners[i][0][1])), 5, (0, 0, 255), -1)
            center[0] += int(conrners[i][0][0]) * 3
            center[1] += int(conrners[i][0][1]) * 3
        center[0] = int(center[0] / len(conrners))
        center[1] = int(center[1] / len(conrners))
        # cv2.circle(frame, center, 20, (0, 255, 255), -1)
        snake_.head_coordinate(frame, center)
    if snake_.game == 1:
        cv2.putText(frame, "Game Over", (150, 300), cv2.FONT_HERSHEY_COMPLEX, 5, (0, 0, 255), 12)
        # out.write(frame)
        cv2.imshow("src_img", frame)
        cv2.waitKey(0)
        # out.release()
        print("手动退出")
        exit()

    # out.write(frame)
    # 显示结果
    cv2.imshow("src_img", frame)
    if cv2.waitKey(1) == 'q':
        # out.release()
        print("手动退出")
        break

    
