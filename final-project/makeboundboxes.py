import csv

boxes = []
latlons = []
with open('drive.traj') as drivefile:
    for row in csv.reader(drivefile):
        lat = float(row[0].split(' ')[0])
        lon = float(row[0].split(' ')[1])
        latlons.append((lat, lon))

widthleft = .0003
widthright = .00002

lastlat = None
lastlon = None

neqct = 0

for ll in range(len(latlons)):
    curlat = latlons[ll][0]
    curlon = latlons[ll][1]
    if ll != len(latlons) - 1:
        nextlat = latlons[ll + 1][0]
        nextlon = latlons[ll + 1][1]
    else:
        nextlat = None
        nextlon = None

    lon1 = curlon - widthleft
    lon2 = curlon + widthright

    if lastlat is not None:
        latdiffbottom = curlat - lastlat
    else:
        latdifftop = nextlat - curlat
        latdiffbottom = latdifftop

    lat1 = curlat - latdiffbottom/2


    if nextlat is not None:
        latdifftop = nextlat - curlat
    else:
        latdifftop = latdiffbottom

    lat2 = curlat + latdifftop / 2

    if latdifftop != latdiffbottom:
        neqct +=1

    boxes.append([lat1, lon1, lat2, lon2])

    lastlat = curlat
    lastlon = curlon

with open('boundboxes.txt', 'wb') as bxs:
    writer = csv.writer(bxs)
    for row in boxes:
        newstr = str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + ' ' + str(row[3])
        # print newstr
        writer.writerow([newstr])
