import socketio
import time


class Sender:
    sio = socketio.Client()

    # this defines if the code should no longer be run
    running = True

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
    def run(self):
        try:
            print("attempting message sending, waiting 5 seconds.")
            while self.running:
                current_time = time.time()
                self.sio.emit('send_message', (f'message was able to send at {current_time}', 'test_user'))
                if self.error:
                    self.error = False
                    print("there was an error: successful count is now 0")
                    if self.status[1] == 3:
                        print("too many errors, terminated")
                        exit(1)
                    continue
                else:
                    self.status[0] += 1
                    print(f"successful test count is {self.status[0]}")
                    self.status[1] = 0
                time.sleep(5)
            else:
                self.sio.disconnect()
                print("ended testing")
        except KeyboardInterrupt:
            self.sio.disconnect()
            print("ended testing")

    # all socket-io events are defined here
    # because this testing module is more focused on
    # sending messages rather than receiving them
    # the callbacks for receiving messages are not defined
    # and the connection callbacks are defined.
    def sio_callbacks(self):
        @self.sio.event
        def connect():
            print('ready to start testing')

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
