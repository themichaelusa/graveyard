import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

public class Main {

    public static void main(String[] args) {


    }

    public static BufferedImage loadImage() {

        try {
            return ImageIO.read(new File("test.png"));

        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    public static ArrayList<int[]> imageToRGB(BufferedImage image) {

        Color c = new Color(image.getRGB());
        int red = c.getRed();
        int green = c.getGreen();
        int blue = c.getBlue();

        return new int[] {red, green, blue};
    }

}
