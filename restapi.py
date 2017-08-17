from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Resource, Api, reqparse
import read_pdf
import os

app = Flask(__name__)
api = Api(app)


ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def Welcome():
    return 'Welcome to Scoring Testing!'

@app.route('/upload', methods= ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        #f = request.files['files']
        f = request.files.getlist('srcfile')
        for f in f:
            c = request.form['collection_name']
            p = request.form['prefix']
            m = request.form['mongodb_id']
            print f.filename, c, p, m
            if not allowed_file(f.filename):
                return 'Invalid file extension. Please only upload PDF files.'
            if f and allowed_file(f.filename):
                print read_pdf.score_test(f,c,p,m)
        return '200'
    else:
        return 'Try later.'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
