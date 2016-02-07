
%asking what direcotry we are in to come back to later
start_dir = pwd;

%asking where the images are
folder_name = uigetdir;
cd(folder_name);

%get the files and put in matrix
imagefiles = dir('*.jpg');      
nfiles = length(imagefiles);    

%changing back to original directory
cd(start_dir);

%add the folder with functions to path
addpath(start_dir, folder_name, 'MatlabFns/Spatial');

%random number for testing
e = 75;

for ii=1:e
    
   %read in the indexed image
   currentfilename = imagefiles(ii).name;
   currentimage = imread(currentfilename); 
   
   %apply the segmentation
   currentimage = onepic(currentimage);
   
   %add the images continually to previous ones
   if(ii == 1)
       totalimage = currentimage;
   elseif(ii > 1)
        totalimage = totalimage + currentimage;
   end
   
end

% if the it was there enough of the time keep it
thresh = max(totalimage) * 0.9;

for idx = 1:numel(totalimage)
    if(totalimage(idx) < thresh)
        totalimage(idx) = 0;
    end
end


figure;
imshow(totalimage);
pause(0.5);

%check that we are not printing something that is the size of the screen
[ilength, iwidth] = size(totalimage);
totalimage = filterregionproperties(totalimage, {'Area', @lt, (iwidth * ilength)/4}, {'Orientation', @lt, 0});
totalimage = filterregionproperties(totalimage, {'Area', @gt, 40}, {'Orientation', @lt, 0});

figure;
imshow(totalimage);