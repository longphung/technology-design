from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route("/")
def hello_world():
    return render_template('index.html')


@socketio.on('message')
def handle_message(msg):
    print(f'Message: {msg}')
    emit('message', msg)
    socketio.sleep(1)
    socketio.emit('message', f'Hello from the server')


if __name__ == '__main__':
    socketio.run(app, debug=True, host='localhost', port=8000)
