#!/usr/bin/env python
import socket, sys
from thread import *


def start():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Initiate Socket
		s.bind(('', listening_port)) # Bind Socket For Listen
		s.listen(max_conn) # Start Listening for Incoming Connections
		print "[*] Initializing Sockets ... Done"
		print "[*] Sockets Binded Successfully ..."
		print("[*] AnonyProx server started [ %d ]\n % (listening_port))
	except Exception, e:
		# Execute this block if socket fails
		print "[*] Unable to initialize sockets"
		sys.exit(2)
		
		
	while 1:
		try:
			conn, addr = s.accept() # Accept connections from client browser
			data = conn.recv(buffer_size) # Receive client data
			start_new_thread(conn_string, (conn,data, addr)) # Start a thread
		except KeyboardInterrupt:
			# Execute this block if client socket failed
			s.close()
			print "\n[*] AnonyProx is shutting down ..."
			sys.exit(1)
			
		s.close()
		
def conn_string(conn, data, addr):
	# Client browser request appears here
	try:
		first_line = data.split('\n')[0]
		
		url = first_line.split(' ')[1]
		
		http_pos = url.find("://") # Find the positions of ://
		if (http_pos==-1):
			temp = url
		else:
		
			temp = url[(http_pos+3):] # Get the rest of the url
			
		port_pos = temp.find(":") # Find the pos of the port if any
		
		webserver_pos = temp.find("/") # Find the end of the webserver
		if webserver_pos == -1:
			webserver_pos = len(temp)
		webserver = ""
		port = -1
		if (port_pos==-1 or webserver_pos < port_pos):  # default port
			port = 80
			webserver = temp[:webserver_pos]
		else:
			# Specific Port
			port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
			webserver = temp[:port_pos]
			
		proxy_server(webserver, port, conn, addr, data)
	except Exception, e:
		pass
		
		
		
def proxy_server(webserver, port, conn, addr, data):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, port))
		s.send(data)
		
		while 1:
			# Read reply or data to and from end web server
			reply = s.recv(buffer_size)
			
			if (len(reply) > 0):
				conn.send(reply) # Send reply back to client
        
				# Send notification to AnonyProx
				dar = float(len(reply))
				dar = float(dar / 1024)
				dar = "%.3s" % (str(dar))
				dar = "%s KB % (dar)
				'Print a custom message for request complete'
				print "[*] Request complete: %s => %s <=" % (str)addr[0]),str(dar))
			else:
				# Break the connection if receiving data failed
				break
			# Feel free to close AnonyProx sockets
			s.close()
			# Now that everything is sent, we may now close our client socket
			conn.close()
		except socket.error, (value, message):
			s.close()
			conn.close()
			sys.exit(1)
			
start()
