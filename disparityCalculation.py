from ast import arg
from dis import dis
import numpy as np
from threading import Thread
import cv2
import calibration
import time
from ctypes import *
import os
import sys

B = 9               #Distance between the cameras [cm]
f = 8              #Camera lense's focal length [mm]
alpha = 56.6        #Camera field of view in the horisontal plane [degrees]
NUM_THREADS = 4

def calc_disp(img1, img2, block_size, max_disp):

    # CONVERT FOCAL LENGTH f FROM [mm] TO [pixel]:
    height_right, width_right = img2.shape
    height_left, width_left = img1.shape

    baseline = 9 # [cm] distance between cameras

    if width_right == width_left:
        f_pixel = (width_right * 0.5) / np.tan(alpha * 0.5 * np.pi/180)

    else:
        print('Left and right camera frames do not have the same pixel width')

    mat_l = img1 # left img
    mat_r = img2 # right img

    rows = mat_r.shape[0]
    cols = mat_r.shape[1]

    disp_map = np.empty(shape=(mat_r.shape), dtype=np.uint32)

    # print(f'Size of element in python {sys.getsizeof(disp_map[0, 0])}')
    # print(f'Type of element {type(mat_r[0, 0])}')

    # C part
    libCalc = CDLL(os.path.abspath("disparity_calc.so"))
    libCalc.disp_calc_job.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_int,
        np.ctypeslib.ndpointer(dtype=np.uint32, shape=(mat_r.shape)),
        np.ctypeslib.ndpointer(dtype=np.uint32, shape=(mat_r.shape)),
        c_int, c_int,
        np.ctypeslib.ndpointer(dtype=np.uint32, shape=(mat_r.shape), flags='CONTIGUOUS')]
    libCalc.disp_calc_job.restype = None
    # libCalc.foo_func.restype = None                      #doctest: +SKIP
    # libCalc.foo_func.argtypes = [np.ctypeslib.ndpointer(dtype=np.double, ndim=1, flags='CONTIGUOUS'), c_int]
    # out = np.empty(15, dtype=np.double)
    # print(out)
    # libCalc.foo_func(out, len(out))
    # print(out)

    # disp_map = libCalc.disp_calc_job(rows, cols, mat_l.astype(np.uint32), mat_r.astype(np.uint32), block_size, max_disp)
    threads = []
    arguments = ()
    # Create and start threads
    for t in range(1):
        if t == 0:
            arguments = (
                t,
                rows,
                cols,
                block_size//2,
                rows//2,
                block_size//2,
                cols//2,
                mat_l.astype(np.uint32),
                mat_r.astype(np.uint32),
                block_size,
                max_disp,
                disp_map.astype(np.uint32)
            )
        elif t == 1:
            arguments = (
                t,
                rows,
                cols,
                block_size//2,
                rows//2,
                cols//2,
                cols - block_size//2,
                mat_l.astype(np.uint32),
                mat_r.astype(np.uint32),
                block_size,
                max_disp,
                disp_map.astype(np.uint32)
            )
        elif t == 2:
            arguments = (
                t,
                rows,
                cols,
                rows//2,
                rows - block_size//2,
                block_size//2,
                cols//2,
                mat_l.astype(np.uint32),
                mat_r.astype(np.uint32),
                block_size,
                max_disp,
                disp_map.astype(np.uint32)
            )
        elif t == 3:
            arguments = (
                t,
                rows,
                cols,
                rows//2,  # start row
                rows - block_size//2, # end row
                cols//2, # start col
                cols - block_size//2, # end col
                mat_l.astype(np.uint32),
                mat_r.astype(np.uint32),
                block_size,
                max_disp,
                disp_map.astype(np.uint32)
            )
        threads.append(Thread(target=libCalc.disp_calc_job, args=arguments))
        threads[t].start()
    # wait for threads to finish
    for thread in threads:
        thread.join()

    disp_map = disp_map.astype(np.uint8)
    return disp_map
    
    # block_intensity_left = np.int32(0)
    # block_intensity_right = np.int32(0)
    
    # for i in range(block_size//2, rows - block_size//2, 1):
    #     for j in range(max_disp + block_size//2, cols - block_size//2 - max_disp, 1):
    #         block_intensity_left = np.int32(np.sum(mat_l[i-block_size//2:i+block_size//2+1, j-block_size//2:j+block_size//2+1]))
    #         best_match = block_intensity_left
    #         disp_px = 0 # disparity in pixels
    #         difference = 0
    #         for k in range(1, max_disp+1):
    #             # compute SAD
    #             block_intensity_right = np.int32(np.sum(mat_r[i-block_size//2:i+block_size//2+1, j-block_size//2-k:j+block_size//2-k+1]))
    #             # print(f'left: {block_intensity_left} \n right: {block_intensity_right}')
    #             difference = abs(np.int32(block_intensity_left - block_intensity_right))
    #             if difference < best_match:
    #                 best_match = difference
    #                 disp_px = k

    #         # if disp_px != 0:
    #         #     zDepth = (baseline*f_pixel)/disp_px             #Depth in [cm]
    #         # else:
    #         #     zDepth = 0
    #         # # print(zDepth)

    #         # convert to 0 255 range
    #         disp_map[i-block_size//2:(i+block_size//2)+1, j-block_size//2:(j+block_size//2)+1] = np.uint8(disp_px/max_disp * 255)
    # return disp_map.astype(np.uint8)

def main():
    img_right =  cv2.imread('test_images/right/imageR0.png')
    img_left = cv2.imread('test_images/left/imageL0.png')

    img_right, img_left = calibration.undistortRectify(img_right, img_left)

    img_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)
    img_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
  
    start = time.time()
    disp_map = calc_disp(img_right, img_left, 3, 128)
    end = time.time()
    print(f'Total execution time {end - start} s')
    # disp_map = cv2.normalize(disp_map, disp_map, alpha=255, beta=0, norm_type=cv2.NORM_MINMAX)
    # print(disp_map.shape)
    # print(type(disp_map))
    # print(disp_map)
    cv2.imwrite("disparity.png", disp_map)
    cv2.imshow("result", disp_map)
    cv2.imshow("left", img_left)
    cv2.imshow("right", img_right)
    cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        pass

if __name__ == "__main__":
    main()