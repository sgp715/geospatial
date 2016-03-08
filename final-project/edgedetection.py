# to call from command line: python edgedetection.py
# writes to linesandcircleedges.jpg with the lines found and the end points of each line circled
# prints a dictionary with lists of 2-element lists of tuple coords
# you may need to take out this import to run on your machine
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import numpy as np
import cv2
import math
import csv
from sys import argv
from geopy.distance import vincenty

latlon_list = []

threshwronglist = []
thresholds = []

finalcoords = {}
finalcoords['leftmost'] = []
finalcoords['rightmost'] = []
finalcoords['secondtoleft'] = []
finalcoords['secondtoright'] = []
finalcoords['midl'] = []
finalcoords['midr'] = []

with open("boundboxes.txt") as file1:
    reader = csv.reader(file1)
    for row in reader:
        # print row[0].split(' ')
        latlon_list.append(row[0].split(' '))
    wronglist = []

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
        output['Pixel Slopes'] = []
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

            if len(pixelcoords) == 2:
                if pixelcoords[0][0] > pixelcoords[1][0] :
                    pixelcoords = [pixelcoords[1], pixelcoords[0]]
                    latloncoords = [latloncoords[1], latloncoords[0]]
                output['Pixel Coordinate Endpoints'].append(pixelcoords)
                output['Lat Lon Coordinate Endpoints'].append(latloncoords)

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
                cv2.circle(img, pixelcoords[0], 10, (0,0,255))
                cv2.circle(img, pixelcoords[1], 10, (0,200,255))
                cv2.line(img,pixelcoords[0],pixelcoords[1],(0,0,255),2)

        if therecount == 4:
            goodpix = []
            goodlats = []
            avgxlist = []
            for g in range(len(gone)):
                pixelcoords = output['Pixel Coordinate Endpoints'][g]
                goodlat = output['Lat Lon Coordinate Endpoints'][g]
                if gone[g] is False:
                    goodpix.append(pixelcoords)
                    goodlats.append(goodlat)
            for px in range(len(goodpix)):
                avgx = (goodpix[px][0][0] + goodpix[px][1][0])/2
                avgxlist.append({'avgx': avgx, 'pixelcoords':goodpix[px], 'latloncoords':goodlats[px]})
            sortedavgxs = sorted(avgxlist, key=lambda k: k['avgx'])

            rightmost = sortedavgxs[3]['pixelcoords']
            secondtoright = sortedavgxs[2]['pixelcoords']
            midrpixelcoords = []
            midrpixelcoords.append(((rightmost[0][0]-secondtoright[0][0])/2 + secondtoright[0][0], rightmost[0][1]))
            midrpixelcoords.append(((rightmost[1][0]-secondtoright[1][0])/2 + secondtoright[1][0], rightmost[1][1]))

            leftmost = sortedavgxs[0]['pixelcoords']
            secondtoleft = sortedavgxs[1]['pixelcoords']
            midlpixelcoords = []
            midlpixelcoords.append(((secondtoleft[0][0]-leftmost[0][0])/2 + leftmost[0][0], leftmost[0][1]))
            midlpixelcoords.append(((secondtoleft[1][0]-leftmost[1][0])/2 + leftmost[1][0], leftmost[1][1]))

            midrlatloncoords = []
            xpercentacross0 = midrpixelcoords[0][0] / float(width)
            ypercentacross0 = midrpixelcoords[0][1] / float(height)
            lon0 = lon1 + xpercentacross0 * londiff
            lat0 = lat2 - ypercentacross0 * latdiff

            xpercentacross1 = midrpixelcoords[1][0] / float(width)
            ypercentacross1 = midrpixelcoords[1][1] / float(height)
            lon1 = lon1 + xpercentacross1 * londiff
            lat1 = lat2 - ypercentacross0 * latdiff

            midrlatloncoords = [(lat0, lon0),(lat1, lon1)]

            midllatloncoords = []
            xpercentacross0 = midlpixelcoords[0][0] / float(width)
            ypercentacross0 = midlpixelcoords[0][1] / float(height)
            lon0 = lon1 + xpercentacross0 * londiff
            lat0 = lat2 - ypercentacross0 * latdiff

            xpercentacross1 = midlpixelcoords[1][0] / float(width)
            ypercentacross1 = midlpixelcoords[1][1] / float(height)
            lon1 = lon1 + xpercentacross1 * londiff
            lat1 = lat2 - ypercentacross0 * latdiff

            midllatloncoords = [(lat0, lon0),(lat1, lon1)]

            finalcoords['leftmost'].extend(avgxlist[0]['latloncoords'])
            finalcoords['rightmost'].extend(avgxlist[3]['latloncoords'])
            finalcoords['secondtoleft'].extend(avgxlist[1]['latloncoords'])
            finalcoords['secondtoright'].extend(avgxlist[2]['latloncoords'])
            finalcoords['midl'].extend(midllatloncoords)
            finalcoords['midr'].extend(midrlatloncoords)

            cv2.line(img,rightmost[0],rightmost[1],(255,255,255),2)
            # cv2.line(img,midlpixelcoords[0],midlpixelcoords[1],(,0,255),2)
            cv2.imwrite('bigoutput/linesandcircleedges' + str(choice) + '.jpg',img)
            fourcount += 1
            break
    threshwronglist.append(len(wronglist))

with open('finaloutput.csv', 'wb') as outputfile:
    writer = csv.writer(outputfile)
    writer.writerow(['SBrightlanelat', 'SBrightlanelon', 'SBmiddlelanelat', 'SBmiddlelanelon', 'SBleftlanelat', 'SBleftlanelon', 'NBleftlanelat', 'NBleftlanelon', 'NBmiddlelanelat', 'NBmiddlelanelon', 'NBrightlanelat', 'NBrightlanelon'])
    for i in range(len(finalcoords['leftmost'])):
        lmlat = str(finalcoords['leftmost'][i][0])
        lmlon = str(finalcoords['leftmost'][i][1])
        rmlat = str(finalcoords['rightmost'][i][0])
        rmlon = str(finalcoords['rightmost'][i][1])
        scndllat = str(finalcoords['secondtoleft'][i][0])
        scndllon = str(finalcoords['secondtoleft'][i][1])
        scndrlat = str(finalcoords['secondtoright'][i][0])
        scndrlon = str(finalcoords['secondtoright'][i][1])
        midllat = str(finalcoords['midl'][i][0])
        midllon = str(finalcoords['midl'][i][1])
        midrlat = str(finalcoords['midr'][i][0])
        midrlon = str(finalcoords['midr'][i][1])
        writer.writerow([lmlat, lmlon, midllat, midllon, scndllat, scndllon, scndrlat, scndrlon, midrlat, midrlon, rmlat, rmlon])
