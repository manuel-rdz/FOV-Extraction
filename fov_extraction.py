import cv2
import os
import numpy as np
import shutil

def calculate_edges(img):
    red = img[:,:,-1]

    h_line = red.shape[0] // 2

    s_h = red[h_line,:]

    t = max(s_h) * 0.06

    x1, x2 = -1, -1

    for idx, v in enumerate(s_h):
        if v > t:
            x1 = idx
            break
    
    for idx in range(len(s_h) - 1, -1, -1):
        if s_h[idx] > t:
            x2 = idx
            break

    return x1, x2

def crop_background(img_path, output_path):
    img = cv2.imread(img_path)
    c_p = [0]*4
    c_p[0], c_p[1] = calculate_edges(img)
    c_p[2], c_p[3] = calculate_edges(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))

    mod = False
    idxs = []
    for idx, v in enumerate(c_p):
        nv = -1
        if v == -1 and (idx == 0 or idx == 2):
            nv = 0
        if v == -1 and idx == 1:
            nv = img.shape[1]
        if v == -1 and idx == 3:
            nv = img.shape[0]

        if nv != -1:
            c_p[idx] = nv
            mod = True
            idxs.append(idx)
    
    if mod:
        print(img.shape, img_path, idxs)

    roi = img[c_p[2]:c_p[3], c_p[0]:c_p[1], :]
    cv2.imwrite(output_path, roi)
