# TODO:
1. Combine Streamer and StreamViewer into a client.py file, with startup arguments determining whether to stream or view
2. Create a GUI to control such settings on the fly (startup parameters should override saved settings)
3. Develop a system for sending commands between clients (Start, stop, mouse_event, keyboard_event, clipboard)
4. Create the centralized server which relays all traffic (stream + commands) between clients