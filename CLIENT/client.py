import paramiko
import os
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import os, winshell
import time
from setup import *
from win32com.client import Dispatch
from tkinter import filedialog
from cryptography.fernet import Fernet

activeTheme = "Light" # setting default theme

localVersion = "4.0.0" # Client App Version
serverVersion = sshhomepath+"/Server_Data/version.txt"
localVersionP = "version.txt"
	

def ConnectMain(): # Main Connection Method

	try:
		global client
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(ipofssh, username=usernamessh, password=passwordssh) # Tries Logging in from details entered in setup.py
		global transport
		global sftp
		transport = client.get_transport()
		sftp = paramiko.SFTPClient.from_transport(transport)
		sftp = client.open_sftp()
		
	except: # Connection Failed Condition
		connectButton['state'] = tkinter.DISABLED
		loginButton['state'] = tkinter.DISABLED
		registerButton['state'] = tkinter.DISABLED
		menu.title("SecuRoom Offline")
		conError = tkinter.Toplevel(menu, bg= "#C3FFF2")
		conError.iconbitmap("Sources/icon.ico")
		conError.geometry("400x60")
		conError.resizable(False, False)
		conError.title("Connection Error")
		conError.configure(background = "#C3FFF2")
		errLabel = tkinter.Label(conError, text = "Failed to connect to SecuRoom",font = "Consolas 15", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
		errLabel.pack()
		errBtn = tkinter.Button(conError, text="Exit",font = "Consolas 10 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = conError.destroy)
		errBtn.pack()
		if activeTheme == "Dark": # 
			conError.configure(bg = darkcolor)
			errLabel.configure(bg = darkcolor,fg = "white")
			errBtn.configure(bg = "#151515",activebackground="#B4B4B4")
		else:
			pass

def connectRoomServer(): # Connecting to created Room Method
	try:
		accountmanagement.destroy()
	except:
		pass
	try:
		sftp = client.open_sftp()
	except: # Internet Connectivity Related Errors
		connectButton['state'] = tkinter.DISABLED
		loginButton['state'] = tkinter.DISABLED
		registerButton['state'] = tkinter.DISABLED
		menu.title("Connection Timed Out")
		internetError = tkinter.Toplevel(menu, bg= "#C3FFF2")
		internetError.iconbitmap("Sources/icon.ico")
		internetError.geometry("575x60")
		internetError.resizable(False, False)
		internetError.title("Server Unavailable")
		internetError.configure(background = "#C3FFF2")
		errLabel1 = tkinter.Label(internetError, text = "Check your Internet Connection",font = "Consolas 15", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
		errLabel1.pack()
		errBtn1 = tkinter.Button(internetError, text="Exit",font = "Consolas 10 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = quit)
		errBtn1.pack()
		internetError.protocol("WM_DELETE_WINDOW", quit)
		if activeTheme == "Dark":
			internetError.configure (bg = darkcolor)
			errLabel1.configure(bg = darkcolor)
			errBtn1.configure(bg = "#151515", activebackground = "#B4B4B4")
		else:
			pass
	sftp.get(serverVersion, localVersionP)
	with open(localVersionP, 'r') as f:
		vers = f.readline().strip()
	f.close()
	os.remove(localVersionP)

	def exitOld():
		oldVersion.destroy()
		menu.destroy()

	if vers != localVersion: # Checking if Client and Server are on the Same Version
		menu.title("SecuRoom Update Available")
		connectButton['state'] = tkinter.DISABLED
		oldVersion = tkinter.Toplevel(menu, bg = "#C3FFF2")
		oldVersion.iconbitmap("Sources/icon.ico")
		oldVersion.geometry("780x60")
		oldVersion.resizable(True, True)
		oldVersion.title("SecuRoom Update Available")
		errLabel2 = tkinter.Label(oldVersion, text = "Update Client to Continue using SecuRoom",font = "Consolas 15", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
		errLabel2.pack()
		exit_button4 = tkinter.Button(oldVersion, text="Exit",font = "Consolas 10 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = exitOld)
		exit_button4.pack()
		if activeTheme == "Dark":
			oldVersion.configure(bg = darkcolor)
			errLabel2.configure(bg = darkcolor,fg = "white")
			exit_button4.configure(bg = "#151515",activebackground="#B4B4B4")
		else:
			pass
	else:
		connectButton['state'] = tkinter.DISABLED
		roomName2 = roomNameConnect.get()
		roomToken2 = roomTokenConnect.get()
		serverPortP = sshhomepath+"/Server_Data/Rooms/"+roomName2+"/port.txt"
		serverRoomName = sshhomepath+"/Server_Data/Rooms/"+roomName2+"/roomName.txt"
		serverRoomToken = sshhomepath+"/Server_Data/Rooms/"+roomName2+"/roomToken.txt"
		localPort = "lastJoinedRoomsPort.txt"
		localRoomName = "room.txt"
		localRoomToken = "token.txt"
		sftp = client.open_sftp()
		try: # Downloading Server Details to connect with Remote
			sftp.get(serverPortP, localPort)
			sftp.get(serverRoomName, localRoomName)
		except: # Room not found error
			def exittt():
				connectButton['state'] = tkinter.NORMAL
				error2.destroy()
			error2 = tkinter.Toplevel(menu, bg = "#C3FFF2")
			error2.geometry("400x60")
			error2.iconbitmap("Sources/icon.ico")
			error2.resizable(False, False)
			error2.title("SecuRoom Failed to Connect")
			error2.configure(background = "#C3FFF2")
			os.remove(localPort)
			buton2 = tkinter.Label(error2, text = "Cannot Find Specified Room.",font = "Consolas 15", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
			buton2.pack()
			ci2k = tkinter.Button(error2, text="Exit",font = "Consolas 10 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = exittt)
			ci2k.pack()
			error2.protocol("WM_DELETE_WINDOW", exittt)
			if activeTheme == "Dark":
				error2.configure(bg = darkcolor)
				buton2.configure(bg = darkcolor,fg = "white")
				ci2k.configure(bg = "#151515",activebackground="#B4B4B4")
			else:
				pass
		else: # Room Found! Continuing with Connection Process
			with open(localPort, 'r') as f:
					portstr = f.readline().strip()
			f.close()
			os.remove(localPort)
			with open(localRoomName, 'r') as f:
				localRoomN = f.readline().strip()
			f.close()
			sftp.get(serverRoomToken, localRoomToken)
			with open(localRoomToken, 'r') as f:
				localRoomT = f.readline().strip()
			f.close()
			try:
				port = int(portstr)
			except ValueError:
				pass
			nameRoom = localRoomN
			tokenRoom = localRoomT
			host = ipofssh
			if nameRoom == roomName2 and tokenRoom == roomToken2:
				os.remove(localRoomName)
				os.remove(localRoomToken)
				def disconnect(): # Disconnect Function
					try:
						top1.destroy()
					except:
						pass
					roomMeeters.place_forget()
					roomwelcome.place_forget()
					scrollbar.pack_forget()
					scrollbar1.pack_forget()
					scrollbar2.pack_forget()
					scrollbar3.pack_forget()
					registerButton.pack(fill="x")
					loginButton.pack(fill="x")
					appTitle1.pack()
					appTitle.pack()
					appDesc.pack()
					msg_list.pack_forget()
					user_list.pack_forget()
					users_frame.place_forget()
					messages_frame.place_forget()
					entry_field.place_forget()
					disconnect_Button.place_forget()
					link_Button.place_forget()
					send_button.place_forget()
					menu.title("SecuRoom Stable v1.0 Release | Account: "+usernameofuser)
					menu.geometry("800x485")
					roomName1.place(x = 225, y = 250)
					room.place(x = 385, y = 250)
					connectRoomToken.place(x = 225, y = 300)
					room1.place(x = 385, y = 300)
					connectButton.place(x=223, y=360, height = 30, width = 340)
					accountManage.place(height = 65, width = 60,x = 725, y=420)

					connectButton['state'] = tkinter.NORMAL
					client_socket.close()
				def receive():# Receiving data from Server
					while True:
						t = time.localtime()
						current_time = time.strftime("[%H:%M]", t)
						try:
							msg = client_socket.recv(BUFSIZ).decode("utf8") # Receive data from the server.
							if msg == "8jhhaZaaq766712h5aaoaoaoaoppp17127477VVVAHAGgagx0Pz_12": # Send the username to the server.
								client_socket.send(usernameofuser.encode("utf8"))

							elif (msg.find("jkkasgjasg76666AJHAHAHxxxxCf") != -1): # File Sent Message
								gizliKod = msg.split("+")[0]
								sentFile = msg.split("+")[1]
								msg_list.insert("end", sentFile)
								msg_list.see("end")

							elif (msg.find("connected to room.") != -1): # New User Connected (Server)
								msg_to_print = msg.split("+")[0]
								online_users = msg.split("+")[1]
								user_list.delete(0,"end")

								for user in online_users.split(" "): # Printing new UserName on New Line
									user_list.insert("end",user)
								try:
									idx = user_list.get(0,"end").index("siddharthnk") # Highlighted Admin Name
									user_list.itemconfig(idx, {'fg':'red'})
								except:
									pass
								msg_list.insert("end",">> "+msg_to_print)
								msg_list.see("end")

							elif (msg.find("left the chat.") != -1): # User Left the Chat Message
								msg_to_print = msg.split("+")[0]
								userr = msg.split("+")[1]
								idx = user_list.get(0,"end").index(userr)
								user_list.delete(idx)
								msg_list.insert("end",">> "+msg_to_print)
								msg_list.see("end")
							elif msg.find("1J731JSG81jags881952kdpiSf18shj-123aasgxXAGa11_sfgCCCXXzzzz") != -1: # Prevents disconnection from Inactivity
								pass
							elif (msg.find("Welcome") != -1): # New User Connected (Client)
								try:
									msg_to_print = msg.split("+")[0]
									online_users = msg.split("+")[1]
									for user in online_users.split(" "):
										user_list.insert("end",user)
										try:
											idx = user_list.get(0,"end").index("siddharthnk") # Highlighted Admin Name
											user_list.itemconfig(idx, {'fg':'red'})
										except:
											pass
									msg_list.insert("end",msg_to_print)
									msg_list.see("end")
								except IndexError: 
									pass
							else:
								msg_list.insert("end",current_time+" "+msg) # Adding Time before all messages other than the ones above.
								msg_list.see("end")
						except OSError:
							break

							

				def linkImage(): # File Sharing Method
					def downloadfile(event=None):
						def downloadfileevent(event=None):
							try:
								filenameloc = filename.get()
								serverfilepath= sshhomepath+"/Server_Data/Rooms/"+nameRoom+"/media/"+filenameloc
								desktop = winshell.desktop()
								downloaddir = os.path.join(desktop, filenameloc)
								sftp = client.open_sftp()
								sftp.get(serverfilepath, downloaddir)
							except FileNotFoundError: # File not Found Error
								try:
									os.remove(downloaddir)
								except:
									pass
								upload_box.pack_forget()
								upload_dialog.pack_forget()
								descoffile1.title("Download Failed.")
								descoffile1.geometry("400x100")
								errLabel3 = tkinter.Label(descoffile1, text="\nFile not Found :(", font="Arial 15",bg = "#C3FFF2", fg = "red")
								errLabel3.pack()
								if activeTheme == "Dark":
									descoffile1.configure(bg = darkcolor)
									errLabel3.configure(bg = darkcolor,fg = "white")
								else:
									pass
							else: # The message that will appear when the download is successful.
								descoffile1.title("Downloaded Successfully")
								descoffile1.geometry("400x100")
								upload_box.pack_forget()
								upload_dialog.pack_forget()
								success_msg = tkinter.Label(descoffile1, text="\nFile has been saved to Desktop", font="Arial 15",bg = "#C3FFF2", fg = "green")
								success_msg.pack()
								if activeTheme == "Dark":
									descoffile1.configure(bg = darkcolor)
									success_msg.configure(bg = darkcolor,fg = "white")
								else:
									pass

						descoffile1 = tkinter.Toplevel(link, bg = "#C3FFF2") # File download screen.
						descoffile1.iconbitmap("Sources/icon.ico")
						descoffile1.title("Download File")
						descoffile1.geometry("540x150")
						filename = tkinter.StringVar()
						descoffile1.resizable(False, False)
						upload_box = tkinter.Label(descoffile1, text="\nType file name followed by extension.\nExample: picture.png\n", font="Arial 15",bg = "#C3FFF2", fg = "red")
						upload_box.pack()
						upload_dialog = tkinter.Entry(descoffile1, textvariable=filename,font = "Arial 15", width = 20, bd = 5)
						upload_dialog.bind("<Return>", downloadfileevent)
						upload_dialog.pack()

						if activeTheme == "Dark":
							descoffile1.configure(bg = darkcolor)
							upload_box.configure(bg = darkcolor,fg = "white")
							upload_dialog.configure(bg="#36393F",fg = "white")
						else:
							pass

					def openFileExplorer(): # Browse for File to Upload
						link.FileName = filedialog.askopenfilename(initialdir="C:/", title = "Send File", filetypes=(("PNG Files", "*.png"),("JPG Files", "*.jpg"),("MP4 Files", "*.mp4"), ("MP3 Files", "*.mp3")))
						if len(link.FileName) > 0:
							def set_up(event=None):
								localfile = link.FileName
								print(localfile)
								userDesc = userDescraw.get()
								serverMediaPath = sshhomepath+"/Server_Data/Rooms/"+nameRoom+"/media/"+userDesc
								sftp = client.open_sftp()
								try: # message if the file is uploaded.
									sftp.put(localfile, serverMediaPath)
									descalma2.pack_forget()
									descverme2.pack_forget()
									descoffile.title("File Uploaded")
									descoffile.geometry("520x90")
									success = tkinter.Label(descoffile, text="\nFile has been uploaded to the Server", font="Arial 15",bg = "#C3FFF2", fg = "green")
									uploadedFile = "kagsjhHYA"+"+"+usernameofuser+"+"+userDesc 
									client_socket.send(bytes(uploadedFile, "utf8"))
									success.pack()
									if activeTheme == "Dark":
										descoffile.configure(bg = darkcolor)
										success.configure(bg = darkcolor,fg = "white")
									else:
										pass
								except FileNotFoundError: # Error message that will appear if the file to upload cannot be found.
									error2 = tkinter.Toplevel(link, bg="#C3FFF2")
									error2.title("File Upload Failed.")
									error2.geometry("400x100")
									error2.resizable(False,False)
									error2.iconbitmap("Sources\\icon.ico")
									errormessage2 = tkinter.Label(error2, text="\nFile not Found :(", font="Arial 15",bg = "#C3FFF2", fg = "red")
									errormessage2.pack()
									if activeTheme == "Dark":
										error2.configure(bg = darkcolor)
										errormessage2.configure(bg = darkcolor,fg = "white")
									else:
										pass
							descoffile = tkinter.Toplevel(link, bg = "#C3FFF2") # Where to upload the file.
							descoffile.iconbitmap("Sources/icon.ico")
							descoffile.title("Set File Name")
							descoffile.geometry("550x200")
							descoffile.resizable(False, False)
							userDescraw = tkinter.StringVar()
							descalma2 = tkinter.Label(descoffile, text="\nEnter file name. Others will use this to download it.\nExample: picture.png\n", font="Arial 15",bg = "#C3FFF2", fg = "red")
							descalma2.pack()
							descverme2 = tkinter.Entry(descoffile, textvariable=userDescraw,font = "Arial 15", width = 20, bd = 5)
							descverme2.bind("<Return>", set_up)
							descverme2.pack()
							localfile = link.FileName
							if activeTheme == "Dark":
								descoffile.configure(bg = darkcolor)
								descalma2.configure(bg = darkcolor,fg = "white")
								descverme2.configure(bg="#36393F",fg = "white")
							else:
								pass
						else:
							pass
					link = tkinter.Toplevel(menu, bg = "#C3FFF2")# "Media Share" section.
					link.iconbitmap("Sources/icon.ico")
					link.title("Media Share")
					link.geometry("270x90")
					link.resizable(False, False)
					pngpath = tkinter.StringVar()
					uploadphoto = tkinter.PhotoImage(file=r"Sources/upload.png")
					upload_label = tkinter.Label(image = uploadphoto)
					upload_label.image=uploadphoto
					uploadFile = tkinter.Button(link,bg = "#C3FFF2", activebackground="#C3FFF2",height = 50,width = 50, image = uploadphoto, borderwidth = 0, command = openFileExplorer)
					uploadFile.place(x = 50,y=20)
					downloadphoto = tkinter.PhotoImage(file=r"Sources/download.png")
					download_label = tkinter.Label(image = downloadphoto)
					download_label.image=downloadphoto
					downloadFile = tkinter.Button(link,height = 50,width = 50, image = downloadphoto,bg = "#C3FFF2", activebackground="#C3FFF2", borderwidth = 0, command = downloadfile)
					downloadFile.place(x = 150,y = 20)
					if activeTheme == "Dark":
						downloadFile.configure(bg = darkcolor,activebackground=darkcolor)
						uploadFile.configure(bg = darkcolor, activebackground=darkcolor)
						link.configure(bg = darkcolor)
					else:
						pass
				def send(event=None): # Informing Server
					try:
						msg = my_msg.get()
						my_msg.set("")
						client_socket.send(bytes(msg, "utf8"))
					except OSError:
						pass
				def on_closing(event=None): # Close Window method
					try:
						connectButton['state'] = tkinter.NORMAL
						menu.destroy()
						client_socket.close()
						top1.destroy()
					except:
						pass
				
				# Discarding all buttons and Labels from the Main Menu

				registerButton.pack_forget()
				loginButton.pack_forget()
				appTitle1.pack_forget()
				appTitle.pack_forget()
				appDesc.pack_forget()
				roomName1.place_forget()
				room.place_forget()
				connectRoomToken.place_forget()
				room1.place_forget()
				accountManage.place_forget()
				connectButton.place_forget()

				# Building the Chat Room Window

				menu.title("SecuRoom | "+ nameRoom)
				menu.geometry('984x520')
				messages_frame = tkinter.Frame(menu)
				users_frame = tkinter.Frame(menu)
				scrollbar2 = tkinter.Scrollbar(users_frame)
				my_msg = tkinter.StringVar()
				my_msg.set("")
				scrollbar = tkinter.Scrollbar(messages_frame)
				scrollbar3 = tkinter.Scrollbar(users_frame, orient='horizontal')
				scrollbar1 = tkinter.Scrollbar(messages_frame, orient='horizontal')
				titleofroom = nameRoom.title()
				roomwelcome = tkinter.Label(menu, text = titleofroom+" Chat Window", font = "Consolas 15 bold", bg= "#C3FFF2", fg ="Purple")
				roomMeeters = tkinter.Label(menu, text = "Online Users", font = "Consolas 15 bold", bg= "#C3FFF2", fg ="Purple")
				roomMeeters.place(x=763,y=5)
				roomwelcome.place(x = 10, y= 5)
				user_list = tkinter.Listbox(users_frame, height = 20, width= 20,font = "Arial 13 bold", bd = 2, bg = "#E7FFFA",yscrollcommand=scrollbar2.set, xscrollcommand=scrollbar3.set)
				msg_list = tkinter.Listbox(messages_frame, height=20, width=80, font = "Arial 13", bd = 2, bg = "#E7FFFA", yscrollcommand=scrollbar.set, xscrollcommand=scrollbar1.set)
				scrollbar.config(command=msg_list.yview)
				scrollbar2.config(command=user_list.yview)
				scrollbar3.config(command=user_list.xview)
				scrollbar1.config(command=msg_list.xview)
				scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
				scrollbar3.pack(side=tkinter.BOTTOM, fill=tkinter.X)
				scrollbar2.pack(side=tkinter.RIGHT, fill=tkinter.Y)
				scrollbar1.pack(side=tkinter.BOTTOM, fill=tkinter.X)
				msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
				user_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
				users_frame.place(x=765,y=40)
				messages_frame.place(x=10,y=40)
				entry_field = tkinter.Entry(menu, textvariable=my_msg,font = "Arial 12", width = 70, bd = 5)
				entry_field.bind("<Return>", send)
				entry_field.place(x=62, y=480)
				gonder_buton = tkinter.PhotoImage(file='Sources/img.png')
				link_button = tkinter.PhotoImage(file="Sources/linkbutton.png")
				link_label = tkinter.Label(image = link_button)
				link_label.image=link_button
				disconnect_Button = tkinter.Button(menu,text = "Disconnect", borderwidth = 2,font = "Consolas 12 bold",fg = "white", bg = "#007CFF", activebackground = "light blue",  command = disconnect)
				disconnect_Button.place(x = 765,y = 476, height = 35, width=205)
				link_Button = tkinter.Button(menu,bg="#C3FFF2",activebackground="#C3FFF2", image = link_button, borderwidth = 0, command = linkImage)
				link_Button.place(x=711, y=475, height=40, width=45)
				img_label = tkinter.Label(image = gonder_buton)
				img_label.image = gonder_buton
				send_button = tkinter.Button(menu, image = gonder_buton,bg="#C3FFF2",activebackground="#C3FFF2", borderwidth = 0, command=send)
				send_button.place(x=12, y=475, height = 40, width = 45)

				# Theme adjustments

				if activeTheme == "Dark":
					send_button.configure(bg = darkcolor,activebackground=darkcolor)
					link_Button.configure(bg = darkcolor,activebackground=darkcolor)
					msg_list.configure(bg = "#36393F",fg="white")
					roomwelcome.configure(bg = darkcolor,fg = "white")
					roomMeeters.configure(bg = darkcolor,fg = "white")
					entry_field.configure(bg="#36393F",fg = "white")
					user_list.configure(bg = "#36393F",fg="white")
					disconnect_Button.configure(bg = "#151515",activebackground="#B4B4B4")
				else:
					pass

				menu.protocol("WM_DELETE_WINDOW", on_closing)
				BUFSIZ = 4096
				ADDR = (host, port)
				def join_room():
					global client_socket
					client_socket = socket(AF_INET, SOCK_STREAM)
					client_socket.connect(ADDR)
				
				try:
					join_room() #Trying to Join the Room
				except: #Room offline error
					top1 = tkinter.Toplevel(menu, bg = "#C3FFF2")
					top1.iconbitmap("Sources/icon.ico")
					top1.geometry("400x60")
					top1.resizable(False, False)
					top1.title("SecuRoom Connection Failed")
					top1.configure(background = "#C3FFF2")
					error = tkinter.Label(top1, text = "Room server offline.",font = "Consolas 15", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
					error.pack()
					exit_button = tkinter.Button(top1, text="Exit",font = "Consolas 10 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = disconnect)
					exit_button.pack()
					if activeTheme == "Dark":
						top1.configure(bg = darkcolor)
						error.configure(bg = darkcolor,fg = "white")
						exit_button.configure(bg = "#151515",activebackground="#B4B4B4")
					else:
						pass
				else:
					receive_thread = Thread(target=receive)
					receive_thread.start()
			else:
				def exitt():
					connectButton['state'] = tkinter.NORMAL
					error1.destroy()
				# Wrong Room Token Error
				error1 = tkinter.Toplevel(menu)
				error1.iconbitmap("Sources/icon.ico")
				error1.geometry("400x60")
				error1.resizable(False, False)
				error1.title("SecuRoom Failed to Connect")
				error1.configure(background = "#C3FFF2")
				os.remove(localRoomName)
				os.remove(localRoomToken)
				buton1 = tkinter.Label(error1, text = "Wrong Room Token.",font = "Consolas 15", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
				buton1.pack()
				cik = tkinter.Button(error1, text="Exit",font = "Consolas 10 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = exitt)
				cik.pack()
				if activeTheme == "Dark":
					error1.configure(bg = darkcolor)
					buton1.configure(bg = darkcolor,fg = "white")
					cik.configure(bg = "#151515",activebackground="#B4B4B4")
				else:
					pass

def manageAccount(event=None):

	def enableDarkTheme(): # Method that enables Dark Theme
		global activeTheme
		global darkcolor
		darkcolor = "#262626"
		activeTheme = "Dark"
		menu.configure(bg = darkcolor)
		appDesc.configure(bg = darkcolor)
		appTitle.config(bg = darkcolor)
		appTitle1.config(bg = darkcolor)
		accountManage.configure(bg = darkcolor,activebackground=darkcolor)
		loginButton.configure(bg = "#151515",activebackground="#B4B4B4")
		registerButton.configure(bg = "#151515",activebackground="#B4B4B4")
		connectButton.configure(bg = "#151515",activebackground="#B4B4B4")
		accountmanagement.configure(bg = darkcolor)
		theme_option.configure(bg = darkcolor, fg = "white")
		space.configure(bg = darkcolor,fg = "white")
		roomName1.configure(bg = darkcolor,fg = "white")
		connectRoomToken.configure(bg = darkcolor,fg = "white")
		logout.configure(bg = "#151515",activebackground="#B4B4B4")
		room.configure(bg = "#B4B4B4")
		room1.configure(bg = "#B4B4B4")

	def enableLightTheme(): # Method to activate Light Theme in Main Menu
		global activeTheme
		global lightcolor
		lightcolor = "#C3FFF2"
		activeTheme = "Light"
		menu.configure(bg = lightcolor)
		appTitle1.configure(bg = lightcolor)
		appTitle.configure(bg = lightcolor)
		appDesc.configure(bg = lightcolor)
		accountManage.configure(bg = lightcolor,activebackground=lightcolor)
		loginButton.configure(bg = "#007CFF",activebackground="White")
		registerButton.configure(bg = "#007CFF",activebackground="White")
		connectButton.configure(bg = "#007CFF", activebackground = "light blue")
		try:
			accountmanagement.configure(bg = lightcolor)
			space.configure(bg = lightcolor,fg = "Black")
			theme_option.configure(bg = lightcolor, fg = "black")
			logout.configure(bg = "#007CFF",activebackground="light blue")
		except:
			pass
		roomName1.configure(bg = lightcolor, fg = "black")
		connectRoomToken.configure(bg = lightcolor, fg = "black")
		room.configure(bg = "#D4FFF6")
		room1.configure(bg = "#D4FFF6")

	def logoutAccount(): # Logout Method
		Thread(target=enableLightTheme).start()
		accountmanagement.destroy()
		connectButton['state'] = tkinter.DISABLED
		loginButton['state'] = tkinter.NORMAL
		registerButton['state'] = tkinter.NORMAL
		menu.title("SecuRoom Launcher Stable v1.0")
		accountManage.place_forget()

	global accountmanagement

	# settings

	accountmanagement = tkinter.Toplevel(menu, bg = "#C3FFF2")
	accountmanagement.title("SecuRoom : Settings")
	accountmanagement.geometry("490x34")
	accountmanagement.resizable(False, False)
	accountmanagement.iconbitmap("Sources/icon.ico")
	theme_option = tkinter.Label(accountmanagement, text = "Theme: ", font = "Consolas 15 bold", bg = "#C3FFF2", fg = "Black")
	theme_option.grid(row=4,column=0)
	Dark_Theme = tkinter.Button(accountmanagement,text="Dark", width = 10, font = "Consolas 12 bold",bg = "#007CFF", activebackground="light blue",fg ="white",command = enableDarkTheme)
	Dark_Theme.configure(bg = "#151515",activebackground="#B4B4B4")
	Dark_Theme.grid(row=4,column=1)
	Light_Theme = tkinter.Button(accountmanagement,text="Light", width = 10, font = "Consolas 12 bold",bg = "#007CFF", activebackground="light blue",fg ="white",command = enableLightTheme)
	Light_Theme.grid(row=4,column=2)
	space = tkinter.Label(accountmanagement, text = "Account: ", font = "Consolas 15 bold", bg = "#C3FFF2", fg = "Black")
	space.grid(row=4,column=3)
	logout = tkinter.Button(accountmanagement,text="Logout", width = 10, font = "Consolas 12 bold",bg = "#007CFF", activebackground="light blue",fg ="white",command = logoutAccount)
	logout.grid(row=4,column=4,sticky ="E")
	if activeTheme == "Dark":
		theme_option.configure(bg = darkcolor, fg = "white")
		space.configure(bg = darkcolor,fg = "white")
		logout.configure(bg = "#151515",activebackground="#B4B4B4")
		accountmanagement.configure(bg = darkcolor)
	else:
		pass

def exitMain():
	try:
		client_socket.close()
		menu.destroy()
	except:
		menu.destroy()

menu = tkinter.Tk()
menu.configure(background = "#C3FFF2")
menu.title("SecuRoom Launcher Stable v1.0 Release")
menu.geometry("800x485")
menu.resizable(False, False)
menu.iconbitmap("Sources/icon.ico")

def register(): # User account creation step
	registerButton['state'] = tkinter.DISABLED # Disabling  the register button to prevent the user from spamming multiple registeration requests
	
	def confirmRegister():

		def exitRegister(event=None):
			registerButton['state'] = tkinter.NORMAL
			createAcc.destroy()
		
		# To hide input forms when result message (error or success) is shown 
		nickname.place_forget()
		nicknamentry.place_forget()
		password1.place_forget()
		passwordonentry.place_forget()
		password2.place_forget()
		passwordtwoentry.place_forget()
		cRegister.place_forget()
		
		# Storing inputted values in variables
		userNameC = requestedNickname.get()
		passwordfirst = passwordone.get()
		passwordsecond = passwordtwo.get()

		# Defining path to store New user Account Details
		userPath = sshhomepath+"/Server_Data/Users/"+userNameC+"/"
		sftp = paramiko.SFTPClient.from_transport(transport)
		try:
			sftp.chdir(userPath) # Changing SFTP Directory to the path stored in userPath Variable
		except IOError:
			if 4 > len(userNameC) or 12 < len(userNameC): # Checking username length condition
				createAcc.geometry("550x60")
				createAcc.title("Username Doesn't Meet The Conditions")
				errormessage6 = tkinter.Label(createAcc, text = "Username must be between 4 and 12 characters.",font = "Consolas 15", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
				errormessage6.pack()
				cikisg = tkinter.Button(createAcc, text="Exit",font = "Consolas 10 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = exitRegister)
				cikisg.pack()
			elif passwordfirst != passwordsecond: # Checking if both passwords entered are same
				createAcc.geometry("400x60")
				createAcc.title("Password Doesn't Meet The Conditions")
				errormessage5 = tkinter.Label(createAcc, text = "Passwords doesn't match.",font = "Consolas 15", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
				errormessage5.pack()
				cikisd = tkinter.Button(createAcc, text="Exit",font = "Consolas 10 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = exitRegister)
				cikisd.pack()
			elif 8 > len(passwordfirst) or 16<len(passwordfirst): # Checking password length condition
				createAcc.geometry("500x60")
				createAcc.title("Password Doesn't Meet The Conditions")
				errormessage4 = tkinter.Label(createAcc, text = "Password must be between 8 and 16 characters.",font = "Consolas 15", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
				errormessage4.pack()
				cikisc = tkinter.Button(createAcc, text="Exit",font = "Consolas 10 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = exitRegister)
				cikisc.pack()
			else:
				def registeredexit():
					registerButton['state'] = tkinter.NORMAL
					createAcc.destroy()

				key = Fernet.generate_key() # key generation
				with open('filekey.key', 'wb') as filekey: # storing key
					filekey.write(key)	

				key = open("filekey.key", "rb").read() # Reading Key
				fernet = Fernet(key)
				fernet = Fernet(key) # using the generated key

				sftp.mkdir(userPath) # Creating new folder for specified user
				encrypteduname = fernet.encrypt(userNameC.encode()) # encrypting the file
				encryptedpw = fernet.encrypt(passwordfirst.encode()) # encrypting the file

				# Running commands to create new files to store username and password and later encrypt them
				stdout, stdin, stderr = client.exec_command('cd Server_Data;cd Users;cd '+userNameC+';echo ' + encryptedpw.decode() + ' > userPassword.txt;echo '+ encrypteduname.decode()+'> userName.txt')
				# stdout, stdin, stderr = client.exec_command('cd Server_Data;cd Users; python3 encrypt.py ' +userNameC+  )
				createAcc.geometry("500x60")
				createAcc.title("Account Created")
				mesaj = tkinter.Label(createAcc, text = "Created Account! You can login.",font = "Consolas 15", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
				mesaj.pack()
				cikisf = tkinter.Button(createAcc, text="Exit",font = "Consolas 10 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = registeredexit)
				cikisf.pack()

		else: # Error message if the username already exists or is left blank.
			createAcc.geometry("500x100")
			createAcc.title("Username Exists")
			errormessage3 = tkinter.Label(createAcc, text = "Username already exists,\nor reserved for system.",font = "Consolas 15", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
			errormessage3.pack()
			cikisb = tkinter.Button(createAcc, text="Exit",font = "Consolas 10 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = exitRegister)
			cikisb.pack()

	def exitRegister1(event=None):
		registerButton['state'] = tkinter.NORMAL
		createAcc.destroy()

	# Building Registeration Form Window	
	createAcc = tkinter.Toplevel(menu, bg="#C3FFF2")
	createAcc.title("Register")
	createAcc.geometry("500x250")
	createAcc.resizable(False, False)
	createAcc.iconbitmap("Sources/icon.ico")
	nickname = tkinter.Label(createAcc, text="Username: ",bg = "#C3FFF2", font = "Arial 17 bold")
	nickname.place(x=85,y=20)
	requestedNickname = tkinter.StringVar()
	nicknamentry = tkinter.Entry(createAcc,width = 15, textvariable = requestedNickname, bd = 5,bg = "#D4FFF6", font = "Arial 15")
	nicknamentry.place(x=220,y=20)
	password1 = tkinter.Label(createAcc, text="Password: ",bg = "#C3FFF2", font = "Arial 17 bold")
	password1.place(x=85,y=65)
	passwordone = tkinter.StringVar()
	passwordonentry = tkinter.Entry(createAcc,width = 15, textvariable = passwordone, bd = 5,bg = "#D4FFF6", font = "Arial 15", show="*")
	passwordonentry.place(x=220,y=65)
	password2 = tkinter.Label(createAcc, text="Password: ",bg = "#C3FFF2", font = "Arial 17 bold")
	password2.place(x=85,y=110)
	passwordtwo = tkinter.StringVar()
	passwordtwoentry = tkinter.Entry(createAcc,width = 15, textvariable = passwordtwo, bd = 5,bg = "#D4FFF6", font = "Arial 15", show="*")
	passwordtwoentry.place(x=220,y=110)
	createAcc.protocol("WM_DELETE_WINDOW",exitRegister1)
	cRegister = tkinter.Button(createAcc, text="Register", borderwidth=4,font="Consolas 15 bold", width=10,fg = "white", bg = "#007CFF", activebackground = "light blue", command=confirmRegister)
	cRegister.place(x = 195, y = 175)

def login(): # Login
	loginButton['state'] = tkinter.DISABLED
	def confirmLogin():
		def selam():
			loginButton['state'] = tkinter.NORMAL
			loginAcc.destroy()
		nickName.place_forget()
		checkUsername1.place_forget()
		checkpassword.place_forget()
		checkpassword1.place_forget()
		cLogin.place_forget()
		global appdata
		global usernameofuser
		appdata = os.getenv("APPDATA")
		usernameofuser = checkUsername.get()
		passwordofuser = passwordone1.get()
		serverLoginUserPath = sshhomepath + "/Server_Data/Users/" + usernameofuser +"/"
		serverPasswordPath= sshhomepath+"/Server_Data/Users/"+usernameofuser+"/userPassword.txt"
		localPasswordPath = appdata+"/checkPassword.txt"
		try:
			sftp.chdir(serverLoginUserPath)
		except FileNotFoundError: # error message that will appear if no account is found.
			loginAcc.title("Can't Find User")
			loginAcc.geometry("420x100")
			errormessage8 = tkinter.Label(loginAcc, text = "Can't find user.\nYou can register for free!",font = "Consolas 14", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
			errormessage8.pack()
			cikish = tkinter.Button(loginAcc, text="Exit", width = 5,font = "Consolas 12 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = selam)
			cikish.pack()
		else:
			try:
				sftp.get(serverPasswordPath, localPasswordPath)
				print(sftp.get(serverPasswordPath, localPasswordPath))
			except FileNotFoundError: # error message will appear if no account is found.
				loginAcc.title("Can't Find User")
				loginAcc.geometry("420x100")
				errormessage8 = tkinter.Label(loginAcc, text = "Can't find user.\nYou can register for free!",font = "Consolas 14", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
				errormessage8.pack()
				cikish = tkinter.Button(loginAcc, text="Exit", width = 5,font = "Consolas 12 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = selam)
				cikish.pack()
			else:
				with open(localPasswordPath, 'r') as f:
					passwordchecking = f.readline().strip()
				f.close()
				os.remove(localPasswordPath)
			try:
				key = open("filekey.key", "rb").read() # Reading Key
				fernet = Fernet(key)
				decrypted = fernet.decrypt(passwordchecking)
				passwordchecking = decrypted.decode()
							
				if passwordofuser == passwordchecking: # After logging in the settings button is activated.

					settings_photo = tkinter.PhotoImage(file="Sources/settings.png")
					settings_label = tkinter.Label(image = settings_photo)
					settings_label.image=settings_photo
					global accountManage
					accountManage = tkinter.Button(menu, image = settings_photo,bg = "#C3FFF2", activebackground="#C3FFF2", borderwidth = 0, command = manageAccount)
					accountManage.place(height = 65, width = 60,x = 725, y=420)
					if activeTheme == "Dark":
						accountManage.configure(bg = darkcolor)
					else:
						pass

					def exitlogs():

						loginAcc.destroy()

					# successful login
					menu.title("SecuRoom Launcher Stable v1.0 Release | Account: "+usernameofuser)
					registerButton['state'] = tkinter.DISABLED
					loginButton['state'] = tkinter.DISABLED
					connectButton['state'] = tkinter.NORMAL
					loginAcc.title("Logged In")
					loginAcc.geometry("300x65")
					errormessage9 = tkinter.Label(loginAcc, text = "Welcome "+usernameofuser+",\nnow you can join to the rooms.\n",font = "Consolas 13", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
					errormessage9.pack()
					loginAcc.protocol("WM_DELETE_WINDOW", exitlogs)
				else: # Wrong password
					loginAcc.title("Login Failed")
					loginAcc.geometry("300x65")
					errormessage10 = tkinter.Label(loginAcc, text = "Wrong password!",font = "Consolas 15", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
					errormessage10.pack()
					cikish = tkinter.Button(loginAcc, text="Exit",font = "Consolas 10 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = selam)
					cikish.pack()
			except UnboundLocalError:
				pass

	def exitLogged(event=None):

		loginButton['state'] = tkinter.NORMAL
		loginAcc.destroy()

	loginAcc = tkinter.Toplevel(menu, bg="#C3FFF2")
	loginAcc.title("Login")
	loginAcc.geometry("500x180")
	loginAcc.resizable(False, False)
	loginAcc.iconbitmap("Sources/icon.ico")
	nickName = tkinter.Label(loginAcc, text="Username: ", bg = "#C3FFF2", font = "Arial 17 bold")
	nickName.place(x=85,y=20)
	checkUsername = tkinter.StringVar()
	checkUsername1 = tkinter.Entry(loginAcc,width = 15, textvariable = checkUsername, bd = 5,bg = "#D4FFF6", font = "Arial 15")
	checkUsername1.place(x=220,y=20)
	checkpassword = tkinter.Label(loginAcc, text="Password: ",bg = "#C3FFF2", font = "Arial 17 bold")
	checkpassword.place(x=85,y=65)
	passwordone1 = tkinter.StringVar()
	checkpassword1 = tkinter.Entry(loginAcc,width = 15, textvariable = passwordone1, bd = 5,bg = "#D4FFF6", font = "Arial 15", show="*")
	checkpassword1.place(x=220,y=65)
	cLogin = tkinter.Button(loginAcc, text="Login", borderwidth=4,font="Consolas 15 bold", width=10,fg = "white", bg = "#007CFF", activebackground = "light blue", command=confirmLogin)
	cLogin.place(x = 195, y = 115)

	loginAcc.protocol("WM_DELETE_WINDOW", exitLogged)

# Main menu
# Building Main Screen GUI

registerButton = tkinter.Button(menu, text="Register", borderwidth=4,font="Consolas 15 bold", width=10,fg = "white", bg = "#007CFF", activebackground = "light blue", command=register)
registerButton.pack(fill="x")
loginButton = tkinter.Button(menu, text="Login", borderwidth=4,font="Consolas 15 bold", width=10,fg = "white", bg = "#007CFF", activebackground = "light blue", command=login)
loginButton.pack(fill="x")
appTitle1 = tkinter.Label(menu, text="", bg="#C3FFF2", font="Arial 25 bold")
appTitle1.pack()
appTitle = tkinter.Label(menu, text="SecuRoom Chat Application", bg="#C3FFF2", font="Arial 25 bold", fg="red")
appTitle.pack()

roomName1 = tkinter.Label(menu, text="Room Name: ",bg = "#C3FFF2", font = "Arial 17 bold")
roomName1.place(x = 225, y = 250)
roomNameConnect = tkinter.StringVar()
room = tkinter.Entry(menu,width = 15, textvariable = roomNameConnect, bd = 5,bg = "#D4FFF6", font = "Arial 15")
room.place(x = 385, y = 250)
connectRoomToken = tkinter.Label(menu, text="Room Token: ",bg = "#C3FFF2", font = "Arial 17 bold")
connectRoomToken.place(x = 225, y = 300)
roomTokenConnect = tkinter.StringVar()
room1 = tkinter.Entry(menu,width = 15, textvariable = roomTokenConnect, bd = 5,bg = "#D4FFF6", font = "Arial 15", show="*")
room1.place(x = 385, y = 300)

connectButton = tkinter.Button(menu, text="Connect",borderwidth=4,font = "Consolas 15 bold", width=10,fg = "white", bg = "#007CFF", activebackground = "light blue", command=connectRoomServer)
connectButton.place(x=223, y=360, height = 30, width = 340)
connectButton['state'] = tkinter.DISABLED

appDesc = tkinter.Label(menu, text="SecuRoom Stable v1.0 Release\n Created by Group F CCBT", bg="#C3FFF2", font="Arial 20", fg="red")
appDesc.pack()

menu.protocol("WM_DELETE_WINDOW", exitMain)

# Calling Connect Main function. This function checks if a SSH connection can be established using the Crednetials Provided.
# ConnectMain()

ConnectMain()
tkinter.mainloop()
