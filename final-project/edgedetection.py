# to call from command line: python edgedetection.py <lat1> <lon1> <lat2> <lon2> <path_to_image>
# writes to linesandcircleedges.jpg with the lines found and the end points of each line circled
# prints a dictionary with lists of 2-element lists of tuple coords
# you may need to take out this import to run on your machine
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import numpy as np
import cv2
import math
from sys import argv
lat1 = float(argv[1])
lon1 = float(argv[2])
lat2 = float(argv[3])
lon2 = float(argv[4])
path_to_image = argv[5]

# smaller longitude is to the left, bigger is to the right (in the eastern hemi)
# bigger lat is up, smaller is down
# lat1 = 46.395361
# lon1 = 11.296116#southwest for horizontal
# lat1 = 46.395259
# lon1 = 11.296116 #southwest for vertical
# lat2 = 46.395361
# lon2 = 11.296171 #northeast

latdiff = lat2 - lat1
londiff = lon2 - lon1

assert (latdiff >= 0), 'I thought that lat2 should always be greater than lat1'
assert (londiff >= 0), 'I thought that lon2 should always be greater than lon1'

img = cv2.imread(path_to_image)
height, width, chnls = img.shape
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray,250,300)

cv2.imwrite('beforehough.jpg',edges)

lines = cv2.HoughLines(edges,1,np.pi/180,180)

output = {}
output['Pixel Coordinate Endpoints'] = []
output['Lat Lon Coordinate Endpoints'] = []
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    dx = x2 - x1
    dy = y2 - y1
    slope = dy/float(dx)

    yatxiszero = int(y1 - slope * x1)
    yatxiswidth = int(y1 + slope * (width - x1))
    xatyiszero = int(x1 + (1/slope) * (-y1))
    xatyisheight = int(x1 + (1/slope) * (height - y1))

    pixelcoords = []
    latloncoords = []

    if ((yatxiszero > 0) & (yatxiszero < height)):
        y = yatxiszero
        x = 0
        ypercentdown = yatxiszero / float(height)
        lat = lat2 - ypercentdown * latdiff
        lon = lon1
        latloncoords.append((lat, lon))
        pixelcoords.append((x, y))

    if ((yatxiswidth > 0) & (yatxiswidth < height)):
        y = yatxiswidth
        x = width
        ypercentdown = yatxiswidth / float(height)
        lat = lat2 - ypercentdown * latdiff
        lon = lon2
        latloncoords.append((lat, lon))
        pixelcoords.append((x, y))

    if ((xatyiszero > 0) & (xatyiszero < width)):
        y = 0
        x = xatyiszero
        lat = lat2
        xpercentacross = xatyiszero / float(width)
        lon = lon1 + xpercentacross * londiff
        latloncoords.append((lat, lon))
        pixelcoords.append((x, y))

    if ((xatyisheight > 0) & (xatyisheight < width)):
        y = height
        x = xatyisheight
        lat = lat1
        xpercentacross = xatyisheight / float(width)
        lon = lon1 + xpercentacross * londiff
        latloncoords.append((lat, lon))
        pixelcoords.append((x, y))

    assert len(pixelcoords) == 2, "somethings wrong! a line should only have two points crossing the edge of the image. and each pair of points per line hopefully isn't on the same edge"

    output['Pixel Coordinate Endpoints'].append(pixelcoords)
    output['Lat Lon Coordinate Endpoints'].append(latloncoords)
    cv2.circle(img, pixelcoords[0], 50, (0,200,255))
    cv2.circle(img, pixelcoords[1], 50, (0,200,255))
    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imshow('Output',img)
cv2.imwrite('linesandcircleedges.jpg',img)
cv2.waitKey(5000)
print output
