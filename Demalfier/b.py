from bottle import route, run, template
from realtestmodel import test

@route('/hello/<name>')
@route('/hello')
def hello():
    #return "Hello World!"
    a = test("google.co.in")
    return a
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)
