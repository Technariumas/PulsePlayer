#!/usr/bin/python3
# idVendor           0x0b9c 
#  idProduct          0x0315 
import binascii
import time
import vlc

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


while 1:
    s = f.read(5)
    #print("----")
    byte1 = ByteToHex(s[4]+s[3])
    pulse = int(str(byte1), base=16)
    bpm = (1000*60/pulse)
    #print(pulse)

    if (bpm < 120) and (bpm > 70):
        print("BPM:", bpm)
        time.sleep(2)
        cat.play()
    if (bpm <= 70) and (bpm > 40):
        print("BPM:", bpm)
        time.sleep(2)
        squirrel.play()

print("done")
