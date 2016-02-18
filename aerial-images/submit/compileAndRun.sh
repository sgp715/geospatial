#!/bin/bash

javac -cp "./json-20160212.jar" AerialData.java AerialImage.java Request.java Main.java

java -cp .:./json-20160212.jar Main

