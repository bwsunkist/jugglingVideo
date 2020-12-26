import cv2
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import moviepy.editor as mp

if __name__ == '__main__':
    ### 設定項目
    input_video_file = "IMG_6859.mp4"
    out_audio = 'IMG_6859.mp3'
    out_video2 = 'IMG_6859_wo_audio.mp4'
    out_video3 = 'IMG_6859_w_audio.mp4'
    out_width = 1280
    out_height = 720
  
    input_video_obj = cv2.VideoCapture(input_video_file)
    input_width = int(input_video_obj.get(cv2.CAP_PROP_FRAME_WIDTH))
    input_height = int(input_video_obj.get(cv2.CAP_PROP_FRAME_HEIGHT))
    input_size = (input_width, input_height)

    num_of_frame = int(input_video_obj.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(input_video_obj.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')#動画のコーデック定義
    writer = cv2.VideoWriter(out_video2, fourcc, fps, (out_width, out_height))#動画のベース作成

    size_ratio = out_height / input_height

    for frame_num in range(num_of_frame):
        print('calc flame No.' + str(frame_num) + '/' + str(num_of_frame))
        _, frame = input_video_obj.read()
        new_frame = np.zeros((out_height, out_width, 3), np.uint8) #カラー画像なので3指定にしておく？
        
        if out_width == input_width:
            # width が同じ場合, 元の動画を一部切り抜いたみたいになる
            new_frame[0:out_height, 0:out_width] = frame
        else:
            frame = cv2.resize(frame, dsize = None, fx = size_ratio, fy = size_ratio)
            frame_height, frame_width = frame.shape[:2] #形状取得
            width_offset = int((out_width - frame_width)/2)
            new_frame[0:out_height, width_offset:(frame_width + width_offset)] = frame
        writer.write(new_frame)
    
    writer.release()
    input_video_obj.release()
