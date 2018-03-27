import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Scanner;

import javax.imageio.ImageIO;

public class ImageToTexture {
	public static void main(String[] args) throws FileNotFoundException {
		File file = new File("./pixels.txt");
		File file2 = new File("./pixels2.txt");
		Scanner input = new Scanner(file);
		Scanner input2 = new Scanner(file2);

		PrintWriter writer = new PrintWriter("data/texture.json");
		writer.print("[");

		final int NUMBER_OF_PICTURES = 1604;
		final int WIDTH = 75;
		final int HEIGHT = 75;

		// loop through number of pictures
	    for (int i = 0; i < NUMBER_OF_PICTURES; i++) {
	    	int[][] imageArray = new int[WIDTH][HEIGHT];
	    	// loop through pixels
	    	for (int j = 0; j < WIDTH; j++) {
	    		for (int k = 0; k < HEIGHT; k++) {
	    			int pixelValue = input.nextInt();
	    			int pixelValue2 = input2.nextInt();

    				imageArray[j][k] = (pixelValue + pixelValue2) / 2;
	    		}
	    	}

	    	boolean isIceberg = input.nextInt() == 1;

	    	int[][] horizontalMatrix = matrixHorizontal(imageArray);
	    	double asm = ASM(horizontalMatrix);
	    	if (i != NUMBER_OF_PICTURES - 1) {
	    		writer.print(asm + ",");
	    	} else {
	    		writer.print(asm);
	    	}
	    }

	    writer.print("]");

		writer.close();
		input.close();
		input2.close();
	}

	// calculates horizontal gray-tone spatial-dependence matrix
	public static int[][] matrixHorizontal(int[][] image) {
		int minGrayTone = image[0][0];
		int maxGrayTone = image[0][0];

		for (int i = 0; i < image.length; i++) {
			for (int j = 0; j < image[0].length; j++) {
				if (image[i][j] < minGrayTone) {
					minGrayTone = image[i][j];
				}

				if (image[i][j] > maxGrayTone) {
					maxGrayTone = image[i][j];
				}
			}
		}

		int range = maxGrayTone - minGrayTone + 1;
		int[][] horizontalMatrix = new int[range][range];

		for (int k = 0; k < image.length; k++) {
			for (int l = 0; l < image[0].length - 1; l++) {
				int val1 = image[k][l] - minGrayTone;
				int val2 = image[k][l + 1] - minGrayTone;
				horizontalMatrix[val1][val2]++;
				horizontalMatrix[val2][val1]++;
			}
		}

		return horizontalMatrix;
	}

	public static double ASM(int[][] matrix) {
		double value = 0;

		for (int i = 0; i < matrix.length; i++) {
			for (int j = 0; j < matrix[0].length; j++) {
				value += Math.pow(matrix[i][j], 2) / Math.pow(matrix.length, 2);
			}
		}

		return value;
	}
}
