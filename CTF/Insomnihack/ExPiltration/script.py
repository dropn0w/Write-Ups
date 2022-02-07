import numpy as np
import cv2
import binascii

# Put the video path here
video = cv2.VideoCapture("video3x.mp4") # It is possible to speed up the video and get the same result. That is why we increased the speed by 3.
video.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

bit = True

# Set the position of the red light
rx = 1103 
ry = 828 

# Set the position of the green light
gx = 1075
gy = 828

bits = ""

print("Video analysis started.")
print("Please wait...")
while True:
    ret, frame = video.read()
    
    # Change the colors of the video
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (11, 11), 0)
        thresh = cv2.threshold(blurred, 220, 255, cv2.THRESH_BINARY)[1]

        cv2.circle(thresh, (rx,ry),12,(255,0,0),1)
        cv2.circle(thresh, (gx,gy),12,(255,0,0),1)

        cv2.imshow("video", thresh)
    else:
        break

    # Pick Pixel Value
    red_center = thresh[ry, rx]
    green_center = thresh[gy, gx]

    if red_center == 0:
        bit = False
    elif not bit and red_center == 255:
        bit = True
        if green_center == 0:
            #print("0", end="")
            bits += "0"
            with open('malicious_output.txt', 'a') as f:
                f.write("0")
                f.close()
        else:
            #print("1", end="")
            bits += "1"
            with open('malicious_output.txt', 'a') as f:
                f.write("1")
                f.close()

    # Push d to stop the script
    if cv2.waitKey(20) & 0xFF==ord('q'):
        break

    
video.release()
cv2.destroyAllWindows()

print("The orginal malicous file has been recreated.")
print('Check >>> "malicious_output.txtt" <<<')
print("Starting to decode the content...")

# Transfor binary format to ASCII 
bits_values = " ".join([bits[i:i+8] for i in range(0, len(bits), 8)])
binary_values = bits_values.split()
ascii_string = ""
for one_byte in binary_values:
    int_transfort = int(one_byte,2)
    ascii_character = chr(int_transfort)
    ascii_string += ascii_character

with open('content_decoded.txt', 'a') as f:
        f.write(ascii_string)
        f.close()

print("Content decoded!")
print("Check >>> content_decoded.txt <<< ")