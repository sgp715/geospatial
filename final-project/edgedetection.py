# to call from command line: python edgedetection.py <lat1> <lon1> <lat2> <lon2> <path_to_image>
# writes to linesandcircleedges.jpg with the lines found and the end points of each line circled
# prints a dictionary with lists of 2-element lists of tuple coords
# you may need to take out this import to run on your machine
import sys
#sys.path.append('/usr/local/lib/python2.7/site-packages')

import numpy as np
import cv2
import math
import csv
from sys import argv
from geopy.distance import vincenty

# smaller longitude is to the left, bigger is to the right (in the eastern hemi)
# bigger lat is up, smaller is down
#lat1 = 46.395361
#lon1 = 11.296116#southwest for horizontal
 #lat1 = 46.395259
# lon1 = 11.296116 #southwest for vertical
#lat2 = 46.395362
#lon2 = 11.296171 #northeast

latlon_list = []

threshwronglist = []
thresholds = []

with open("boundboxes.txt") as file1:
    reader = csv.reader(file1)
    for row in reader:
        print row[0].split(' ')
        latlon_list.append(row[0].split(' '))
    wronglist = []
    #print threshold
    #thresholds.append(threshold)
fourcount = 0
for choice in range(len(latlon_list)):
    for threshold in np.arange(3.5,5.2,0.1):
        if choice == 0:
            path_to_image = 'actual.jpeg'
        else:
            path_to_image = str('actual' + str(choice) + ".jpeg")


        lat1 = float(latlon_list[choice][0])
        lon1 = float(latlon_list[choice][1])
        lat2 = float(latlon_list[choice][2])
        lon2 = float(latlon_list[choice][3])

        latdiff = lat2 - lat1
        londiff = lon2 - lon1

        assert (latdiff > 0), 'I thought that lat2 should always be greater than lat1'
        assert (londiff > 0), 'I thought that lon2 should always be greater than lon1'

        img = cv2.imread(path_to_image)
        height, width, chnls = img.shape
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray,250,300)

        cv2.imwrite('beforehough.jpg',edges)

        lines = cv2.HoughLines(edges,1,np.pi/180,35)

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
            slope = dy/float(dx+.00000000000000001)

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

            # assert len(pixelcoords) == 2, "somethings wrong! a line should only have two points crossing the edge of the image. and each pair of points per line hopefully isn't on the same edge"
            if len(pixelcoords) == 2:
                output['Pixel Coordinate Endpoints'].append(pixelcoords)
                output['Lat Lon Coordinate Endpoints'].append(latloncoords)

        # print len(output['Pixel Coordinate Endpoints'])

        badpairs = []
        #feet
        gone = [False for ll in output['Lat Lon Coordinate Endpoints']]

        for ll1 in range(len(output['Lat Lon Coordinate Endpoints'])):
            for ll2 in range(len(output['Lat Lon Coordinate Endpoints'])):
                if (gone[ll1] == False) & (gone[ll2] == False):
                    latlon1 = output['Lat Lon Coordinate Endpoints'][ll1]
                    latlon2 = output['Lat Lon Coordinate Endpoints'][ll2]
                    dist0 = vincenty(latlon1[0], latlon2[0]).feet
                    dist1 = vincenty(latlon1[1], latlon2[1]).feet
                    # print dist0
                    # print dist1
                    if ll1 != ll2:
                        if (dist0 + dist1) / 2 < threshold:
                            gone[ll2] = True

        therecount = 0
        for g in range(len(gone)):
            pixelcoords = output['Pixel Coordinate Endpoints'][g]
            if gone[g] is False:
                therecount +=1
                cv2.circle(img, pixelcoords[0], 10, (0,200,255))
                cv2.circle(img, pixelcoords[1], 10, (0,200,255))
                cv2.line(img,pixelcoords[0],pixelcoords[1],(0,0,255),2)

        # print "number of lines:", therecount

        if therecount != 4:
            print threshold, therecount
        else:
            cv2.imwrite('bigoutput/linesandcircleedges' + str(choice) + '.jpg',img)
            fourcount += 1
            break
            #print 'choice', choice
            #print 'tcount', therecount
        # cv2.imshow('Output',img)
        # cv2.waitKey()
        # print output
    threshwronglist.append(len(wronglist))
    # print 'lenwronglist', len(wronglist)

# print 'lenthreshwrong', len(threshwronglist)
# print 'min', np.min(threshwronglist)
print fourcount
# for i in range(len(threshwronglist)):
#     if threshwronglist[i] == min(threshwronglist):
#         print 'thresh', thresholds[i]
#         print 'numwrong', threshwronglist[i]
