import cv2
import math

bx = 530
by = 300

ball_x = []
ball_y = []

video = cv2.VideoCapture('bb3.mp4')

camera,frames = video.read()

tracker = cv2.TrackerCSRT_create()

roi = cv2.selectROI("Tracking", frames, False)

tracker.init(frames,roi)

# print(roi) 

def drawing(frames, roi):
    x, y, w, h = int(roi[0]), int(roi[1]), int(roi[2]), int(roi[3])

    cv2.rectangle(frames, (x,y), ((x+w), (y+h)), (255,0,0), 3)

    cv2.putText(frames, "Tracking", (75,90), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,255), 3)


def tracking(frames, roi):
    x, y, w, h = int(roi[0]), int(roi[1]), int(roi[2]), int(roi[3])

    center1 = x + int(w/2)
    center2 = y + int(h/2)

    cv2.circle(frames, (center1, center2), 2, (0,255,0), 5)

    cv2.circle(frames, (bx,by), 2, (0,255,0), 5)

    distance = math.sqrt(((center1-bx)**2) + ((center2-by)**2))

    if(distance<=20):
        cv2.putText(frames, "Goal", (175,90), cv2.FONT_HERSHEY_COMPLEX, 1, (255,34,255), 3)

    ball_x.append(center1)
    ball_y.append(center2)

    for i in range(len(ball_x)-1):
     cv2.circle(frames, (ball_x[i], ball_y[i]), 2, (0,255,0), 5)


while True:
    
    check, img = video.read()   

    # Update the tracker on the img and the bounding box
    success, bbox = tracker.update(img)

    if success:
        drawing(img, bbox)
    else:
        cv2.putText(img,"Lost",(75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

    tracking(img, roi)

    cv2.imshow("result", img)
            
    key = cv2.waitKey(25)
    if key == 32:
        print("Stopped")
        break

video.release()
cv2.destroyALLwindows()