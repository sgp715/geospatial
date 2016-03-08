#!/bin/bash

#directory to store all the images
mkdir actual-images


#iterate through input file
while read line           
do           

	#data that we got from current line
	echo "$line"           

		 #capture the first two fields from string
                lat0=$(echo "$line" | cut -f1 -d' ')
                long0=$(echo "$line" | cut -f2 -d' ')
		lat1=$(echo "$line" | cut -f3 -d' ')
		long1=$(echo "$line" | cut -f4 -d' ')


		#getting the next picture
		java -cp .:./json-20160212.jar Main $lat0 $long0 $lat1 $long1

		eog actual.jpeg &

		#give the computer a break
		sleep 3
		pkill eog
	
		#save the old image
		mv actual.jpeg actual-images/actual$count.jpeg
		
		#increment the counter
		count=$((count+1))


done < boundboxes.txt
