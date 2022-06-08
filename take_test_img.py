import cv2
import os

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(2)


filenames = next(os.walk('test_images/right'), (None, None, []))[2]  # [] if no file
num = max([int(filename.split('.')[0].split('imageR')[1]) for filename in filenames])
print(num)

while cap.isOpened():


    succes1, img = cap.read()
    succes2, img2 = cap2.read()

    k = cv2.waitKey(5)


    if k == ord('s'): # wait for 's' key to save and exit
        num = num + 1
        cv2.imwrite('test_images/left/imageL' + str(num) + '.png', img)
        cv2.imwrite('test_images/right/imageR' + str(num) + '.png', img2)
        print("images saved!")
    if k == ord('q'):
        break


    cv2.imshow('Img 1',img)
    cv2.imshow('Img 2',img2)

# Release and destroy all windows before termination
cap.release()
cap2.release()

cv2.destroyAllWindows()