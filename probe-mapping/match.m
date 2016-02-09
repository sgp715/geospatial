%asking what direcotry we are in to come back to later
start_dir = pwd;

%asking where the images are
folder_name = uigetdir;
cd(folder_name);

%get the files and put in matrix
data = dir('*.csv');      

%changing back to original directory
cd(start_dir);

%add the folder with functions to path
addpath(start_dir, folder_name);

%parsing data for two files

%parsing for probepoints
%sampleID, dateTime, sourceCode, latitude, longitude, altitude, speed, heading
fid0 = fopen(data(2).name, 'rt');  %the 't' is important!
probepoints = ...
    textscan(fid0,'%f %s %f %f %f %f %f %f',...
    'Delimiter',',','EndOfLine','\r\n','ReturnOnError',false','EmptyValue',0);
fclose(fid0);

%parsing for link data
%linkPVID, refNodeID, nrefNodeID, length, functionalClass, directionOfTravel, speedCategory, 
%fromRefSpeedLimit, toRefSpeedLimit, fromRefNumLanes, toRefNumLanes, multiDigitized, urban, 
%timeZone, shapeInfo, curvatureInfo, slopeInfo
fid1 = fopen(data(1).name, 'rt'); 
linkdata = ...
    textscan(fid1,'%f %f %f %f %f %c %f %f %f %f %f %c %c %f %s %s %s', ...
    'Delimiter',',','EndOfLine','\r\n','ReturnOnError',false','EmptyValue',0);
fclose(fid1);

probelat = probepoints{1,4};
probelong = probepoints{1,5};
speed = probepoints{1,7};
timeStamp = probepoints{1,2};

%linkdata
fromSpeedLimit = linkdata{1, 9};
numLanes = linkdata{1,10};
timeZone = linkdata{1,14};
shapeInfo = linkdata{1,15};


%apply map matching algorithm
%1) trajectories-set(T): longitude, latitude, speed and time stamp
%2) segment(r): longitude, latitude, road width, speed limit, two-lanes?
%3) digital-map(G): a set of segments



probeg = getGermany(probelat,probelong);
%linkg

