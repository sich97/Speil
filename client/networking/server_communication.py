from .transmission import send_zipped_pickle, recv_zipped_pickle


def get_pending_command(socket, connection_id):
    send_zipped_pickle(socket, {"connection_id": connection_id, "type": "get_pending_command", "data": None})
    reply_status, reply_data = recv_zipped_pickle(socket)
    if reply_status == 0:
        print(reply_data)
        return False
    elif reply_status == 1:
        return reply_data


def execute_command(socket, connection_id, command):
    if command == "start_stream":
        start_stream(socket, connection_id)

    elif command == "stop_stream":
        stop_stream(socket, connection_id)


def start_stream(socket, connection_id):
    pass


def stop_stream(socket, connection_id):
    pass


def get_available_clients(socket, connection_id):
    send_zipped_pickle(socket, {"connection_id": connection_id, "type": "get_available_clients", "data": None})
    reply_status, reply_data = recv_zipped_pickle(socket)
    if reply_status == 0:
        print("Some unknown error occurred on the server")
        return {}
    elif reply_status == 1:
        return reply_data
