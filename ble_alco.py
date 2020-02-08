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
                                    print "Read: "+ str(c.read())
                                    command_addr = "684230303002186801020002ffc016"
                                    command_connect = "684230303002186804030004ff01c716"
                                    command_disconnect = "684230303002186804030004ff00c616"
                                    command_status = "684230303002186801020001905016"
                                    command_measure = "684230303002186801020002905116"
                                    command_read = "684230303002186801020003905216"
                                    command_mode = "684230303016096804030003ff01cb16"
                                    command_readtime = "684230303002186801020001ffbf16"
                                    #c.write(binascii.unhexlify(command_measure))
                                    #p.waitForNotifications(1.0)
                                    #raw_input("Press Enter to continue...")
                                    c.write(binascii.unhexlify(command_read))
                                    p.waitForNotifications(1.0)
                        except Exception as e:
                            print e
                    p.disconnect();
                except Exception as e:
                    print e
                    #continue
                finally:
                    pass
