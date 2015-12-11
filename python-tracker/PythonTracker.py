import socket
import sys
import struct
from xml.etree import ElementTree as ET
import OSC


def ReceiveMessage(socketConnection):
	# read the first 4 bytes containing the total length of the response message
	messageLengthinBytes = socketConnection.recv(4)
	# convert the byte array to an int (array)
	totalMessageLength = struct.unpack('I', messageLengthinBytes)[0]
	# read the second 4 bytes containing the length of the messageType
	messageTypeLengthinBytes = socketConnection.recv(4)
	# convert the byte array to an int (array)
	messageTypeLength = struct.unpack('I', messageTypeLengthinBytes)[0]
	# read the message type
	messageTypeString = socketConnection.recv(messageTypeLength)
	# print 'Received a response message op type: ' + messageTypeString
	remainingLength = totalMessageLength - 8 - messageTypeLength
	# read the xml data
	messageString = ''
	if remainingLength > 0:
		messageString = socketConnection.recv(remainingLength)
		# print 'Response message: ' + messageString
		# print messageString
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


with open("startAnalyzing.xml", "r") as startfile:
	startMessage = startfile.read()
with open("receiveDetailed.xml", "r") as receivefile:
	receiveMessage = receivefile.read()
messageType = 'FaceReaderAPI.Messages.ActionMessage'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
	s.connect(('127.0.0.1', 9090))
except socket.error, msg:
	print 'Connection failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

print 'Socket connected to FaceReader'
## better practice ##
clientSebas = OSC.OSCClient()
clientSebas.connect(('10.0.1.96', 8000))
clientMark = OSC.OSCClient()
clientMark.connect(('10.0.1.108', 8000))
clientBas = OSC.OSCClient()
clientBas.connect(('10.0.1.125', 8000))


def SendToClients(msg):
	clientSebas.send(msg)
	clientMark.send(msg)
	clientBas.send(msg)


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

				if (tiepe == 'Value'):
					# print tiepe, ' : ', label, ' : ', number

					msg = OSC.OSCMessage()
					msg.setAddress('/live/%s' % label.lower())
					msg.append(float(number))

					SendToClients(msg)

finally:
	print >> sys.stderr, 'closing socket'
	s.close()
