from __future__ import division
#!/usr/bin/python3
# idVendor           0x0b9c 
#  idProduct          0x0315 
import binascii
import time
import vlc
import numpy as np

forestFile = "/home/pi/PulsePlayer/sounds/jura.wav"
cityFile = "/home/pi/PulsePlayer/sounds/miestas.wav"

cat = vlc.MediaPlayer(cityFile)
squirrel = vlc.MediaPlayer(forestFile)

def ByteToHex( byteStr ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """
    
    # Uses list comprehension which is a fractionally faster implementation than
    # the alternative, more readable, implementation below
    #   
    #    hex = []
    #    for aChar in byteStr:
    #        hex.append( "%02X " % ord( aChar ) )
    #
    #    return ''.join( hex ).strip()        

    return ''.join([ "%02X" % ord( x ) for x in byteStr ] ).strip()

def hex2dec (hex):
    result_dec = int(hex, 0)
    return result_dec

device = "/dev/hidraw5"
f = open(device, 'r')

def checkPulse():
    s = f.read(5)
    byte1 = ByteToHex(s[4]+s[3])
    pulse = int(str(byte1), base=16)
    bpm = (1000*60/pulse)
    return bpm

avgArray = checkPulse()*np.ones((10, 1))
previousMean = np.mean(avgArray)
counter = 0

while 1:
    bpm = checkPulse()
    if (bpm < 120) and (bpm > 30):
      counter+=1
      print(counter)
      if counter > 10:	
        avgArray = np.roll(avgArray, -1)
        avgArray[0] = bpm
        mean = np.mean(avgArray)
        print(mean, "mean")
        print(previousMean, "PREVIOUS")
        if (mean - previousMean) >= 1:
          squirrel.stop()
          print("CAT")
          cat.play()
          time.sleep(3)
          previousMean = mean          
          #bpm = checkPulse()
          #if (bpm <= 80):
		   # cat.stop()
		    #break
        elif (mean - previousMean) < -1:
          cat.stop()
          print("SQUIRREL")
          squirrel.play()
          time.sleep(3)
          #bpm = checkPulse()
          #if (bpm > 80):
		  #  squirrel.stop()
		    #break
  # 		  break
          previousMean = mean
	else:
		print("WAITING")
		bpm = checkPulse()
		time.sleep(0.1)	
		print("BPM:", bpm)
print("done")
