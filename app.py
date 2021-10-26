from flask import Flask, redirect, url_for, render_template, request
from graphviz import dot
from Analyzer.Grammar import parse
import graphviz

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

headingsSimbolos = ("Environment", "Name", "Type", "Value", "Line", "Column")
headingsErrores = ("Type", "Error", "Line", "Column")

@app.route("/analyze", methods=["POST","GET"])
def analyze():
    if request.method == "POST":
        inpt = request.form["inpt"]
        global tmp_val
        tmp_val=inpt
        tmp_val = str(tmp_val).replace('||', '!!!')
        tmp_val = str(tmp_val).replace('global ', '')
        tmp_val = str(tmp_val).replace('local ', '')
        return redirect(url_for("output"))
    else:
        return render_template('analyze.html', initial="")

@app.route('/output', methods=["POST", "GET"])
def output():
    global tmp_val
    result = parse(tmp_val)
    app.c = result[1]
    # Eliminar las siguientes 2 lineas cuando ya se tenga todo
    result[2] = () # Datos de simbolos o errores
    result[3] = () # Codigo dot para copiar y pegar en un graficador online
    if request.method == "POST":
        return redirect(url_for("grafo"))
    else:
        if result[3] == '':
            return render_template('output.html', input=result[0], headings=headingsErrores, data=result[2], codigo=result[3])
        return render_template('output.html', input=result[0], headings=headingsSimbolos, data=result[2], codigo=result[3])

@app.route('/grafo')
def grafo():
    dot = app.c
    return dot.pipe().decode('utf-8')

if __name__ == '__main__':
    app.run()