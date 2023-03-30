import cv2
import numpy as np

cap = cv2.VideoCapture('single ball.mov')

feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

x, y, r = 100, 100, 40

waittime = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    x_prev, y_prev = x, y
    vel = 0
    prev_vel = vel
    
    p0 = cv2.goodFeaturesToTrack(gray, mask=None, **feature_params)
    
    p1, st, err = cv2.calcOpticalFlowPyrLK(prev_gray, gray, p0, None, **lk_params)
    
    good_new = p1[st==1]
    good_old = p0[st==1]
    
    distances = np.linalg.norm(good_new - np.array([x_prev, y_prev]), axis=1)
    idx = np.argmin(distances)
    x, y = good_new[idx].ravel()
    vx, vy = good_new[idx].ravel() - good_old[idx].ravel()
    ax, ay = np.array([x, y]).ravel() - 2 * np.array([x_prev, y_prev]).ravel() + np.array([x_prev, y_prev]).ravel()
    
    cv2.circle(frame, (int(x), int(y)), r, (0, 255, 0), 2)
    
    cv2.imshow('frame', frame)
    
    prev_gray = gray.copy()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    waittime += 1
    
    if waittime % 100 == 0:

        # Direction
        dirr = ((x-x_prev)**2 + (y-y_prev)**2)**0.5
        dir_x = (x-x_prev)
        dir_y = (y-y_prev)
    
        # Velocity
        time_elapsed = 1 / cap.get(cv2.CAP_PROP_FPS)
        vel = (dirr / time_elapsed / 100).round(2)

        # Acceleration
        acc = (((vel - prev_vel) / time_elapsed) / 100).round(2)

        if dir_x !=0 and dir_y !=0:
            print("Direction:", dir_x, "i", dir_y, "j")
            print("Velocity:", vel)
            print("Acceleration:", acc)
            print()
        
cap.release()
cv2.destroyAllWindows()
