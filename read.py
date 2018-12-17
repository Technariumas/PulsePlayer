#!/usr/bin/python3
# idVendor           0x0b9c 
#  idProduct          0x0315 
import binascii
import time
import vlc
from multiprocessing import Process

forestFile = "/home/opit/Desktop/hackerspace/projects/Pulse/sounds/squirrel.mp4"
cityFile = "/home/opit/Desktop/hackerspace/projects/Pulse/sounds/cat.mp4"

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

device = "/dev/hidraw4"
f = open(device, 'r')

def checkPulse():
    s = f.read(5)
    byte1 = ByteToHex(s[4]+s[3])
    pulse = int(str(byte1), base=16)
    bpm = (1000*60/pulse)
    print("BPM:", bpm)
    return bpm


while 1:
    bpm = checkPulse()
    print("INIT BPM:", bpm)
    if (bpm < 120) and (bpm > 80):
        print("CAT")
        cat.play()
        time.sleep(1)
        print("CHECKING")
        bpm = checkPulse()
        if (bpm <= 80):
		  cat.stop()
		  #break
    else if (bpm <= 80) and (bpm > 30):
        print("SQUIRREL")
        squirrel.play()
        time.sleep(1)
        print("CHECKING")        
        bpm = checkPulse()
        if (bpm > 80):
		  squirrel.stop()
		  #break
#		  break
	else:
		print("WAITING")
		bpm = checkPulse()
		time.sleep(0.1)	
		print("BPM:", bpm)
print("done")
