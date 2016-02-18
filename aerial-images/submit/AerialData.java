import java.awt.List;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.Iterator;

import javax.swing.text.BadLocationException;
import javax.swing.text.Document;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.json.JSONArray;
import org.json.JSONObject;
import org.xml.sax.InputSource;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.XMLReaderFactory;

public class AerialData {
	
	private URL realURL;
	private String dataString;
	private JSONObject jsonObject;
	private double[] center;
	private double[] box;
	
	public AerialData(String url){
		
		dataString = null;
		realURL = null;
		jsonObject = null;
		
			try {
				// getting the string to url
				realURL = new URL(url);
				InputStreamReader inStream = new InputStreamReader(realURL.openStream());
				
				// getting the string data
				dataString = getDataString(inStream);
				
				// getting the json object
				jsonObject = getJson(dataString);
				
			} catch (MalformedURLException e) {
				// TODO Auto-generated catch block
				System.err.println("could not get url- " + e);
			} catch (IOException e) {
				
				System.err.println(e);
			}
			
			
			// not setting the center and the box
			center = getData("center");
			box = getData("bbox");

	}
	
	public double[] getCenter(){
		return center;
	}
	
	public double[] getBox(){
		return box;
	}
	
	//always moving through image from left to right and down to up so add
	
	public double getHeight(){
		// subtracting the two latitudes
		int lat1 = 0;
		int lat2 = 2;
		return Math.abs(box[lat1] - box[lat2]);
	}
	
	public double getWidth(){
		//subtracting the two longitudes
		int long1 = 1;
		int long2 = 3;
		return Math.abs(box[long1] - box[long2]);
		
		
	}
	
	public double getNextLong(){
		//add the center longitude width 
		int centerLong = 1;
		return center[centerLong] + getWidth();
	}
	
	public double getNextLat(){
		//add the center latitude with height
		int centerLat = 0;
		return center[centerLat] + getHeight();
	}
	
	
	
	
	private JSONObject getJson(String jsonData){
		
		//creating the object from a string
		JSONObject jsonObject = new JSONObject(jsonData);
		
		return jsonObject;
		
	}
	
	private String getDataString(InputStreamReader inputStreamReader){
		
		// getting the buffer from url
		BufferedReader bufferedRead = 
				new BufferedReader(inputStreamReader);
		
		StringBuilder response = new StringBuilder();
		String inputLine;
		
        try {
			while ((inputLine = bufferedRead.readLine()) != null){
				response.append(inputLine);
			}
			
			 //closing the reader
	        bufferedRead.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        
        //getting the string
        String dataString = response.toString();
        
        return dataString;
	}
	
	
	public void printData(){
		
		if(dataString == null){
			System.err.println("no data to read inputLine is null");
			return;
		}
		
	}
	
	private double[] getData(String which){
		
		double[] returnData = null;
		
		if(jsonObject == null){
			System.err.println("jsonObject was null");
		}
		
		if(!jsonObject.has("resourceSets")){
			System.err.println("no resourseSets");
		}
		JSONArray resourceSetsArray = (JSONArray) jsonObject.get("resourceSets");
		
		if(resourceSetsArray.length()==0){
			System.err.println("no resourseSets");
		}
		JSONObject resourcesSetsObject = resourceSetsArray.getJSONObject(0);
		
		if(!resourcesSetsObject.has("resources")){
			System.err.println("no resourse");
		}
		
		JSONArray resourceArray = resourcesSetsObject.getJSONArray("resources");
		
		if(resourceArray.length()==0){
			System.err.println("no resource array");
		}
		JSONObject resourceObject = resourceArray.getJSONObject(0);
		
		
		if(which.equals("center")){
		
		if(!resourceObject.has("mapCenter")){
			System.err.println("no mapCenter");
		}
		JSONObject mapCenterObject = resourceObject.getJSONObject("mapCenter");
		
		if(!mapCenterObject.has("coordinates")){
			System.err.println("no coordinates");
		}
		JSONArray coordinateArray = mapCenterObject.getJSONArray("coordinates");
		
		//store the coordinates in the array
		returnData = new double[2];
		returnData[0] = coordinateArray.getDouble(0);
		returnData[1] = coordinateArray.getDouble(1);
		
		}
		
		else if(which.equals("bbox")){
			
			if(!resourceObject.has("bbox")){
				System.err.println("no bbox");
			}
			
			JSONArray boxArray = resourceObject.getJSONArray("bbox");
			
			//store the coordinates in the array
			returnData = new double[4];
			returnData[0] = boxArray.getDouble(0);
			returnData[1] = boxArray.getDouble(1);
			returnData[2] = boxArray.getDouble(2);
			returnData[3] = boxArray.getDouble(3);
		}
		
		if(returnData == null){
			System.err.println("that is not legitamite data");
		}
		
		return returnData;
	}

}
