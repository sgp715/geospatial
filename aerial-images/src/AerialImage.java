import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;

import javax.imageio.ImageIO;

public class AerialImage {
	
	private URL realURL;
	private BufferedImage bufferedImage;
	
	public AerialImage (String url){
		
		try {
			
			//creating the URL 
			URL realURL = new URL(url);
			
			// saving the image
			bufferedImage = ImageIO.read(realURL);
		    
		} catch (MalformedURLException e) {
			System.err.println("could not create the image URL: " + e);
		} catch (IOException e) {
			System.err.println("could not read in the file from URL: " + e);
		}
		
	}
	
	public void saveImage(int number){
		
		// writing the file
		File outputfile = new File("aerial-image" + number + ".jpg");
		
		
		try {
			ImageIO.write(bufferedImage, "jpg", outputfile);
		} catch (Exception e) {
			System.err.println("could not create image: " + e);
		}
		
	}
	
	public BufferedImage getImage(){
		return bufferedImage;
	}

}
