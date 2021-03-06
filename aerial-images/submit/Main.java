import java.awt.Graphics;
import java.awt.List;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Scanner;

import javax.imageio.ImageIO;

public class Main {
	
	
	public static String buildRequest(String cp, String md){
		
		String url = 
				"http://dev.virtualearth.net/REST/V1/Imagery/Map/aerial";
		
		
		//parameters to add
		String format = "format=jpeg";
		String key = "&key=AmpMl2ATcsLwygMGOAJ3CqIAUVv2rtQp9x7J3RDu0mddr5adKBH8oGfcr9PMLV4v";
		String metaData = "&mapMetadata="+md;
		String zl = "/19";
		String center = "/";
		center += cp;

		//requests for the boxes
		Request dataRequest0 = new Request(url);
		dataRequest0.add(center);
		dataRequest0.add(zl);
		dataRequest0.add("?");
		dataRequest0.add(format);
		dataRequest0.add(metaData);
		dataRequest0.add(key);
		
		//creating the actual request and getting data
		return dataRequest0.getString();
	}
	
	public static double[] makeBoundBox(double lat1, double long1, double lat2, double long2){
		
		double[] boundBox0 = new double[4];
		boundBox0[0] = lat1;
		boundBox0[1] = long1;
		boundBox0[2] = lat2;
		boundBox0[3] = long2;
		
		return boundBox0;
	}
	
	
	
	
	
	
	
	

	public static void main(String[] args) {
		
		// array to hold the coordinates
		int numberCoords = 4;
		double[] boundBox = new double[4];
		
		
				if(args.length > 0){
			if(args.length < 4){
				System.err.println("not correct number of arguments");
				return;
			}
			
			double args0 = Double.parseDouble(args[0]);
			double args1 = Double.parseDouble(args[1]);
			double args2 = Double.parseDouble(args[2]);
			double args3 = Double.parseDouble(args[3]);
			
			boundBox[0] = args0; //southwest
			boundBox[1] = args1;
			boundBox[2] = args2; //northeast 42.7125
			boundBox[3] = args3;
		}else{
		
		
		System.out.println("Enter the four coordinate for the bounding box: \n");
		//ask user for the bounding box
		for(int i = 0; i < numberCoords; i++){
			
			//getting user input
			Scanner reader = new Scanner(System.in);  // Reading from System.in
			
			if(i < 2){
				if(i==0)
					System.out.println("lat1: ");
				if(i==1)
					System.out.println("long1: ");
			}else{
				if(i==2)
					System.out.println("lat2: ");
				if(i==3)
					System.out.println("long2: ");
			}
			boundBox[i] = reader.nextInt(); 
		}
		
	      }
		
		
		
		
		// random bounding box coordinates
		//South Latitude, West Longitude, North Latitude, East Longitude
		// 45.219,-122.325,47.610,-122.107
		boundBox[0] = 42.712439; //southwest
		boundBox[1] = -71.693370;
		boundBox[2] = 42.712439; //northeast 42.7125
		boundBox[3] = -71.693370;
		
		
		
		
		AerialData aData = null;
		double currentLat;
		double currentLong;
		double[] currentCenter = new double[]{boundBox[0], boundBox[1]};
		String centerString;
		String data;
		String image;
		
		// get all of the images and put in a 2D array
		ArrayList<ArrayList<BufferedImage>> listOfListImages = new ArrayList<ArrayList<BufferedImage>>(); 
		
		while(currentCenter[0] <= boundBox[2]){
			
			// resetting the current long
			currentCenter[1] = boundBox[1];
			
			// the row we will add images to
			ArrayList<BufferedImage> currentRow = new ArrayList<BufferedImage>(); 
			
			while(currentCenter[1] <= boundBox[3]){
				
				// this is the start point
				centerString = currentCenter[0] + "," + currentCenter[1];
				
				// build request for image
				data = buildRequest(centerString,"1");
				image = buildRequest(centerString,"0");
				
				// creating the image
				aData = new AerialData(data);
				AerialImage aImage = new AerialImage(image);
				
				//adding the new image to the list
				currentRow.add(aImage.getImage());
				
				// incrementing the longitude
				currentCenter[1] = aData.getNextLong();
			}
			
			if(aData == null){
			// incrementing the longitude
			System.err.println("there is not image in those bounds");
			break;
			}
			
			currentCenter[0] = aData.getNextLat();
			listOfListImages.add(currentRow);
		}
		
		//could to checking to make sure all columns are same number
		
		// number of pixels in image is 350
		int numberPixelsImage = 350;
		
		//add all the images togethere
		// width is the number of column * 350
		int width = listOfListImages.get(0).size() * 350;
		//height is the number of rows * 350
		int height = listOfListImages.size() * 350;
		
		// the new image that we will layer
		BufferedImage combined = new BufferedImage(width, height, listOfListImages.get(0).get(0).getType());
		
		Graphics graphics = combined.getGraphics();
		
		int yIndex = 0;
		int yCounter = 0;
		
		for(int j = listOfListImages.size() - 1; j > -1; --j){
			
			for(int i = 0; i < listOfListImages.get(j).size(); ++i){
				
			int xIndex = i * 350;
			// loop through adding the images to the finalImage
			graphics.drawImage(listOfListImages.get(j).get(i), xIndex, yIndex, null);

			}
			
			yCounter++;
			yIndex = yCounter * 350;
			
		}
		
		// saving the final image
		try {
			ImageIO.write(combined, "jpg", new File("combined.jpeg"));
		} catch (IOException e) {
				System.err.println("could not save image");
				e.printStackTrace();
		}
			
	}
	


}





