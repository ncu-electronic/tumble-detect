import cv2

# initialize the camera
cam = cv2.VideoCapture(0)
ret, image = cam.read()

if ret:
    cv2.imshow('SnapshotTest',image)
    cv2.waitKey(0)
    cv2.destroyWindow('SnapshotTest')
    cv2.imwrite('/home/pi/book/output/SnapshotTest.jpg',image)
cam.release()
