
public class BoundArea {
	
	
	private double boundArea;
	private double radius;
	private double earthArea;
	private double[] levels;

	public BoundArea(double lat1, double lat2, double long1, double long2){
		
		// earths radius and sa in km
		radius = 6371;
		earthArea = 510100000;
		
		//calculating the area of the bound
		boundArea = ((Math.PI)/180) * Math.pow(radius, 2) * Math.abs(Math.sin(lat1) - Math.sin(lat2)) * Math.abs(long1 -long2);
		
		
		//calculating all the levels
		levels = new double[23];
		calculateLevels();
		
	}
	
	private void calculateLevels(){
		
		for(int i = 1; i < levels.length+1; i++){
			double tiles = Math.pow(4, i);
			levels[i-1] = earthArea / tiles;
		}
		
	}
	
	public void printLevels(){
		for(int i = 0; i < levels.length; i++){
			System.out.println("current level: ");
			System.out.println(levels[i]);
		}
	}
	
	public void printArea(){
		System.out.println("The bounding box area is: " + boundArea);
	}
	
	
	public double getArea(){
		return boundArea;
	}
	
	public double getEarthArea(){
		return earthArea;
	}
	
	public int getLevel(){
		
		int level = 0;
		
		if(boundArea > earthArea){
			System.err.println("The calculated area: " + boundArea + "is larger that earth: " + earthArea);
		}
		
		while(boundArea < levels[level] && (level != 22)){
			level++;
		}
		
		// we can not have a level greater that 23 or less than 1
		assert(level < 24);
		assert(level > 0);
		
		return level;
	}
	
	public int getNumTiles(){
		return 0;
	}

}
