import cv2
import numpy as np

video=cv2.VideoCapture('multiple balls.mov')
prevCircle = [0, 0]
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2
vel = 0

while True:
    ret, frame = video.read()
    if not ret:
        break

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(grayFrame, (17,17), 0)

    circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1.2, 10, param1=100, param2=30, minRadius=1, maxRadius=4000)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        chosen = None
        for i in circles[0, :]:
            if chosen is None:
                chosen = i
        
        cv2.circle(frame, (chosen[0], chosen[1]), 1, (0, 100, 100), 3)
        cv2.circle(frame, (chosen[0], chosen[1]), chosen[2], (255, 0, 255), 3)

        # Direction
        dirr = ((chosen[0]-prevCircle[0])**2 + (chosen[1]-prevCircle[1])**2)**0.5
        dir_x = (chosen[1]-prevCircle[0])
        dir_y = (chosen[1]-prevCircle[1])
    
        # Velocity
        time_elapsed = 1 / video.get(cv2.CAP_PROP_FPS)
        prev_vel = vel
        vel = (dirr / time_elapsed / 100).round(2)

        # Acceleration
        acc = (((vel - prev_vel) / time_elapsed) / 100).round(2)

        if dir_x !=0 and dir_y !=0:
            print("Direction:", dir_x, "i", dir_y, "j")
            print("Velocity:", vel)
            print("Acceleration:", acc)
            print()

        prevCircle = chosen

    cv2.imshow("circles", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyALLWindows()
        