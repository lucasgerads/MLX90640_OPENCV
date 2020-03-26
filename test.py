import numpy as np
import serial, cv2, math

serialport = "COM34" # or something like '/dev/ttyS0' 
scalling = 20

width = scalling * 32
height = scalling * 24

img = np.zeros([height,width,3])
imgGray = np.zeros([height,width,3])

try:
    ser = serial.Serial(serialport,115000)
except serial.SerialException:
    print("Cannot open serial port")
    quit()

try:
    print("press Ctrl-C to end")
    while True:
        # read data from serial port
        cc=str(ser.readline())   
        cc = cc[2:-6]
        data = np.fromstring(cc,  sep=',')
         
        # reshape data into matrix
        output = data.reshape(24,32)
        
        # scaling
        minValue = math.floor(np.amin(output))
        maxValue = math.ceil(np.amax(output))
        output = output - minValue      
        output = output * 255/ (maxValue - minValue) # Now scaled to 0 - 255   

        # resize image
        dim = (width, height)
        output = cv2.resize(output, dim, interpolation = cv2.INTER_LINEAR )
             
        # apply colormap
        imgGray = output.astype(np.uint8)
        img = cv2.applyColorMap(imgGray, cv2.COLORMAP_JET)
        
        # put min/max text on image
        text = "Min: " + str(minValue) +  " C  Max: " + str(maxValue)+ " C"  
        font = cv2.FONT_HERSHEY_SIMPLEX  
        org = (20, 50) 
        image = cv2.putText(img, text, org, font, 1, (255, 255, 255) , 2, cv2.LINE_AA) 
        
        cv2.waitKey(50)
        cv2.imshow("image", img);

except KeyboardInterrupt:
    print("Bye bye :)")
    ser.close()
    
    
    
