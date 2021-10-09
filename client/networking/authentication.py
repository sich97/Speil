from .transmission import send_zipped_pickle, recv_zipped_pickle


def connect_to_server(parent, server_address, password):
    # Establish connection
    server_address = "tcp://" + server_address
    parent.socket.connect(server_address)

    # Authenticate
    payload_data = {"name": parent.window_preferences.preferences["authentication"]["client_id"],
                    "password": parent.window_preferences.preferences["authentication"]["client_password"],
                    "server_password": password}
    payload = {"connection_id": "none", "type": "register", "data": payload_data}
    send_zipped_pickle(parent.socket, payload)

    reply_status, reply_data = recv_zipped_pickle(parent.socket)
    if reply_status == 0:
        parent.socket.disconnect(server_address)
        return False, reply_data
    elif reply_status == 1:
        parent.connection_id = reply_data
        return True, reply_data
