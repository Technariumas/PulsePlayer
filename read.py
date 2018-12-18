#!/usr/bin/python3
# idVendor           0x0b9c 
#  idProduct          0x0315 
import binascii
import time
import vlc
from multiprocessing import Process
import numpy as np
import collections

forestFile = "/home/opit/Desktop/hackerspace/projects/Pulse/sounds/squirrel.mp4"
cityFile = "/home/opit/Desktop/hackerspace/projects/Pulse/sounds/cat.mp4"

cat = vlc.MediaPlayer(cityFile)
squirrel = vlc.MediaPlayer(forestFile)

def running_mean(x, N):
    cumsum = numpy.cumsum(numpy.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

def moving_average(iterable, n=10):
    # moving_average([40, 30, 50, 46, 39, 44]) --> 40.0 42.0 45.0 43.0
    # http://en.wikipedia.org/wiki/Moving_average
    it = iter(iterable)
    d = deque(itertools.islice(it, n-1))
    d.appendleft(0)
    s = sum(d)
    for elem in it:
        s += elem - d.popleft()
        d.append(elem)
        yield s / n

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
    return bpm

avgArray = checkPulse()*np.ones((10, 1))
previousMean = np.mean(avgArray)
counter = 0

while 1:
    bpm = checkPulse()
    if (bpm < 120) and (bpm > 30):
      counter+=1
      if counter > 10:	
        avgArray = np.roll(avgArray, -1)
        avgArray[0] = bpm
        mean = np.mean(avgArray)
        print(mean, "mean")
        print(previousMean, "PREVIOUS")
        if mean >= previousMean:
          squirrel.stop()
          print("CAT")
          cat.play()
          time.sleep(3)
          previousMean = mean          
          #bpm = checkPulse()
          #if (bpm <= 80):
		   # cat.stop()
		    #break
        elif (mean < previousMean):
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
