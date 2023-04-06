import socketio


class Receiver:
    sio = socketio.Client()

    # this defines if the code should no longer be run
    running = True

    # this is the status codes for the test
    err = [0]

    # people currently typing
    people_typing = []

    # all the basics required to connect to the server
    def __init__(self, ip_address: str, port: int, secure_connection: bool):
        self.error = False
        port = str(port)
        if secure_connection:
            self.connector = f"https://{ip_address}:{port}"
        else:
            self.connector = f"http://{ip_address}:{port}"

    # this sets up the connection to the server
    def setup(self):
        self.sio_callbacks()
        try:
            self.sio.connect(self.connector)
        except socketio.exceptions.ConnectionError:
            print("error connecting")
            exit(1)

    def stop(self):
        self.dc()
        print("stopped")
        exit(0)

    # all socket-io events are defined here
    # no sender functions are defined here.
    def sio_callbacks(self):
        @self.sio.event
        def connect():
            print('ready to start testing')

        @self.sio.event
        def connect_error(data):
            print(f"there was an error in connection: {data}")
            self.error = True
            self.err[0] += 1

        @self.sio.event
        def disconnect():
            print('disconnected from server')

        @self.sio.on("new_message")
        def on_message(message, username, time):
            print(f"{username} said: {message} at {time}")

        @self.sio.on("user_typing")
        def on_type(username):
            print(f"{username} is typing")

        @self.sio.on("user_not_typing")
        def on_type(username):
            print(f"{username} is not typing")

    def dc(self):
        self.sio.disconnect()
