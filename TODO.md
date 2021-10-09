# TODO:
<span style="color: green">Green</span>: Done\
<span style="color: orange">Orange</span>: Partly done\
<span style="color: red">Red</span>: Not done\
<span style="color: blue">Blue</span>: Currently in progress

###General:
- What if a client looses internet connection, gets a timeout from server, and reconnect - still with an old (and possibly in-use) connection ID?

- ###Client:
- [x] <span style="color: green">Develop main GUI root window
- [x] <span style="color: green">Develop preferences- menu option and window
- [x] <span style="color: orange">Develop dashboard window
  - [x] <span style="color: green">Create rudimentary layout
  - [x] <span style="color: green">Load available clients from server and display them in item list
  - [ ] <span style="color: blue">Develop interaction with these items as to initiate remote control (requires client-to-client authentication)


- ###Server:
- [x] <span style="color: green">Establish fundamental networking logic
- [x] <span style="color: green">Develop system to send and receive commands to/from clients
- [ ] <span style="color: red">Kick clients from memory after a certain timeout
- [ ] <span style="color: orange">Missing server/client commands:
  - [x] <span style="color: green">Being able to start and stop other clients from streaming
  - [ ] <span style="color: red">Being able to kick other clients from the network
  - [ ] <span style="color: red">Being able to change server password from a client
  - [ ] <span style="color: red">Being able to rename other clients
  - [ ] <span style="color: red">Being able to change the client password of other clients (requires client-to-client authentication)