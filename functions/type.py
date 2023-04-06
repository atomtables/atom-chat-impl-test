import socketio
import time


class Typer:
    sio = socketio.Client()

    # this defines if the code should no longer be run
    typing = False

    # this is the status codes for the test
    status = [0,  # number of success
              0]  # number of failure

    # all the basics required to connect to the server
    def __init__(self, ip_address: str, port: int, username: str, secure_connection: bool):
        self.error = None
        port = str(port)
        if secure_connection:
            self.connector = f"https://{ip_address}:{port}"
        else:
            self.connector = f"http://{ip_address}:{port}"
        self.username = username

    # this sets up the connection to the server
    def setup(self):
        self.sio_callbacks()
        try:
            self.sio.connect(self.connector)
        except socketio.exceptions.ConnectionError:
            print("error connecting")
            exit(1)

    # these are the main functions of the program
    def type(self):
        if not self.typing:
            print("starting a type process")
            self.sio.emit("client_typing", self.username)
            self.typing = True
        else:
            print("error: already typing")

    def untype(self):
        if self.typing:
            print("ending type process")
            self.sio.emit("no_client_typing", self.username)
            self.typing = False
        else:
            print("error: not typing")

    # all socket-io events are defined here
    # because this testing module is more focused on
    # sending messages rather than receiving them
    # the callbacks for receiving messages are not defined
    # and the connection callbacks are defined.
    def sio_callbacks(self):
        @self.sio.event
        def connect():
            print('ready to start forging typing')

        @self.sio.event
        def connect_error(data):
            print(f"there was an error in connection: {data}")
            self.error = True
            self.status[1] += 1
            self.status[0] = 0

        @self.sio.event
        def disconnect():
            print('disconnected from server')

    def dc(self):
        self.sio.disconnect()


