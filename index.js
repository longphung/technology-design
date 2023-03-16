const app = require('express')();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', (socket) => {
  console.log('Client connected');

  // When a message is received from a client
  socket.on('chat message', (msg) => {
    console.log(`Received message: ${msg}`);

    // Broadcast the message to all connected clients
    io.emit('chat message', msg);
    // Reply to the client that sent the message after 1 second as an example
    setTimeout(() => {
      socket.emit('chat message', 'Hello from the server');
    }, 1000);
  });

  // When a client disconnects
  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

http.listen(8080, () => {
  console.log('Listening on port 8080');
});
