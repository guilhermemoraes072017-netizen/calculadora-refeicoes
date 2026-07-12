from flask import Flask, request, redirect, session, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "trocar-esta-chave-depois"

# Banco temporário apenas para iniciarmos o sistema.
# Depois será substituído por um banco de dados online.
usuarios = {
    "admin": {
        "nome": "Administrador",
        "empresa": "Administração do Sistema",
        "senha": generate_password_hash("admin123"),
        "tipo": "admin"
    }
}


PAGINA_INICIAL = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora de Refeições</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            color: #1e293b;
        }

        .topo {
            background: #0f172a;
            color: white;
            padding: 22px;
            text-align: center;
        }

        .conteudo {
            max-width: 900px;
            margin: 60px auto;
            padding: 20px;
            text-align: center;
        }

        .cartao {
            background: white;
            border-radius: 18px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }

        h1 {
            margin-top: 0;
        }

        .botoes {
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
            margin-top: 30px;
        }

        .botao {
            display: inline-block;
            padding: 14px 28px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: bold;
            background: #2563eb;
            color: white;
        }

        .botao-secundario {
            background: #16a34a;
        }

        .rodape {
            margin-top: 30px;
            color: #64748b;
            font-size: 14px;
        }
    </style>
</head>

<body>
    <div class="topo">
        <h2>Calculadora de Refeições</h2>
    </div>

    <div class="conteudo">
        <div class="cartao">
            <h1>Organize seus cálculos de forma simples</h1>

            <p>
                Sistema criado para restaurantes, marmitarias,
                lanchonetes e outros estabelecimentos.
            </p>

            <div class="botoes">
                <a class="botao" href="/login">Entrar</a>
                <a class="botao botao-secundario" href="/cadastro">
                    Criar conta
                </a>
            </div>
        </div>

        <div class="rodape">
            Sistema administrado pelo proprietário da plataforma.
        </div>
    </div>
</body>
</html>
"""


LOGIN = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Entrar</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            margin: 0;
        }

        .caixa {
            max-width: 420px;
            margin: 70px auto;
            background: white;
            padding: 35px;
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }

        h1 {
            text-align: center;
        }

        input {
            width: 100%;
            padding: 13px;
            margin: 8px 0 18px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 16px;
        }

        button {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 8px;
            background: #2563eb;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        .mensagem {
            color: #dc2626;
            text-align: center;
        }

        .voltar {
            display: block;
            text-align: center;
            margin-top: 20px;
        }
    </style>
</head>

<body>
    <div class="caixa">
        <h1>Entrar</h1>

        {% if mensagem %}
            <p class="mensagem">{{ mensagem }}</p>
        {% endif %}

        <form method="post">
            <label>Usuário</label>
            <input name="usuario" required>

            <label>Senha</label>
            <input name="senha" type="password" required>

            <button type="submit">Entrar</button>
        </form>

        <a class="voltar" href="/">Voltar</a>
    </div>
</body>
</html>
"""


CADASTRO = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Criar conta</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            margin: 0;
        }

        .caixa {
            max-width: 520px;
            margin: 40px auto;
            background: white;
            padding: 35px;
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }

        h1 {
            text-align: center;
        }

        input {
            width: 100%;
            padding: 13px;
            margin: 8px 0 18px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 16px;
        }

        button {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 8px;
            background: #16a34a;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        .mensagem {
            color: #dc2626;
            text-align: center;
        }

        .voltar {
            display: block;
            text-align: center;
            margin-top: 20px;
        }
    </style>
</head>

<body>
    <div class="caixa">
        <h1>Criar conta</h1>

        {% if mensagem %}
            <p class="mensagem">{{ mensagem }}</p>
        {% endif %}

        <form method="post">
            <label>Seu nome</label>
            <input name="nome" required>

            <label>Nome da empresa</label>
            <input name="empresa" required>

            <label>Nome de usuário</label>
            <input name="usuario" required>

            <label>Senha</label>
            <input name="senha" type="password" minlength="6" required>

            <button type="submit">Criar minha conta</button>
        </form>

        <a class="voltar" href="/">Voltar</a>
    </div>
</body>
</html>
"""


PAINEL = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            margin: 0;
        }

        .topo {
            background: #0f172a;
            color: white;
            padding: 20px;
        }

        .conteudo {
            max-width: 1000px;
            margin: 35px auto;
            padding: 20px;
        }

        .cartao {
            background: white;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.07);
            margin-bottom: 20px;
        }

        .menu {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
            gap: 15px;
        }

        .item {
            background: #e2e8f0;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            font-weight: bold;
        }

        .sair {
            color: white;
            float: right;
        }
    </style>
</head>

<body>
    <div class="topo">
        <strong>Calculadora de Refeições</strong>
        <a class="sair" href="/sair">Sair</a>
    </div>

    <div class="conteudo">
        <div class="cartao">
            <h1>Olá, {{ nome }}!</h1>
            <p>Empresa: <strong>{{ empresa }}</strong></p>

            {% if tipo == "admin" %}
                <p>Você entrou como administrador geral.</p>
            {% else %}
                <p>Sua conta está pronta para começar a usar.</p>
            {% endif %}
        </div>

        <div class="menu">
            <div class="item">Nova refeição</div>
            <div class="item">Produtos e valores</div>
            <div class="item">Histórico</div>
            <div class="item">Relatórios</div>
            <div class="item">Dados da empresa</div>

            {% if tipo == "admin" %}
                <div class="item">Administração geral</div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""


@app.route("/")
def inicio():
    return render_template_string(PAGINA_INICIAL)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    mensagem = ""

    if request.method == "POST":
        nome = request.form["nome"].strip()
        empresa = request.form["empresa"].strip()
        usuario = request.form["usuario"].strip().lower()
        senha = request.form["senha"]

        if usuario in usuarios:
            mensagem = "Este nome de usuário já está sendo usado."
        else:
            usuarios[usuario] = {
                "nome": nome,
                "empresa": empresa,
                "senha": generate_password_hash(senha),
                "tipo": "cliente"
            }

            session["usuario"] = usuario
            return redirect("/painel")

    return render_template_string(CADASTRO, mensagem=mensagem)


@app.route("/login", methods=["GET", "POST"])
def login():
    mensagem = ""

    if request.method == "POST":
        usuario = request.form["usuario"].strip().lower()
        senha = request.form["senha"]

        conta = usuarios.get(usuario)

        if conta and check_password_hash(conta["senha"], senha):
            session["usuario"] = usuario
            return redirect("/painel")

        mensagem = "Usuário ou senha incorretos."

    return render_template_string(LOGIN, mensagem=mensagem)


@app.route("/painel")
def painel():
    usuario = session.get("usuario")

    if not usuario or usuario not in usuarios:
        return redirect("/login")

    conta = usuarios[usuario]

    return render_template_string(
        PAINEL,
        nome=conta["nome"],
        empresa=conta["empresa"],
        tipo=conta["tipo"]
    )


@app.route("/sair")
def sair():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
