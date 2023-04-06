from functions import send, type, receive

# make a prompt that will ask for the ip address and username
ip_address = input("ip address: ")
port = int(input("port: "))
username = input("username: ")
secure_connection = input("secure connection? (y/n): ")
if secure_connection == "y":
    secure_connection = True
else:
    secure_connection = False

# create send and type objects
send = send.Sender(ip_address, port, username, secure_connection)
typer = type.Typer(ip_address, port, username, secure_connection)

# create a receiver instance
receive = receive.Receiver(ip_address, port, secure_connection)
# setup receiver
receive.setup()
send.setup()
typer.setup()

# ask the user what they want to do
while True:
    action = input("action: ")
    if action == "send":
        send.run()
    elif action == "type":
        typer.type()
    elif action == "untype":
        typer.untype()
    elif action == "dc":
        send.dc()
        typer.dc()
    elif action == "exit":
        send.dc()
        typer.dc()
        break
    else:
        print("error: invalid action")

# close the connection
send.dc()
typer.dc()




