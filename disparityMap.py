import numpy as np
import cv2
import calibration

DEPTH_VISUALIZATION_SCALE = 2048

# Open both cameras
cap_right = cv2.VideoCapture(0)                    
cap_left =  cv2.VideoCapture(1)

win_size = 3
# stereo = cv2.StereoSGBM_create(
# minDisparity=20,
# numDisparities=120,
# blockSize=7,
# uniquenessRatio=10,
# speckleWindowSize=3,
# speckleRange=1,
# P1=8 * 3 * win_size ** 2,
# P2=32 * 3 * win_size ** 2,
# )

# stereo = cv2.StereoBM_create()

# while(cap_right.isOpened() and cap_left.isOpened()):

#     succes_right, frame_right = cap_right.read()
#     succes_left, frame_left = cap_left.read()

#     # Undistort and rectify images
#     frame_right = cv2.cvtColor(cv2.remap(frame_right, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0), cv2.COLOR_BGR2GRAY)
#     frame_left = cv2.cvtColor(cv2.remap(frame_left, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0), cv2.COLOR_BGR2GRAY)

#     cv2.imwrite('left.png', frame_left)
#     cv2.imwrite('right.png', frame_right)                     
    
#     disparity = stereo.compute(frame_left, frame_right)
#     disparity = cv2.normalize(disparity, None, alpha = 0, beta = 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

#     # Show the frames
#     cv2.imshow("frame right", frame_right) 
#     cv2.imshow("frame left", frame_left)
#     cv2.imshow("disparity", disparity)


#     # Hit "q" to close the window
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# Matched block size. It must be an odd number >=1 . Normally, it should be somewhere in the 3..11 range.
block_size = 3
min_disp = 0
max_disp = 128
# Maximum disparity minus minimum disparity. The value is always greater than zero.
# In the current implementation, this parameter must be divisible by 16.
num_disp = max_disp - min_disp
# Margin in percentage by which the best (minimum) computed cost function value should "win" the second best value to consider the found match correct.
# Normally, a value within the 5-15 range is good enough
uniquenessRatio = 10
# Maximum size of smooth disparity regions to consider their noise speckles and invalidate.
# Set it to 0 to disable speckle filtering. Otherwise, set it somewhere in the 50-200 range.
speckleWindowSize = 0
# Maximum disparity variation within each connected component.
# If you do speckle filtering, set the parameter to a positive value, it will be implicitly multiplied by 16.
# Normally, 1 or 2 is good enough.
speckleRange = 2
disp12MaxDiff = 0


stereo = cv2.StereoSGBM_create(
    minDisparity=min_disp,
    numDisparities=num_disp,
    blockSize=block_size,
    uniquenessRatio=uniquenessRatio,
    speckleWindowSize=speckleWindowSize,
    speckleRange=speckleRange,
    disp12MaxDiff=disp12MaxDiff,
    P1=8 * 1 * block_size * block_size,
    P2=32 * 1 * block_size * block_size,
)
while True:
    succes_right, frame_right = cap_right.read()
    succes_left, frame_left = cap_left.read()

    # Undistorting and rectifying images based on stereoMap.xml
    frame_right, frame_left = calibration.undistortRectify(frame_right, frame_left)

    # Converting images into grayscale
    frame_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)
    frame_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)

    disparity_SGBM = stereo.compute(frame_left, frame_right)

    # Normalize the values to a range from 0..255 for a grayscale image
    disparity_SGBM = cv2.normalize(disparity_SGBM, disparity_SGBM, alpha=255,
                                  beta=0, norm_type=cv2.NORM_MINMAX)
    disparity_SGBM = np.uint8(disparity_SGBM)
    cv2.imwrite('left.png', frame_left)
    cv2.imwrite('right.png', frame_right)  
    cv2.imshow("frame right", frame_right) 
    cv2.imshow("frame left", frame_left)
    cv2.imshow("Disparity", disparity_SGBM)
    cv2.imwrite("disparity_SGBM_norm.png", disparity_SGBM)
    #     # Hit "q" to close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# # Release and destroy all windows before termination
cap_right.release()
cap_left.release()

cv2.destroyAllWindows()