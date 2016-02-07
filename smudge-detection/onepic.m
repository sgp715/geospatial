function outimg = onepic(inimg)

% set the return variable
outimg = inimg;

% make the image small (let's not thrash harddrives more)
outimg = imresize(outimg, 0.25);

% make the smudge more visible
outimg = imsharpen(outimg,'Radius',20,'Amount', 1, 'Threshold', 0);

% convert image to gray scale and invert
outimg = rgb2gray(outimg);
outimg = imcomplement(outimg);

% calculated the backgroung
back = imopen(outimg,strel('disk',15));

% subtract out background
outimg = outimg - back;

%segment image
outimg = imadjust(outimg);
outimg = im2bw(outimg, 0.2); %arbitrary
outimg = bwareaopen(outimg, 50);

% fill the holes in the bw image
outimg = imfill(outimg,'holes');
end