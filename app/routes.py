from app import app
from flask import render_template
from flask import request
import requests
import json
link = "https://flasktintbianca-default-rtdb.firebaseio.com/"


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',titulo="Página Inicial")

@app.route('/contato')
def contato():
    return render_template('contato.html', titulo="Contatos")

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', titulo="Cadastrar")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    try:
        cpf = request.form.get("cpf")
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")
        dados = {"cpf":cpf, "nome":nome, "telefone":telefone, "endereco":endereco}
        requisicao = requests.post(f'{link}/cadastro/.json', data= json.dumps(dados))
        return 'Cadastrado com sucesso!'
    except Exception as e:
        return f'Ocorreu um erro\n + {e}'

@app.route('/listar')
def listarTudo():
    return render_template('listar.html', titulo="Lista de Cadastros")


@app.route('/listarTodos')
def listar():
    try:
        requisicao = requests.get(f'{link}/cadastro/.json') #solicita o dado
        dicionario = requisicao.json()
        return dicionario
    except Exception as e:
        return f'Algo deu errado \n {e}'

@app.route('/listaIndi')
def individual():
    return render_template('/listarIndividual.html', titulo="Lista individual")
@app.route('/listarIndividual', methods=['POST'])
def listarIndividual():
    try:
        nome = request.form.get("nome")
        requisicao = requests.get(f'{link}/cadastro/.json')
        dicionario = requisicao.json()
        idCadastro = ""
        for codigo in dicionario:
            chave = dicionario[codigo]['nome']
            if chave == nome:
                idCadastro = codigo
                return idCadastro
    except Exception as e:
        return f'Algo deu errado \n {e}'

@app.route('/listarDados', methods=['POST'])
def listarDados():
    try:
        requisicao = requests.get(f'{link}/cadastro/.json')
        dicionario = requisicao.json()
        codigo = request.form.get("codigo")

        for codigo in dicionario:
            nome = dicionario[codigo]['nome']
            cpf = dicionario[codigo]['cpf']
            tel = dicionario[codigo]['telefone']
            end = dicionario[codigo]['endereco']
            return f'Código: {codigo} \n\n---- Nome: {nome} \n\n---- Cpf: {cpf} \n\n---- Telefone: {tel} \n\n---- Endereço: {end}'
    except Exception as e:
        return f'Algo deu errado \n {e}'


@app.route('/att')
def att():
    return render_template('/atualizar.html', titulo="Atualizar Dados")
@app.route('/atualizar', methods=['POST'])
def atualizar():
    try:
        codigo = request.form.get("codigo")
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        telefone = request.form.get("telefone")
        end = request.form.get("endereco")

        req = requests.get(f'{link}/cadastro/.json')
        dicionario = req.json()
        for codigo in dicionario:
            dados = {"codigo":codigo,"nome":nome,"cpf":cpf,"telefone": telefone,"endereco":end}
            requisicao = requests.patch(f'{link}/cadastro/{codigo}/.json', data=json.dumps(dados))
        return "Atualizado com sucesso!"
    except Exception as e:
        return f'Algo deu errado \n {e}'

@app.route('/excluirPage')
def excluirPage():
    return render_template('/excluir.html', titulo="Excluir dados")

@app.route('/excluir', methods=['POST'])
def excluir():
    try:
        codigo = request.form.get("codigo")
        requisicao = requests.get(f'{link}/cadastro/.json')
        dicionario = requisicao.json()
        dados = ""
        for codigo in dicionario:
            dados = requests.delete(f'{link}/cadastro/{codigo}/.json')
        return "Excluido com sucesso!!"
    except Exception as e:
        return f'Algo deu errado \n {e}'

@app.route('/livros')
def livros():
    return render_template('/livros.html', titulo="Livros")