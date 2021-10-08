import configparser
import zmq
import json

PREFERENCES_PATH = "preferences.ini"

connections = {"0": "Placeholder"}


def main():
    # Load preferences
    preferences = get_preferences()
    server_bind_address = "tcp://" + preferences["default"]["bind_address"] + preferences["default"]["bind_port"]

    # Initialize listener
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(server_bind_address)

    # Process connections indefinitely
    while True:
        # Accept connection, if any, and convert message to json
        message = json.loads(socket.recv_string())
        payload_connection_id = message["connection_id"]
        payload_type = message["type"]
        payload_data = message["data"]

        reply = ""

        if payload_type == "register":
            # Expected data format: {name: CLIENT-NAME, password: CLIENT-PASSWORD, server_password: SERVER-PASSWORD}
            registration_data = json.loads(payload_data)
            if registration_data.pop("server_password") == preferences["default"]["password"]:
                new_connection_id = str(int(list(connections.keys())[-1]) + 1)
                connections[new_connection_id] = Connection(new_connection_id, registration_data)
                reply = new_connection_id
            else:
                reply = "Error: authentication unsuccessful!"

        else:
            if payload_connection_id not in connections:
                reply = "Error: connection_id not recognized!"

            else:
                origin_connection = connections[payload_connection_id]

                if payload_type == "close_connection":
                    # Expected data format: NONE
                    reply = close_connection(payload_connection_id)

                elif payload_type == "get_available_streams":
                    # Expected data format: NONE
                    reply = get_available_clients()

                elif payload_type == "start_stream":
                    # Expected data format: TARGET-CONNECTION-ID
                    target_connection = connections[payload_data]
                    reply = target_connection.start_stream()

                elif payload_type == "stream_started":
                    # Expected data format: NONE
                    reply = origin_connection.stream_started()

                elif payload_type == "update_frame_info":
                    # Expected data format: {image: IMAGE-AS-STRING, cursor_pos: CURSOR-POSITION}
                    reply = origin_connection.update_frame_info(payload_data)

                elif payload_type == "get_frame_info":
                    # Expected data format: TARGET-CONNECTION-ID
                    target_connection = connections[payload_data]
                    reply = target_connection.get_frame()

        socket.send(reply)


class Connection:
    connection_id = None
    name = None
    password = None

    is_streaming = False
    frame = None
    cursor_pos = None

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

    def update_frame_info(self, frame_info):
        self.frame = frame_info["image"]
        self.cursor_pos = frame_info["cursor_pos"]
        return "update_frame_info function finished"

    def get_frame_info(self):
        return json.dumps({"image": self.frame, "cursor_pos": self.cursor_pos})


def close_connection(connection_id):
    return "close_connection function not developed yet!"


def get_available_clients():
    available_clients = {}
    for connection in connections:
        info = [connections[connection].name, connections[connection].is_streaming]
        available_clients[connection] = info
    return json.dumps(available_clients)


def get_preferences():
    config = configparser.ConfigParser()
    config.read(PREFERENCES_PATH)

    sections_dict = {}

    # Get all defaults
    defaults = config.defaults()
    temp_dict = {}
    for key in defaults:
        temp_dict[key] = defaults[key]

    sections_dict['default'] = temp_dict

    # Get sections and iterate over each
    sections = config.sections()

    for section in sections:
        options = config.options(section)
        temp_dict = {}
        for option in options:
            temp_dict[option] = config.get(section, option)

        sections_dict[section] = temp_dict

    return sections_dict


if __name__ == "__main__":
    main()
