import socket
from threading import Thread
import time
import sys
from colorama import Fore, Back, Style, init

init(autoreset=True)

def accept_incoming_connections(): # Accepts incoming connections.
	while True:
		client, client_address = SERVER.accept()
		print("%s:%s connected." % client_address)
		client.send(bytes("8jhhaZaaq766712h5aaoaoaoaoppp17127477VVVAHAGgagx0Pz_12", "utf8")) # Sending "encrypted" message to the server
		addresses[client] = client_address
		Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
	while True:
		t = time.localtime()
		current_time = time.strftime("[%H:%M:%S]", t)
		Thread(target=announcements, args=(client,)).start()
		try:
			name = client.recv(BUFSIZ).decode("utf8")
			if name in users:
				client.send(bytes("Looks like you're already connected to the server!", "utf8")) # Clinet Error shown when Connecting with same ID Multiple times
				try:
					del clients[client]
				except KeyError:
					raise KeyError("[ERROR 100] "+name+" Multiple Client Try.") # Server Error shown when Connecting with same ID Multiple times
			else:
				users.append(name)
				global usernames
				usernames = ', '.join(users)
				welcome = '[Room] Welcome '+ name +'. Enjoy!' + "+"
				tmp = " "
				tmp = tmp.join(list(clients.values()))
				welcome = welcome + tmp
				client.send(bytes(welcome, "utf8"))
				clients[client] = name
				msg = name +" connected to room."+"+"
				joinlog = current_time +" >>>>>"+name +" connected to room." + "<<<<<"
				with open("LOGS.txt","a") as output: # Storing user connnected in LOGS.txt
					output.write(joinlog + '\n')
				output.close()
				tmp = " "
				tmp = tmp.join(list(clients.values()))
				msg = msg + tmp
				broadcast(bytes(msg, "utf8"))
				break
		except ConnectionResetError:

			try:
				del clients[client]
			except:
				pass
			try:
				users.remove(name)
			except:
				pass
				
		except BrokenPipeError:
			pass
	while True:

		try:
			msg = client.recv(BUFSIZ)
			checkMessage = str(msg)
			if len(msg) > 60:
				client.send(bytes("[Room] Message is too long (maximum is 60 characters).", "utf8")) # Message size < 60 chars check

			elif (msg == "7AHSGHA8125125125.AGSAGMKJASAH_1571257125AHSH.ZZZZZ"):
				client.send(bytes("[Room] Failed to send message, try again...", "utf8"))

			elif (checkMessage.find("kagsjhHYA") != -1): # File sent broadcast
				sender = checkMessage.split("+")[1]
				filename = checkMessage.split("+")[2]
				newFile = "jkkasgjasg76666AJHAHAHxxxxCf"+"+"+"[Room] "+sender + " has sent '"+filename+"."
				broadcast(bytes(newFile, "utf8"))
			elif (checkMessage.find("validationcheck") != -1): # File sent broadcast
				pw1 = checkMessage.split("+")[1]
				pw2 = checkMessage.split("+")[2]
				if pw1 == pw2:
					client.send(bytes("PASS", "utf8"))
			else:
				broadcast(msg, name+": ")
			
			
		except:
			try:
				client.close()
				users.remove(name)
				del clients[client]
				msg = name +" left the chat."+"+"
				leftlog = current_time +" >>>>>"+name + " left the chat." + "<<<<<"
				with open("LOGS.txt","a") as output: # Storing user left in LOGS.txt
					output.write(leftlog + '\n')
				output.close()
				msg = msg + name
				broadcast(bytes(msg, "utf8"))
				break
			except KeyError:
				break
			else:
				msg = name +" left the chat."+"+"
				leftlog1 = current_time +" >>>>>" +name + " left the chat." + "<<<<<"
				with open("LOGS.txt","a") as output:
					output.write(leftlog1 + '\n')
				output.close()
				msg = msg + name
				try:
					del clients[client]
				except KeyError:
					break
				broadcast(bytes(msg, "utf8"))
				users.remove(name)
				break

		if msg != "1J731JSG81jags881952kdpiSf18shj-123aasgxXAGa11_sfgCCCXXzzzz":

			msglog = msg.decode("utf8").rstrip()
			namelog = name

			message_log = current_time +" " +namelog + ": " + msglog
			with open("LOGS.txt","a") as output: # chat log saved in LOGS.txt
				output.write(message_log + '\n')

def announcements(client): # Avoid Timeout Method
	while True:
		try:
			time.sleep(120)
			timeoutProtect = "1J731JSG81jags881952kdpiSf18shj-123aasgxXAGa11_sfgCCCXXzzzz"
			client.send(bytes(timeoutProtect, "utf8"))
			time.sleep(120)
		except OSError:
			pass
def broadcast(msg, prefix=""): # Broadcast message recieved from client to other clients
	for sock in clients:
		sock.send(bytes(prefix, "utf8")+msg)

users = []
clients = {}
addresses = {}

with open("port.txt", 'r') as f: # Read port from port.txt
	portstr = f.readline().strip()

HOST = '10.1.0.5' # IP address of ssh server
PORT = int(portstr)
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM, proto = 0)
SERVER.bind((ADDR))

if __name__ == "__main__": # Console Log to display server status
	SERVER.listen(5)
	print(Fore.GREEN + "Server Started!")
	print(Fore.GREEN + "Clients now can connect.")
	print(Fore.GREEN + "Listening...\n")
	ACCEPT_THREAD = Thread(target=accept_incoming_connections)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()

