from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return """
    <h1>Calculadora de Refeições</h1>
    <h3>Projeto iniciado com sucesso!</h3>
    """
