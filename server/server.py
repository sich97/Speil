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

        reply_status = 0
        reply_data = ""

        if payload_type == "register":
            # Expected data format: {name: CLIENT-NAME, password: CLIENT-PASSWORD, server_password: SERVER-PASSWORD}
            if payload_data.pop("server_password") == preferences["default"]["password"]:
                new_connection_id = int(list(connections.keys())[-1]) + 1
                connections[str(new_connection_id)] = client_communication.Connection(new_connection_id, payload_data)
                reply_status, reply_data = 1, new_connection_id
            else:
                reply_status, reply_data = 0, "Authentication unsuccessful"

        else:
            if str(payload_connection_id) not in connections:
                reply_status, reply_data = 0, "Connection ID not recognized"

            else:
                origin_connection = connections[str(payload_connection_id)]

                if payload_type == "close_connection":
                    # Expected data format: NONE
                    reply_status,\
                     reply_data = client_communication.close_connection(connections[str(payload_connection_id)])

                elif payload_type == "get_available_streams":
                    # Expected data format: NONE
                    reply_status, reply_data = client_communication.get_available_clients(connections)

                elif payload_type == "start_stream":
                    # Expected data format: TARGET-CONNECTION-ID
                    target_connection = connections[str(payload_data)]
                    reply_status, reply_data = target_connection.start_stream()

                elif payload_type == "stop_stream":
                    # Expected data format: TARGET-CONNECTION-ID
                    target_connection = connections[str(payload_data)]
                    reply_status, reply_data = target_connection.stop_stream()

                elif payload_type == "stream_started":
                    # Expected data format: NONE
                    reply_status, reply_data = origin_connection.stream_started()

                elif payload_type == "stream_stopped":
                    # Expected data format: NONE
                    reply_status, reply_data = origin_connection.stream_stopped()

                elif payload_type == "update_frame_info":
                    # Expected data format: frame_info_pickle
                    reply_status, reply_data = origin_connection.update_frame_info(payload_data)

                elif payload_type == "get_frame_info":
                    # Expected data format: TARGET-CONNECTION-ID
                    target_connection = connections[str(payload_data)]
                    reply_status, reply_data = target_connection.get_frame()

                elif payload_type == "get_pending_command":
                    # Expected data format: NONE
                    reply_status, reply_data = origin_connection.get_pending_command()

        transmission.send_zipped_pickle(socket, (reply_status, reply_data))


if __name__ == "__main__":
    main()
