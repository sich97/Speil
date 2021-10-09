# Public packages
import zmq

# Private packages
from networking import transmission, client_communication
from utils import ini_manager

SETTINGS_PATH = "settings.ini"

connections = {"0": "Placeholder"}


def main():
    # Load preferences
    preferences = ini_manager.get_ini(SETTINGS_PATH)
    server_bind_address = "tcp://" + preferences["default"]["bind_address"] + ":" + preferences["default"]["bind_port"]

    # Initialize listener
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(server_bind_address)

    # Process connections indefinitely
    while True:
        # Accept connection, if any, and de-pickle it
        message = transmission.recv_zipped_pickle(socket)
        payload_connection_id = message["connection_id"]
        payload_type = message["type"]
        payload_data = message["data"]

        reply = ""

        if payload_type == "register":
            # Expected data format: {name: CLIENT-NAME, password: CLIENT-PASSWORD, server_password: SERVER-PASSWORD}
            if payload_data.pop("server_password") == preferences["default"]["password"]:
                new_connection_id = str(int(list(connections.keys())[-1]) + 1)
                connections[new_connection_id] = client_communication.Connection(new_connection_id, payload_data)
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
                    reply = client_communication.close_connection(payload_connection_id)

                elif payload_type == "get_available_streams":
                    # Expected data format: NONE
                    reply = client_communication.get_available_clients(connections)

                elif payload_type == "start_stream":
                    # Expected data format: TARGET-CONNECTION-ID
                    target_connection = connections[payload_data]
                    reply = target_connection.start_stream()

                elif payload_type == "stream_started":
                    # Expected data format: NONE
                    reply = origin_connection.stream_started()

                elif payload_type == "update_frame_info":
                    # Expected data format: frame_info_pickle
                    reply = origin_connection.update_frame_info(payload_data)

                elif payload_type == "get_frame_info":
                    # Expected data format: TARGET-CONNECTION-ID
                    target_connection = connections[payload_data]
                    reply = target_connection.get_frame()

        transmission.send_zipped_pickle(socket, reply)


if __name__ == "__main__":
    main()
