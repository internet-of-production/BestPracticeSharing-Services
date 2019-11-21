#!flask/bin/python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/zwei')
def index2():
    return "Hello, World 2!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)