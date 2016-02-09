function duetsch = getGermany(latdata, longdata)

%https://www.mathworks.com/matlabcentral/newsreader/view_thread/163724
%^^ border data

%output will be map
%duetsch = worldmap('Germany');
duetsch = worldmap(...
    [min(latdata),max(latdata)],[min(longdata),max(longdata)]...
    );
land = shaperead('landareas.shp', 'UseGeoCoords', true);
geoshow(land, 'FaceColor', [0.15 0.5 0.15])
cities = shaperead('worldcities', 'UseGeoCoords', true);
geoshow(cities, 'Marker', '.', 'Color', 'red')

%adding data
plotm(latdata,longdata)

                       

                       
                       
                       
                       
                       
                       