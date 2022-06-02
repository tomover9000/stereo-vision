import cv2

cap = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(0)


while cap.isOpened():

    succes1, img = cap.read()
    succes2, img2 = cap2.read()

    k = cv2.waitKey(5)


    if k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('test_images/left/imageL' + '.png', img)
        cv2.imwrite('test_images/right/imageR' + '.png', img2)
        print("images saved!")
        break


    cv2.imshow('Img 1',img)
    cv2.imshow('Img 2',img2)

# Release and destroy all windows before termination
cap.release()
cap2.release()

cv2.destroyAllWindows()