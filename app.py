import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.get("/")
def hello_world():
    return render_template('index.html')


@app.get('/faqs')
def faqs():
    response = requests.get('https://www.swinburneonline.edu.au/faqs/')
    soup = BeautifulSoup(response.content, 'html.parser')
    # Get faq cards
    faqs_cards = soup.select('.faqs-group .card')
    result = []
    # loop through and get questions and answers
    for faq in faqs_cards:
        question_el = faq.select_one('.card-header h5 > div:nth-child(2)')
        answer_el = faq.select_one('.card-body .content')
        # add to result if question and answer exist
        if question_el and answer_el:
            question = question_el.get_text(strip=True)
            answer = answer_el.get_text(strip=True)
            result.append((question, answer))
    return result


@socketio.on('message')
def handle_message(msg):
    print(f'Message: {msg}')
    emit('message', msg)
    socketio.sleep(1)
    socketio.emit('message', f'Hello from the server')


if __name__ == '__main__':
    socketio.run(app, debug=True, host='localhost', port=8000)
