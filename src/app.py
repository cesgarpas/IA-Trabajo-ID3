from flask import Flask,render_template, request
from id3 import create_tree

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('landing.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        data = request.form.to_dict()

        # Obtención del valor de barajar
        shuffle = True
        try:
            data["shuffle"]
        except:
            shuffle = False

        # Llamada al algoritmo
        result, info = create_tree(data["dataset"], data["train"], data["quorum"], data["quorum_type"], data["k"], shuffle)
        return render_template('result.html', result=result)
    else:
        return render_template('form.html')

@app.route('/testing', methods=['GET', 'POST'])
def testing():
    if request.method == 'POST':
        data = request.form.to_dict()

        # Obtención del valor de barajar
        shuffle = True
        try:
            data["shuffle"]
        except:
            shuffle = False

        print(data)

        # Llamada al algoritmo
        #result, info = create_tree(data["dataset"], data["train"], data["quorum"], data["quorum_type"], data["k"], shuffle)
        return render_template('testing_form.html')
    else:
        return render_template('testing_form.html')



