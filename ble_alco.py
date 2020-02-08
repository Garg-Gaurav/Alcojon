from bluepy.btle import Scanner, DefaultDelegate, Peripheral
import threading
import binascii
import time
from struct import *
 
class NotificationDelegate(DefaultDelegate):
 
    def __init__(self, number):
        DefaultDelegate.__init__(self)
        self.number = number
 
    def handleNotification(self, cHandle, data):
        print 'Notification:\nConnection:'+str(self.number)+'\nHandler:'+str(cHandle)+'\nMsg:'+binascii.hexlify(data)
 
bt_addrs = []
connections = []
connection_threads = []
scanner = Scanner(0)

def calculateCheckSum(dataString):
    dataPacketStr = dataString.split(',')
    loop = len(dataPacketStr)
    checkSumTotal = 0;
    while loop > 0:
        checkSumTotal = int(dataPacketStr[loop - 1], 16) + checkSumTotal;
        loop = loop - 1;
    checkSumTotal = checkSumTotal % 256
    #print(hex(checkSumTotal))
    return hex(checkSumTotal)

def sendDataPacket(controlBit, Data):
    initialDataPacket="0x68,0x42,0x30,0x30,0x30,0x02,0x18,0x68";
    dataLength = "0x%0.2X,0x00" % (len(Data.replace("0x","").replace(",",""))/2)
    #print("dataLenth:"+dataLength)
    calulateCheckSumString=initialDataPacket+","+controlBit+","+dataLength+","+Data;
    checkSumVal=calculateCheckSum(calulateCheckSumString);
    finalDataPacket=calulateCheckSumString+","+str(checkSumVal)+",0x16"
    return finalDataPacket.replace("0x","").replace(",","")


class ConnectionHandlerThread (threading.Thread):
    def __init__(self, connection_index):
        threading.Thread.__init__(self)
        self.connection_index = connection_index
 
    def run(self):
        connection = connections[self.connection_index]
        connection.setDelegate(NotificationDelegate(self.connection_index))
        while True:
            if connection.waitForNotifications(1):
                connection.writeCharacteristic(37, 'Thank you for the notification!')
 
while True:
    #print'Connected: '+str(len(connection_threads))
    #print 'Scanning...'
    devices = scanner.scan(2)
    for d in devices:
        #print "[",d.addr,"]:",d.rssi
        s = ""
        found = 0
        for (adtype, desc, value) in d.getScanData():
            #print "    %s = %s"%(desc,value)
            s = s + str(desc) + " : " + str(value) + "\n"
            if desc == "Complete Local Name" and "HMSoft" in value:
                #print s
                try:
                    p = Peripheral(d)
                    p.setDelegate( NotificationDelegate(0) )
                    services = p.getServices()
                    for srv in services:
                        #print "    UUID:", srv.uuid
                        try:
                            characteristics = srv.getCharacteristics()
                            for c in characteristics:
                                #print "        UUID:", c.uuid
                                if c.uuid == "0000ffe1-0000-1000-8000-00805f9b34fb":
                                    print "Alco char found!"
                                    #Connect
                                    c.write(binascii.unhexlify(sendDataPacket("0x04","0x04,0xff,0x01")))
                                    p.waitForNotifications(1.0)
                                    #Measure
                                    c.write(binascii.unhexlify(sendDataPacket("0x01","0x02,0x90")))
                                    while p.waitForNotifications(10.0):
                                        continue
                                    #Disconncet
                                    c.write(binascii.unhexlify(sendDataPacket("0x04","0x04,0xff,0x00")))
                                    p.waitForNotifications(1.0)
                        except Exception as e:
                            print e
                    p.disconnect();
                except Exception as e:
                    print e
                    #continue
                finally:
                    pass
