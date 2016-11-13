"""Module responsible for the communication with the App."""

import json
from threading import Thread

from bluetooth import *
from configuration import Configuration
import db

TAG = "PireworksServer"
UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

class BackEnd():
    """Controls the bluetooth server."""
    def __init__(self):
        self.thread = None
        db.setup()

    def start(self):
        """Starts the backend server."""
        self.thread = BluetoothServer(self.callback)
        self.thread.start()

    def stop(self):
        """Stop the backend server."""
        if self.thread is not None:
            self.thread.stop()
        self.thread = None
        
    def register(self, callback):
        """Register a save config callback function.
        Parameters
        ----------
        callback : function(Configuration)
            The callback that will be called each time a new
            Pireworks Configuration is to be applied.
        """
        self.callback = callback


class BluetoothServer(Thread):
    """The backend bluetooth server."""

    def __init__(self, callback):
        """The server constructor."""
        Thread.__init__(self)
        self.server_sock = BluetoothSocket(RFCOMM)
        self.callback = callback
        self.running = False
        
    def stop(self):
        """Stop the currently running thread"""
        self.running = False
    
    def run(self):
        """Starts the bluetooth server."""
        self.running = True
        self.server_sock.bind(("",PORT_ANY))
        self.server_sock.listen(1)
        advertise_service(self.server_sock, TAG,
                        service_id = UUID,
                        service_classes = [UUID, SERIAL_PORT_CLASS],
                        profiles = [SERIAL_PORT_PROFILE],)

        while self.running:
            print("Waiting for client to connect...")
            self.client_sock, self.client_info = self.server_sock.accept()
            print("Accepted connection from " + str(self.client_info))

            try:
                while True:
                    data = self.client_sock.recv(1024)
                    self.handle_message(data)
            except IOError:
                pass

        self.client_sock.close()
        self.server_sock.close()
        print("disconnected")

    def handle_message(self, data):
        """Handles a message sent from the client."""
        if len(data) == 0: 
            return

        # TODO:
        # data = json.load(data)
        # check message tepe (get / set)
        # if get, return default Configuration
        # if set, get the db.saveConfiguration(Configuration(data["config"]))
        #   and call callback.

        config = db.getDefaultConfiguration()
        self.client_sock.send(config.toJson())

        if self.callback is not None:
            self.callback(config)