import json


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
        return "start_stream function finished"

    def stream_started(self):
        self.pending_commands.remove("start_stream")
        return "stream_started function finished"

    def update_frame_info_pickle(self, frame_info_pickle):
        self.frame_info_pickle = frame_info_pickle
        return "update_frame_info function finished"

    def get_frame_info_pickle(self):
        return self.frame_info_pickle


def close_connection(connection_id):
    return "close_connection function not developed yet!"


def get_available_clients(connections):
    available_clients = {}
    for connection in connections:
        info = [connections[connection].name, connections[connection].is_streaming]
        available_clients[connection] = info
    return json.dumps(available_clients)
