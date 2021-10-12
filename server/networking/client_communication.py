class Connection:
    connection_id = None
    name = None
    password = None

    is_streaming = False
    frame_info_pickle = None

    pending_commands = []

    def __init__(self, connection_id, registration_data):
        self.connection_id = connection_id
        self.name = registration_data["name"]
        self.password = registration_data["password"]

    def start_stream(self):
        self.pending_commands.append("start_stream")
        return 1, "starting stream"

    def stop_stream(self):
        self.pending_commands.append("stop_stream")
        return 1, "stopping stream"

    def stream_started(self):
        self.is_streaming = True
        return 1, "stream started"

    def stream_stopped(self):
        self.is_streaming = False
        return 1, "stream stopped"

    def update_frame_info_pickle(self, frame_info_pickle):
        self.frame_info_pickle = frame_info_pickle
        return 1, "frame info updated"

    def get_frame_info_pickle(self):
        return 1, self.frame_info_pickle

    def get_pending_command(self):
        if len(self.pending_commands) > 0:
            return 1, self.pending_commands.pop(0)
        else:
            return 0, "no pending commands"


def close_connection():
    return 0, "close_connection function not developed yet!"


def get_available_clients(connections):
    available_clients = {}
    for connection in connections:
        if connection != "0":
            info = [connections[connection].name, connections[connection].is_streaming]
            available_clients[connection] = info
    return 1, available_clients
