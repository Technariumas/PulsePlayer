#!/usr/bin/python3
# idVendor           0x0b9c 
#  idProduct          0x0315 
import binascii
import time



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
    print("----")
    byte1 = ByteToHex(s[4]+s[3])
    pulse = int(str(byte1), base=16)
    print(pulse)
    print("BPM:", (1000*60)/pulse)
print("done")
