import csv
from io import StringIO
from flask import Flask, render_template, Response, request
from flask_cors import CORS

from utils import faqs, models

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'


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


@app.post('/message')
def post_message():
    print(request.json)
    string = request.json['string']
    result = models.classify(string)
    print(result)
    if result[0] == "in-scope":
        stream = models.generate_in_scope(string)
    else:
        stream = models.generate_out_of_scope(string)
    return Response(stream, mimetype='text/event-stream')



async def server_loop(q):
    while True:
        (string, response_q) = await q.get()
        out = models.classify(string)
        response_q.put_nowait({'out': out, 'string': string})




if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)
