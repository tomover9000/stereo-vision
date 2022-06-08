import numpy as np
import cv2
import calibration
import time
from ctypes import *

B = 9               #Distance between the cameras [cm]
f = 8              #Camera lense's focal length [mm]
alpha = 56.6        #Camera field of view in the horisontal plane [degrees]

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


    ptr_mat_r = mat_r.ctypes.data_as(POINTER(POINTER(c_int) * rows))
    ptr_mat_l = mat_l.ctypes.data_as(POINTER(POINTER(c_int) * rows))
    # C part
    libCalc = CDLL("C:\\Users\\vladz\\OneDrive - Universitatea Politehnica Bucuresti\\Licenta\\stereo-vision-local\\disparity_calc.so")
    libCalc.disparity_calc.argtypes = [c_int, c_int, POINTER(POINTER(c_int) * rows), POINTER(POINTER(c_int) * rows), c_int, c_int]
    libCalc.disparity_calc.restype = POINTER(POINTER(c_int) * rows)
    disp_map_ptr = libCalc.disparity_calc(rows, cols, ptr_mat_l, ptr_mat_r, block_size, max_disp)
    disp_map = np.frombuffer(disp_map_ptr.contents)
    return disp_map



    # disp_map = np.ndarray(mat_r.shape).astype(np.uint8)

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
    img_right =  cv2.imread('test_images/right/imageR.png')
    img_left = cv2.imread('test_images/left/imageL.png')

    img_right, img_left = calibration.undistortRectify(img_right, img_left)

    img_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)
    img_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
  
    start = time.time()
    disp_map = calc_disp(img_right, img_left, 5, 10)
    end = time.time()
    print(f'Total execution time {end - start} s')
    # disp_map = cv2.normalize(disp_map, disp_map, alpha=255, beta=0, norm_type=cv2.NORM_MINMAX)
    # print(disp_map.shape)
    # print(type(disp_map))
    # print(disp_map)
    cv2.imshow("result", disp_map)
    cv2.imwrite("disparity.png", disp_map)
    cv2.imshow("left", img_left)
    cv2.imshow("right", img_right)
    cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        pass

if __name__ == "__main__":
    main()