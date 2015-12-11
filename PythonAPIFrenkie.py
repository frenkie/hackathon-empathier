import socket
import logging
import sys
import struct
import xmltodict, json
import OSC

from xml.etree import ElementTree as ET

logging.basicConfig(level=getattr(logging, 'INFO', None));

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
   # print 'Received a response message op type: ' + messageTypeString
   remainingLength = totalMessageLength - 8 - messageTypeLength

   #read the xml data
   if remainingLength > 0:
       messageString = socketConnection.recv(remainingLength)

       # buh!
       if "<ClassificationValue>" in messageString:
           try:
               print messageString
               o = xmltodict.parse(messageString)
               logging.info(json.dumps(o) + "\n")
               #return messageString

           except:
               print 'skipping'

   return ''


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

try:
   s.connect(('10.0.1.124', 9090))
except socket.error , msg:
   print 'Connection failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
   sys.exit()

print 'Socket connected to FaceReader'


try:

  SendMessage(s, messageType, receiveMessage)
  response = ReceiveMessage(s)
  SendMessage(s, messageType, startMessage)
  response = ReceiveMessage(s)

  while True:
      response = ReceiveMessage(s)
      if not response == '':
          print response
          xmlTree = ET.fromstring(response)


finally:
   print >>sys.stderr, 'closing socket'
   s.close()