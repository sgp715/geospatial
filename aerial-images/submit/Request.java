
public class Request {

	private String url;
	
	public Request(String url){
		
		this.url = url;	
	}
	
	public String getString(){
		return url;
	}
	
	
	public void printURL(){
		System.out.println(url);	
	}
	
	public void add(String add){
		
		//appending things to the URL
		url = url + add;
	}
	
	public void createMapArea(double[] boundBox){
	// a couple of things to add to the request
	String mapArea = "mapArea=";
	
	// filling in coordinates from user 
		for(int i = 0; i < boundBox.length; i++){
			mapArea = mapArea + boundBox[i];
			if(i < boundBox.length-1){
				mapArea = mapArea + ",";
			}
		}
	
		url = url + mapArea;
	}
	
}
