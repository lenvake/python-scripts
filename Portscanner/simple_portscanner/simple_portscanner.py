######################################
#Copyright of David lenvake, 2022             
######################################
import socket
import termcolor #in order to print some statements in diffrent colours

def scan(target, ports):
        print('\n' + ' Start the Scan for ' + str(target))
        for port in range(1,ports): #this will iterate from one to any number that was specified(look down in the code)
                scan_port(target,port) #call for every number the scan port function

def scan_port(ipaddress, port):
    try:                           
    #to figure out wheter a certain Port is closed or opened
    #--> using try and except statement
            sock = socket.socket() #it will try to initiate the socket object
            sock.connect((ipaddress, port)) #trying to connect to a certain port/ip-adress
            print("[+] Port is open" + str(port))
            sock.close()

    except:
            pass #so that the closed ports are not displayed
targets = input("[*] Enter the targets IP:" )
ports = int(input("[*] How many ports do you want to scan?:"))
if ',' in targets:
    print(termcolor.colored(("[*] Going to scan multiple targets"), 'green')) 
    for ip_addr in targets.split(','): #simply splits the input that was specified
        scan(ip_addr.strip(' '), ports)
else:
        scan(targets,ports)
