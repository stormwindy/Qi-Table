import java.io.PrintWriter;
import java.util.Scanner;

import com.fazecast.jSerialComm.SerialPort;


/*
 * This code would have not been possible without
 * https://github.com/SackLunch/Java-Arduino-Controller/blob/master/Arduino.java
 */

public class main {

	//No idea what this is
	private static final long serialVersionUID = 1L;
	//Serial port object
	private static SerialPort comPort;
	
	//Serial port name, on DICE it is ttyACM0 for 1st USB connected
	private static String comPortName = "ttyACM0";
	//Setting the baud rate (should be 115200)
	private static int baudRate = 115200;

	//Writer object for serial
	private static PrintWriter outPut;

	
	//forward: in binary 010, in decimal 2
	private final static byte forward = 2;
	//backwards: in binary 001, in decimal 1
	private final static byte backwards = 1;
	//left: in binary 011, in decimal 3
	private final static byte left = 3;
	//right: in binary 100, in decimal 4
	private final static byte right = 4 ;
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub

		comPort = SerialPort.getCommPort(comPortName);
		comPort.setBaudRate(baudRate);
			
		//If the port is not closed, open the USB port.
		if(comPort.isOpen() == false)
		{	
			try 
			{
				//Open the USB port and initialize the PrintWriter.
				comPort.openPort();
				Thread.sleep(1000);
				outPut = new PrintWriter(comPort.getOutputStream());
			} 
			
			catch(Exception c){}
			
			//Update the console and status.
			System.out.println("Connection to Arduino successful.");
			
		}
		else 
		{
			//If the port couldn't be opened print out to the console.
			System.out.println("Error opening port.");
			System.exit(0); //exit
		}
//----------------------------------------------------------------------------------------		

		String line;
		byte repeatCounter = 0;
	    Scanner sc = new Scanner(System.in);
	    do {
	    	   System.out.println("w/a/s/d (smaller case) and press ENTER (exit with q):");
	           line = sc.nextLine().trim();
	           
	           //exit if q is pressed
	           if (line.equals("q"))
	        	   break;
	           
		       System.out.println("Enter an integer for how many times it should be sent:");
		       repeatCounter = Byte.parseByte(sc.nextLine().trim());
				       
			
				//If all good, send the required data
				if(comPort.isOpen() == true)
				{
					
				   byte encodedValue = 100; //random value of 100 decimal

					
					//Send the end value.
					switch (line) {
						case "w" : encodedValue = forward; break;
						case "a" : encodedValue = left; break;
						case "s" : encodedValue = backwards; break;
						case "d" : encodedValue = right; break;
						default:  System.out.println("unrecognised char"); continue;

					}
					
					for (byte i = 0; i < repeatCounter; i++) {
						outPut.print(encodedValue);
						outPut.flush();
					}
					}
				else
				{
					//Update the status/console if the Arduino hasn't been connected.
					System.out.println("Arduino not connected, Connect Arduino!");
					System.exit(0);
				}
		
	    	} while (true); //exit with q

		
		
//----------------------------------------------------------------------------------------		
		//Close the USB port if it's open.
		if(comPort.isOpen() == true)
		{	
			//Close the port and update the console/status.
			comPort.closePort();
			System.out.println("Disconnected from Arduino.");
			System.exit(0);
		}
		
	}
	

}
