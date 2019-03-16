import cv2
import numpy as np
import pyautogui

device= cv2.VideoCapture(0)
#device.set(3,800)
#device.set(4,800)

print("Width: "+str(device.get(3)))
print("Height: "+str(device.get(4)))
direction_X=""
direction_Y=""
prev="Hey"

while True:
    ret,frame=device.read()

    #To avoid mirroring
    frame = cv2.flip(frame, 1)

    #To draw divisions on the frames
    cv2.line(frame,(int(device.get(3)/3),0),(int(device.get(3)/3),int(device.get(4))),(0,0,255))
    cv2.line(frame, (int((2*device.get(3)) / 3), 0), (int((2*device.get(3)) / 3), int(device.get(4))), (0,0, 255))
    cv2.line(frame, (int(device.get(3)/3),int(device.get(4) / 3)), ((2*int(device.get(3)/3)),int(device.get(4) / 3) ), (0,0, 255))
    cv2.line(frame, (int(device.get(3)/3), int((2*device.get(4)) / 3)), ((2*int(device.get(3)/3)), int((2*device.get(4)) / 3)), (0,0, 255))

    #To define sections
    font= cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,'UP', (300,100),font,1,(0,0,255),4,cv2.LINE_AA)
    cv2.putText(frame, 'DOWN',(270, 400), font, 1, (0, 0, 255), 4, cv2.LINE_AA)
    cv2.putText(frame, 'LEFT', (60, 250), font, 1, (0, 0, 255), 4, cv2.LINE_AA)
    cv2.putText(frame, 'RIGHT', (490, 250), font, 1, (0, 0, 255), 4, cv2.LINE_AA)

    #Gaussian Blur to remove noise
    blurred_frame=cv2.GaussianBlur(frame,(5,5),0)

    #Calculate upper and lower range of HSV values
    hsv= cv2.cvtColor(blurred_frame,cv2.COLOR_BGR2HSV)
    lwr_bound_HSV= np.array([100,150,0])
    upr_bound_HSV= np.array([140,255,255])

    #Selecting object specified by HSV range
    mask = cv2.inRange(hsv,lwr_bound_HSV,upr_bound_HSV)


    #Defining contour around the selected blue object
    contours, _ = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    cnt=max(contours,key=cv2.contourArea) if contours else None
    #Calculating the centroid
    center=None
    Mts =cv2.moments(cnt)
    if Mts['m00']!=0:
        centroid_X=int(Mts['m10'] / Mts['m00'])
        centroid_Y = int(Mts['m01'] / Mts['m00'])
    else:
        centroid_X=0
        centroid_Y=0
    cv2.circle(frame, (centroid_X, centroid_Y), 7, (255, 255, 255), -1)

    #Logic
    #Checking centroid's position in various sections of the images
    #To determmine the change in direction
    print(prev)
    if centroid_X <= device.get(3)/3 :
        print("Left")
        if prev != "Left":
            prev= "Left"
            pyautogui.press('left')
    elif centroid_X >= (2*device.get(3))/3:
        print("Right")
        if prev != "Right":
            prev = "Right"
            pyautogui.press('right')
    elif centroid_Y <= device.get(4)/3:
        print("Up")
        if prev != "Up":
            prev = "Up"
            pyautogui.press('up')
    elif centroid_Y >= (2*device.get(4))/3:
        print("Down")
        if prev != "Down":
            prev = "Down"
            pyautogui.press('down')
    else:
        print ("Centre")

    #cv2.imshow("masked",mask)
    cv2.imshow("frame", frame)

    result= cv2.bitwise_and(frame,frame,mask=mask)

    if cv2.waitKey(1)==ord('x'):
        break
device.release()
cv2.destroyAllWindows()