from .transmission import send_zipped_pickle, recv_zipped_pickle


def connect_to_server(parent, server_address, password):
    # Establish connection
    server_address = "tcp://" + server_address
    parent.socket.connect(server_address)

    # Authenticate
    payload_data = {"name": parent.preferences.preferences["authentication"]["client_id"],
                    "password": parent.preferences.preferences["authentication"]["client_password"],
                    "server_password": password}
    payload = {"connection_id": "none", "type": "register", "data": payload_data}
    send_zipped_pickle(parent.socket, payload)

    reply = recv_zipped_pickle(parent.socket)
    print(reply)
    if reply.lower().startswith("error"):
        parent.socket.close()
        return reply
    else:
        parent.connection_id = reply
        return "Authentication successful!"
