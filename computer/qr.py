import cv2

# QR
import pyzbar.pyzbar as pyzbar
from pyzbar.pyzbar import ZBarSymbol

import numpy as np

# have to edit this file, remove convex hull code for tracking angle to work
# pyzbar.__file__

class QRTracker(object):
    def __init__(self):
        pass
    
    def start_camera(self, cam_index=1):
        self.cap = cv2.VideoCapture(cam_index)

    def stop_camera(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def snap_and_track(self):
        ret, img = self.cap.read()
        return self.track(img)

    def display(self, img):
        cv2.imshow("Results", img)
        cv2.waitKey(1)

    def track(self, img):
        decodedObjects = []

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (0,0), fx=0.6, fy=0.6)
        decodedObjects = pyzbar.decode(img, symbols=[ZBarSymbol.QRCODE])
        
        # Loop over all decoded objects
        points = []
        
        for decodedObject in decodedObjects: 
            points = decodedObject.polygon
    
        # If the points do not form a quad, find convex hull
        hull = points
        
        # Number of points in the convex hull
        n = len(hull)
        
        if n == 0:
            return img, -1, -1, -1, False
    
        # Draw the convext hull
        for j in range(0,n):
            cv2.line(img, hull[j], hull[ (j+1) % n], (255,0,0), 3)
            
        # center
        cx = 0
        cy = 0
        
        # angle
        angle = np.arctan2(hull[0][1] - hull[1][1], hull[0][0] - hull[1][0])
        angle -= np.pi/2
        
        for i in range(n):
            cx += hull[i][0]
            cy += hull[i][1]
            
        cx /= float(n)
        cy /= float(n)
        
        cv2.circle(img, (int(cx), int(cy)), 5, color=(255,255,255), thickness=2)
        cv2.circle(img, (int(cx + np.cos(angle) * 50), int(cy + np.sin(angle) * 50)), 5, color=(255,255,255), thickness=2)
        
        cv2.putText(img,'{}, {}'.format(cx, cy), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
        return img, cx, cy, angle, True
