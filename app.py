import csv
from io import StringIO
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit

from utils import faqs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.get("/")
def hello_world():
    return render_template('index.html')


@app.get('/faqs')
def faqs():
    return faqs.get_swinburne_faqs()


@app.get('/faqs/download')
def download_faqs():
    questions_answers = faqs.get_swinburne_faqs()

    def generate_csv():
        in_memory_file = StringIO()
        csv_writer = csv.writer(in_memory_file)
        csv_writer.writerow(['Questions', 'Answers'])
        for question, answer in questions_answers:
            # write the row to the in-memory object
            csv_writer.writerow([question, answer])
            csv_row = in_memory_file.getvalue()
            # reset the in-memory object for the next row
            in_memory_file.seek(0)
            in_memory_file.truncate(0)
            yield csv_row

    return Response(
        generate_csv(),
        content_type='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=faqs.csv'
        }
    )


@socketio.on('message')
def handle_message(msg):
    print(f'Message: {msg}')
    emit('message', msg)
    socketio.sleep(1)
    socketio.emit('message', f'Hello from the server')


if __name__ == '__main__':
    socketio.run(app, debug=True, host='localhost', port=8000)
