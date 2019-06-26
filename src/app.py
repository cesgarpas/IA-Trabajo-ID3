from flask import Flask, render_template, request
from id3 import get_results
from testing import test

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
        result, info = get_results(data["dataset"], data["train"], data["quorum"], data["quorum_type"], data["k"], shuffle, 0)
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

        # Llamada al algoritmo
        result = test(data["dataset"], data["train"], shuffle, data["trees"], data["vary"], data["quorum_min"],
                      data["quorum_max"], data["quorum_quorum_type"], data["quorum_interval"], data["quorum_k"],
                      data["k_min"], data["k_max"], data["k_quorum"], data["k_quorum_type"])
        if result is None:
            error = "Parece que los datos de entrenamiento no son suficientes para los datos de prueba."
            error += " Pruebe un porcentaje de entrenamiento mayor o a barajar el conjunto."
            return render_template('testing_result.html', result=result, vary="Fail")
        else:
            return render_template('testing_result.html', result=result, vary=data["vary"])
    else:
        return render_template('testing_form.html')



