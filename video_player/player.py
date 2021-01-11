import numpy as np
import cv2


def play(file_list):

    caps = [cv2.VideoCapture(file) for file in file_list]

    frames = [None] * len(file_list)
    ret = [None] * len(file_list)

    while True:

        for i, cap in enumerate(caps):
            if cap is not None:
                ret[i], frames[i] = cap.read()
                frames[i] = cv2.resize(frames[i], (360, 240))

        for i, frame in enumerate(frames):
            if ret[i] is True:
                cv2.imshow(file_list[i], frame)

        if cv2.waitKey(1) and 0xFF == ord('q'):
            break

    for cap in caps:
        if cap is not None:
            cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    files = [
        'C:/Videos/2020.07.25_12.19.09_i_have_cookies.mp4',
        'C:/Videos/2020.07.25_12.40.51_jillikins.mp4'
    ]
    play(files)
