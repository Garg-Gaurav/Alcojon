#calculate checksum

def calculateCheckSum(dataString):
    dataPacketStr = dataString.split(',')
    loop = len(dataPacketStr)
    checkSumTotal = 0;
    while loop > 0:
        checkSumTotal = int(dataPacketStr[loop - 1], 16) + checkSumTotal;
        loop = loop - 1;
    checkSumTotal = checkSumTotal % 256
    print(hex(checkSumTotal))
    return hex(checkSumTotal)

def sendDataPacket(controlBit,dataLength,Data):
    initialDataPacket="0x68,0x42,0x30,0x30,0x30,0x16,0x09,0x68";
    calulateCheckSumString=initialDataPacket+","+controlBit+","+dataLength+","+Data;
    checkSumVal=calculateCheckSum(calulateCheckSumString);
    finalDataPacket=calulateCheckSumString+","+str(checkSumVal)+",0x16"
    return finalDataPacket


dataPacket=sendDataPacket("0x04","0x03,0x00","0x04,0xff")
print(dataPacket)



