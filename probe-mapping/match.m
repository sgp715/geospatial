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

lat = probepoints{1,4};
long = probepoints{1,5};

g = getGermany(lat,long);

