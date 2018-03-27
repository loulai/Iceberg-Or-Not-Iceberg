import java.awt.image.BufferedImage;
import java.awt.image.WritableRaster;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;
import java.util.*;

public class Image {
	public static void main(String[] args) throws IOException {
		File icebergs1 = new File("./icebergs1");
		File icebergs2 = new File("./icebergs2");
		File icebergsAverage = new File("./icebergsAverage");
		
		File ships1 = new File("./ships1");
		File ships2 = new File("./ships2");
		File shipsAverage = new File("./shipsAverage");
		
		if (!(icebergs1.exists() || icebergs2.exists() || icebergsAverage.exists()
				|| ships1.exists() || ships2.exists() || shipsAverage.exists())) {
			icebergs1.mkdir();
			icebergs2.mkdir();
			icebergsAverage.mkdir();
			ships1.mkdir();
			ships2.mkdir();
			shipsAverage.mkdir();
		}
		
		File file = new File("./pixels.txt");
		File file2 = new File("./pixels2.txt");
		Scanner input = new Scanner(file);
		Scanner input2 = new Scanner(file2);
		
		// default 1604
		final int NUMBER_OF_PICTURES = 1604;
		final int WIDTH = 75;
		final int HEIGHT = 75;
		final int BANDS = 3;

	    int icebergCounter = 0;
	    int shipCounter = 0;

	    // loop through number of pictures
	    for (int i = 0; i < NUMBER_OF_PICTURES; i++) {   
	    	int[] imageArray1 = new int[WIDTH * HEIGHT * 3];
	    	int[] imageArray2 = new int[WIDTH * HEIGHT * 3];
	    	int[] imageArray3 = new int[WIDTH * HEIGHT * 3];
	    	// loop through pixels
	    	for (int j = 0; j < WIDTH; j++) {
	    		for (int k = 0; k < HEIGHT; k++) {
	    			int pixelValue = input.nextInt();
	    			int pixelValue2 = input2.nextInt();
	    			// loop through RGB values
	    			for (int l = 0; l < 3; l++) {
	    				imageArray1[(j * WIDTH + k) * BANDS + l] = pixelValue;
	    				imageArray2[(j * WIDTH + k) * BANDS + l] = pixelValue2;
	    				imageArray3[(j * WIDTH + k) * BANDS + l] = (pixelValue + pixelValue2) / 2;
	    			}
	    		}
	    	}
	    	
	    	boolean isIceberg = input.nextInt() == 1;
	    	
	    	String imagePath1 = null;
	    	String imagePath2 = null;
	    	String imagePath3 = null;
	    	
	    	if (isIceberg) {
	    		icebergCounter++;
	    		imagePath1 = "./icebergs1/" + icebergCounter;
	    		imagePath2 = "./icebergs2/" + icebergCounter;
	    		imagePath3 = "./icebergsAverage/" + icebergCounter;
	    	} else {
	    		shipCounter++;
	    		imagePath1 = "./ships1/" + shipCounter;
	    		imagePath2 = "./ships2/" + shipCounter;
	    		imagePath3 = "./shipsAverage/" + shipCounter;
	    	}
	    	
	    	BufferedImage image1 = getImageFromArray(imageArray1, WIDTH, HEIGHT);
	        File imageFile1 = new File(imagePath1);
	        ImageIO.write(image1, "PNG", imageFile1);
	        
	        BufferedImage image2 = getImageFromArray(imageArray2, WIDTH, HEIGHT);
	        File imageFile2 = new File(imagePath2);
	        ImageIO.write(image2, "PNG", imageFile2);
	        
	        BufferedImage image3 = getImageFromArray(imageArray3, WIDTH, HEIGHT);
	        File imageFile3 = new File(imagePath3);
	        ImageIO.write(image3, "PNG", imageFile3);
	    }
	    
	    
	    input.close();
	    input2.close();
	}
	
	public static BufferedImage getImageFromArray(int[] pixels, int width, int height) {
		BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
	    WritableRaster raster = (WritableRaster) image.getData();
	    raster.setPixels(0, 0, width, height, pixels);
	    image.setData(raster);
	    return image;
	}
}
