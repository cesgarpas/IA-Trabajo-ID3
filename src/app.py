from flask import Flask,render_template, request
from id3 import create_tree
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('landing.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        create_tree(data["dataset"], data["train"], data["quorum"], data["quorum_type"], data["k"])
        return "Correcto!"
    else:
        print("GET")
        return render_template('form.html')



