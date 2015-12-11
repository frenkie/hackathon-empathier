import socket
import sys
import struct
from xml.etree import ElementTree as ET
import OSC





def ReceiveMessage(socketConnection):
    #read the first 4 bytes containing the total length of the response message
    messageLengthinBytes = socketConnection.recv(4)
    #convert the byte array to an int (array)
    totalMessageLength = struct.unpack('I', messageLengthinBytes)[0]
    #read the second 4 bytes containing the length of the messageType
    messageTypeLengthinBytes = socketConnection.recv(4)
    #convert the byte array to an int (array)
    messageTypeLength = struct.unpack('I', messageTypeLengthinBytes)[0]

    #read the message type
    messageTypeString = socketConnection.recv(messageTypeLength)
    #print 'Received a response message op type: ' + messageTypeString
    remainingLength = totalMessageLength - 8 - messageTypeLength

    #read the xml data
    messageString = ''

    if remainingLength > 0:
        messageString = socketConnection.recv(remainingLength)
        #print 'Response message: ' + messageString
        #print messageString

    return messageString




def SendMessage(socketConnection, messageType, xmlMessage):
    dataToSend = bytearray()
    lenMessageType = len(messageType)
    lenMessage = len(xmlMessage)
    totalLen = 4 + lenMessageType + lenMessage + 4
    lenMessageTypeInBytes = struct.pack('I', len(messageType))
    lenInBytesTotal = struct.pack('I', totalLen)
    dataToSend.extend(lenInBytesTotal)
    dataToSend.extend(lenMessageTypeInBytes)
    dataToSend.extend(messageType)
    dataToSend.extend(xmlMessage)
    print 'Sending message: ' + xmlMessage
    socketConnection.send(dataToSend)


with open ("startAnalyzing.xml", "r") as startfile:
    startMessage=startfile.read() 

with open ("receiveDetailed.xml", "r") as receivefile:
    receiveMessage=receivefile.read() 

messageType = 'FaceReaderAPI.Messages.ActionMessage'


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
try:
    s.connect(('10.0.1.124', 9090))
except socket.error , msg:
    print 'Connection failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket connected to FaceReader'

## better practice ##
client = OSC.OSCClient()
client.connect( ('10.0.1.96', 8000) ) # note that the argument is a tupple and not two arguments


try:
   
   SendMessage(s, messageType, receiveMessage)  
   response = ReceiveMessage(s)
   SendMessage(s, messageType, startMessage)  
   response = ReceiveMessage(s)
   
   xmlTree = ET.fromstring(response)
   while True:
       response = ReceiveMessage(s)
       xmlTree = ET.fromstring(response)
       for child in xmlTree.iter('ClassificationValues'):
           for sub in child.iter('ClassificationValue'):
               tiepe = sub.find('Type').text
               label = sub.find('Label').text
               
               for value in sub.iter('Value'):
                   if (tiepe == 'Value') and (label == 'Landmarks'):
                      number = value.findall('float')
                   else:
                      number = value.find('float').text
 
               if (tiepe == 'Value') and (label == 'X - Head Orientation'):
                   print tiepe, ' : ', label, ' : ', number
                   msg = OSC.OSCMessage() #  we reuse the same variable msg used above overwriting it
                   msg.setAddress('/Ox')
                   msg.append(float(number))
                   client.send(msg) # now we dont need to tell the client the address anymore

               if (tiepe == 'Value') and (label == 'Y - Head Orientation'):
                   print tiepe, ' : ', label, ' : ', number
                   msg = OSC.OSCMessage() #  we reuse the same variable msg used above overwriting it
                   msg.setAddress('/Oy')
                   msg.append(float(number))
                   client.send(msg) # now we dont need to tell the client the address anymore

               if (tiepe == 'Value') and (label == 'Z - Head Orientation'):
                   print tiepe, ' : ', label, ' : ', number
                   msg = OSC.OSCMessage() #  we reuse the same variable msg used above overwriting it
                   msg.setAddress('/Oz')
                   msg.append(float(number))
                   client.send(msg) # now we dont need to tell the client the address anymore

               if (tiepe == 'Value') and (label == 'Landmarks'):
                   print tiepe, ' : ', label, ' : ', number[0].text, ' , ', number[1].text
                   msg = OSC.OSCMessage() #  we reuse the same variable msg used above overwriting it
                   msg.setAddress('/x')
                   msg.append(float(number[0].text))
                   client.send(msg) # now we dont need to tell the client the address anymore
                   msg = OSC.OSCMessage() #  we reuse the same variable msg used above overwriting it
                   msg.setAddress('/y')
                   msg.append(float(number[1].text))
                   client.send(msg) # now we dont need to tell the client the address anymore


                   

  

finally:
    print >>sys.stderr, 'closing socket'
    s.close()
