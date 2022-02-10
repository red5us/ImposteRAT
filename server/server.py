from socket import *
from server_logic import *
import threading as thread
from gui import *

# Setup
server = socket(AF_INET, SOCK_STREAM)  # Define the server socket type
server.bind(("", 5555))  # Configure the server ip address and port
server.listen(100)  # listien to max of 100 endpoints
clients = []  # list of online hosts

# This funcation stop the server.


def stop_server():
    for x in range(0, len(clients)):
        clients[x][0].close()
    server.close()

# This funcation handles all the commands the server gives.
# every commnds that has been chosen has a function of its own


def communication():
    menu()
    try:
        while True:
            try:
                command = input('[' + '\033[31m' + 'Menu' + '\033[0m' ']:> ')
                if command == "1":
                    list_of_clients(clients)  # List Conncted Clients
                elif command == "2":
                    run_commands(clients)  # Run Server Commands
                elif command == "3":
                    stop_server()  # Stop Server from running
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


def listen_for_new_clients():
    try:
        while (True):
            client, address = server.accept()
            clients.append([client, address])
    except:
        pass


if __name__ == '__main__':
    t = thread.Thread(target=listen_for_new_clients,)
    t.start()  # Start listening
    communication()  # Server Starts Menu and Communication
